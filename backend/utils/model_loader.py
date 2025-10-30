"""
Model loading and inference utilities
"""

import traceback

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch_geometric.nn import GCNConv
    try:
        from torchdiffeq import odeint
        TORCHDIFFEQ_AVAILABLE = True
    except ImportError:
        TORCHDIFFEQ_AVAILABLE = False
        print("⚠️  torchdiffeq not available - GNODE model will use simplified version")
    TORCH_AVAILABLE = True
    print("✅ PyTorch is available - GNODE model ready")
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️  PyTorch not installed. Using mock predictions only.")

from pathlib import Path


# ==================== GNODE Model Architecture ====================
if TORCH_AVAILABLE:
    class ODEFunc(nn.Module):
        """ODE function component for GNODE model"""
        def __init__(self, in_channels, hidden_channels, edge_index):
            super(ODEFunc, self).__init__()
            self.edge_index = edge_index
            self.gc1 = GCNConv(in_channels, hidden_channels)
            self.gc2 = GCNConv(hidden_channels, hidden_channels)

        def forward(self, t, x):
            """Forward pass - t is required by torchdiffeq"""
            x = self.gc1(x, self.edge_index)
            x = F.relu(x)
            x = self.gc2(x, self.edge_index)
            return x

    class GNODEModel(nn.Module):
        """Graph Neural Ordinary Differential Equation Model"""
        def __init__(self, in_channels, hidden_channels, out_channels, edge_index):
            super(GNODEModel, self).__init__()
            self.input_proj = nn.Linear(in_channels, hidden_channels)
            self.odefunc = ODEFunc(hidden_channels, hidden_channels, edge_index)
            self.linear = nn.Linear(hidden_channels, out_channels)
            self.in_channels = in_channels
            self.hidden_channels = hidden_channels
            self.out_channels = out_channels

        def forward(self, x):
            """Forward pass through GNODE model"""
            # Project input to hidden dimension
            x = self.input_proj(x)
            x = F.relu(x)
            
            # Solve ODE if torchdiffeq is available
            if TORCHDIFFEQ_AVAILABLE:
                t = torch.tensor([0.0, 1.0], dtype=torch.float32, device=x.device)
                out = odeint(self.odefunc, x, t, method='rk4', options={'step_size': 0.1})
                out = out[-1]  # Take last time step
            else:
                # Simplified version without ODE solver
                out = self.odefunc(0, x)  # Direct GNN application
            
            # Project to output classes
            out = self.linear(out)
            return out

        def predict_proba(self, x):
            """Get probability predictions"""
            self.eval()
            with torch.no_grad():
                logits = self.forward(x)
                probs = F.softmax(logits, dim=1)
            return probs
# ===================================================================


