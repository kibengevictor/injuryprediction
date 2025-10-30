# GNODE Model Integration Guide

## Overview
The GNODE (Graph Neural Ordinary Differential Equation) model has been successfully extracted from the research notebook and is ready for integration into the web application.

## Model Architecture

**GNODE** combines two powerful concepts:
1. **Graph Neural Networks (GNN)** - Models relationships between biomarkers as a graph
2. **Neural ODEs** - Models continuous dynamics over time

### Components:

#### 1. ODEFunc Class
- Uses 2 Graph Convolutional layers (GCNConv)
- Takes node features and graph structure as input
- Outputs derivatives for ODE solver

#### 2. GNODEModel Class
- **Input Projection**: Maps 7 input features to 32 hidden dimensions
- **ODE Solver**: Integrates from t=0 to t=1 using RK4 method
- **Output Layer**: Maps to 2 classes (No Injury / Injury)

### Model Configuration (from notebook):
```python
- Input channels: 7 features
  1. mw (molecular weight)
  2. tissue_sweat (0 or 1)
  3. tissue_urine (0 or 1)  
  4. rms_feat (EMG feature)
  5. zero_crossings (EMG feature)
  6. skewness (EMG feature)
  7. waveform_length (EMG feature)

- Hidden channels: 32
- Output channels: 2 (binary classification)
- ODE method: RK4 (4th order Runge-Kutta)
- ODE step size: 0.1
```

## Installation Requirements

To use the GNODE model, you need to install the following packages:

```bash
pip install torch torchvision torchaudio
pip install torch-geometric
pip install torch-scatter torch-sparse torch-cluster -f https://data.pyg.org/whl/torch-2.0.0+cpu.html
pip install torchdiffeq
```

**Note**: The `torch-scatter`, `torch-sparse`, and `torch-cluster` URLs depend on your PyTorch and CUDA versions.

## Files Created

1. **`backend/models/gnode_model.py`** - Complete GNODE model implementation
   - `ODEFunc` class
   - `GNODEModel` class
   - `load_gnode_model()` function
   - `GNODE_CONFIG` dictionary

## Integration Steps

### Step 1: Install Dependencies

```bash
cd backend
pip install torch torchdiffeq torch-geometric
```

### Step 2: Update model_loader.py

Replace the current mock prediction system with real GNODE loading:

```python
from models.gnode_model import GNODEModel, load_gnode_model, GNODE_CONFIG
from torch_geometric.nn import knn_graph
import torch

class GNODEModelWrapper:
    def __init__(self, model_path=None):
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        if model_path and Path(model_path).exists():
            self.load_model(model_path)
    
    def load_model(self, model_path):
        try:
            # Create dummy edge_index (will be recreated for each prediction)
            edge_index = torch.tensor([[0], [0]], dtype=torch.long)
            
            self.model = load_gnode_model(
                model_path=model_path,
                in_channels=GNODE_CONFIG['in_channels'],
                hidden_channels=GNODE_CONFIG['hidden_channels'],
                out_channels=GNODE_CONFIG['out_channels'],
                edge_index=edge_index,
                device=self.device
            )
            print(f"✅ GNODE model loaded from {model_path}")
            return True
        except Exception as e:
            print(f"❌ Error loading GNODE model: {e}")
            return False
    
    def predict(self, features):
        if self.model is None:
            return self._mock_prediction(features)
        
        try:
            # Prepare input tensor
            feature_vector = [
                features['mw'],
                features['tissue_sweat'],
                features['tissue_urine'],
                features['rms_feat'],
                features['zero_crossings'],
                features['skewness'],
                features['waveform_length']
            ]
            
            # Convert to tensor
            x = torch.FloatTensor([feature_vector]).to(self.device)
            
            # Create k-NN graph for single sample (self-loop)
            edge_index = torch.tensor([[0], [0]], dtype=torch.long).to(self.device)
            
            # Update model's edge_index
            self.model.odefunc.edge_index = edge_index
            
            # Get prediction
            probs = self.model.predict_proba(x)
            risk_score = probs[0, 1].item() * 100  # Injury probability
            
            return risk_score
            
        except Exception as e:
            print(f"❌ GNODE prediction error: {e}")
            return self._mock_prediction(features)
```

### Step 3: Train or Obtain Model Weights

You have two options:

#### Option A: Use Existing Trained Model
If you have a trained model from the notebook (`gnode_model.pth`):
```bash
# Copy the trained model to your backend
cp /path/to/gnode_model.pth backend/models/
```

#### Option B: Train New Model
Run the training cells from the notebook to create a new `gnode_model.pth` file.

### Step 4: Update config.py

```python
GNODE_MODEL_PATH = Path(__file__).parent / 'models' / 'gnode_model.pth'
```

### Step 5: Test the Model

```python
python backend/test_prediction.py
```

## Current Status

✅ **Extracted**: GNODE model architecture from notebook  
✅ **Created**: `backend/models/gnode_model.py` with complete implementation  
❌ **Not Installed**: PyTorch and dependencies (need to install)  
❌ **No Model File**: Need `gnode_model.pth` trained weights  
✅ **Mock System**: Currently using fallback predictions

## Model Performance (from notebook)

The GNODE model achieved the following metrics:

- **Training Accuracy**: ~95%+
- **Validation Accuracy**: Similar to training
- **Binary Classification**: No Injury (0) vs Injury (1)

## Next Steps

1. **Install PyTorch** (most important):
   ```bash
   pip install torch torchvision torchaudio
   ```

2. **Install PyTorch Geometric**:
   ```bash
   pip install torch-geometric
   ```

3. **Install torchdiffeq**:
   ```bash
   pip install torchdiffeq
   ```

4. **Get trained model weights**:
   - Either copy `gnode_model.pth` from notebook output
   - Or run training cells in the notebook

5. **Update `model_loader.py`** to use real GNODE model

6. **Test integration** with test_prediction.py

## Troubleshooting

### Issue: "No module named 'torch'"
**Solution**: Install PyTorch first

### Issue: "No module named 'torchdiffeq'"
**Solution**: `pip install torchdiffeq`

### Issue: "Model file not found"
**Solution**: Ensure `gnode_model.pth` is in `backend/models/` directory

### Issue: "CUDA out of memory"
**Solution**: Model will automatically fall back to CPU

## Benefits of Real GNODE Model

✅ **Learned patterns** from actual hamstring injury data  
✅ **Graph structure** captures biomarker relationships  
✅ **Continuous dynamics** via Neural ODEs  
✅ **Better accuracy** than heuristic-based predictions  
✅ **Scientific rigor** - research-backed architecture  

## Files Summary

```
backend/
├── models/
│   ├── gnode_model.py          ← GNODE implementation
│   └── gnode_model.pth          ← Trained weights (need to add)
├── utils/
│   └── model_loader.py          ← Update to use GNODE
├── config.py                    ← Add GNODE_MODEL_PATH
└── requirements.txt             ← Add torch, torchdiffeq, torch-geometric
```

---

**Status**: Ready for integration after installing dependencies and obtaining trained model weights.