class GNODEModelWrapper:
    """Wrapper for GNODE model with inference capabilities"""
    
    def __init__(self, model_path=None):
        self.model = None
        self.model_path = model_path
        
        if TORCH_AVAILABLE:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            print(f"🔧 Device: {self.device}")
        else:
            self.device = 'cpu'
            print("⚠️  PyTorch not available, will use mock predictions")
        
        if model_path:
            print(f"🔍 Looking for model at: {model_path}")
            if Path(model_path).exists():
                print(f"✅ Model file found!")
                if TORCH_AVAILABLE:
                    self.load_model(model_path)
                else:
                    print("⚠️  Cannot load model: PyTorch not available")
            else:
                print(f"⚠️  Model file not found at: {model_path}")
                print(f"   Will use mock predictions until model is added")
        else:
            print("⚠️  No model path provided")
    
    def load_model(self, model_path):
        """Load trained GNODE model from file"""
        if not TORCH_AVAILABLE:
            print("❌ Cannot load model: PyTorch not installed")
            return False
            
        try:
            print(f"⏳ Loading GNODE model...")
            
            # Create GNODE model architecture
            # Input: 7 features -> Hidden: 32 -> Output: 2 classes
            edge_index = torch.tensor([[0], [0]], dtype=torch.long).to(self.device)
            self.model = GNODEModel(
                in_channels=7,
                hidden_channels=32,
                out_channels=2,
                edge_index=edge_index
            ).to(self.device)
            
            # Load trained weights
            state_dict = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state_dict)
            self.model.eval()
            
            print(f"✅ GNODE model loaded successfully!")
            print(f"   Path: {model_path}")
            print(f"   Device: {self.device}")
            print(f"   Architecture: 7 inputs → 32 hidden → 2 outputs (ODE solver)")
            return True
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def predict(self, features):
        """
        Make prediction using GNODE model.
        
        Input: features dict with keys:
            - mw: molecular weight
            - tissue_sweat: 0 or 1
            - tissue_urine: 0 or 1
            - rms_feat: EMG feature
            - zero_crossings: EMG feature
            - skewness: EMG feature
            - waveform_length: EMG feature
        
        Output: risk score (0-100)
        """
        if not TORCH_AVAILABLE or self.model is None:
            # Return mock prediction if PyTorch not available or model not loaded
            print("⚠️  Using mock prediction (model not loaded)")
            return self._mock_prediction(features)
        
        try:
            # Convert features to tensor
            feature_vector = [
                features['mw'],
                features['tissue_sweat'],
                features['tissue_urine'],
                features['rms_feat'],
                features['zero_crossings'],
                features['skewness'],
                features['waveform_length']
            ]
            
            input_tensor = torch.FloatTensor([feature_vector]).to(self.device)
            
            # Create self-loop edge index for single sample
            edge_index = torch.tensor([[0], [0]], dtype=torch.long).to(self.device)
            
            # Update model's edge_index (GNODE needs it)
            if hasattr(self.model, 'odefunc'):
                self.model.odefunc.edge_index = edge_index
            
            # Make prediction using GNODE
            with torch.no_grad():
                self.model.eval()
                logits = self.model(input_tensor)
                probs = F.softmax(logits, dim=1)
                risk_score = probs[0, 1].item() * 100  # Probability of injury class
            
            print(f"✅ GNODE prediction: {risk_score:.2f}%")
            return risk_score
            
        except Exception as e:
            print(f"❌ Error during GNODE prediction: {e}")
            print("⚠️  Falling back to mock prediction")
            return self._mock_prediction(features)
    
    def _mock_prediction(self, features):
        """
        Generate mock prediction based on features.
        Used when actual model is not available.
        Uses a more sophisticated heuristic that considers biomarker deviation.
        """
        # Extract features
        mw = features.get('mw', 200)
        tissue_sweat = features.get('tissue_sweat', 0)
        tissue_urine = features.get('tissue_urine', 0)
        
        # Get metadata if available (passed from app.py)
        metadata = features.get('metadata', {})
        
        print(f"\n🔍 Mock Prediction Debug:")
        print(f"   MW: {mw} Da")
        print(f"   Tissue: sweat={tissue_sweat}, urine={tissue_urine}")
        print(f"   Metadata present: {bool(metadata)}")
        
        # Base score calculation using molecular weight
        # Smaller molecules (like lactate 89 Da) typically indicate higher metabolic stress
        if mw < 100:
            mw_score = 40  # High risk molecules
        elif mw < 200:
            mw_score = 30
        elif mw < 400:
            mw_score = 20
        else:
            mw_score = 15  # Large molecules, lower base risk
        
        print(f"   MW Score: {mw_score}")
        
        # Tissue type impact
        tissue_score = 0
        if tissue_sweat == 1:
            tissue_score = 15  # Sweat biomarkers most indicative for muscle injury
        elif tissue_urine == 1:
            tissue_score = 10  # Urine biomarkers moderately indicative
        else:  # saliva
            tissue_score = 5
        
        print(f"   Tissue Score: {tissue_score}")
        
        # CRITICAL: Use biomarker deviation/elevation data if available
        elevation_score = 0
        if metadata:
            # Get the actual deviation of the primary biomarker
            metabolite_scores = metadata.get('metabolite_scores', {})
            tissue_scores_data = metadata.get('tissue_scores', {})
            primary_tissue = metadata.get('primary_tissue', '')
            primary_biomarker = metadata.get('primary_biomarker', '')
            
            print(f"   Primary Tissue: {primary_tissue}")
            print(f"   Primary Biomarker: {primary_biomarker}")
            
            # Use the average elevation from the primary tissue
            if primary_tissue and tissue_scores_data:
                tissue_info = tissue_scores_data.get(primary_tissue, {})
                avg_elevation = tissue_info.get('elevation', 0)
                
                print(f"   Average Elevation: {avg_elevation:.2f}")
                
                # Elevation ranges from 0 (normal) to 2.0 (very abnormal)
                # Convert to risk contribution (0-30 points)
                elevation_score = avg_elevation * 15  # 0-30 points
        
        print(f"   Elevation Score: {elevation_score:.1f}")
        
        # EMG features contribution (if different from defaults)
        emg_score = 0
        rms_feat = features.get('rms_feat', 0.5)
        if rms_feat > 0.6:  # Higher RMS might indicate muscle fatigue
            emg_score += 5
        
        print(f"   EMG Score: {emg_score}")
        
        # Combine all scores
        total_score = mw_score + tissue_score + elevation_score + emg_score
        
        # Add slight variability for realism
        import random
        noise = random.uniform(-3, 3)
        
        risk_score = max(5, min(95, total_score + noise))
        
        print(f"   Total (before noise): {total_score}")
        print(f"   Noise: {noise:.1f}")
        print(f"   FINAL RISK SCORE: {risk_score:.1f}%\n")
        
        return risk_score


# Global model instance
_model_instance = None

def get_model():
    """Get global model instance"""
    global _model_instance
    if _model_instance is None:
        from config import Config
        _model_instance = GNODEModelWrapper(Config.MODEL_PATH)
    return _model_instance

def predict_injury_risk(features):
    """Wrapper function for making predictions"""
    model = get_model()
    return model.predict(features)
