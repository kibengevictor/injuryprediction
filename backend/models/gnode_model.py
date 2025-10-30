"""
GNODE (Graph Neural ODE) Model for Hamstring Injury Prediction
Extracted from research notebook

This model uses Graph Convolutional Networks combined with Neural ODEs
to model continuous dynamics of biomarker interactions over time.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv

try:
    from torchdiffeq import odeint
    TORCHDIFFEQ_AVAILABLE = True
except ImportError:
    TORCHDIFFEQ_AVAILABLE = False
    print("⚠️ torchdiffeq not installed. Install with: pip install torchdiffeq")


class ODEFunc(nn.Module):
    """
    ODE function component for GNODE model.
    Defines the derivative function for the Neural ODE.
    """
    def __init__(self, in_channels, hidden_channels, edge_index):
        super(ODEFunc, self).__init__()
        self.edge_index = edge_index
        self.gc1 = GCNConv(in_channels, hidden_channels)
        self.gc2 = GCNConv(hidden_channels, hidden_channels)

    def forward(self, t, x):
        """
        Forward pass for ODE function.
        
        Args:
            t: Time parameter (required by torchdiffeq, may be unused)
            x: Node features tensor [num_nodes, hidden_channels]
            
        Returns:
            Derivative of x with respect to time
        """
        # Apply first graph convolution
        x = self.gc1(x, self.edge_index)
        x = F.relu(x)
        
        # Apply second graph convolution
        x = self.gc2(x, self.edge_index)
        
        return x


class GNODEModel(nn.Module):
    """
    Graph Neural Ordinary Differential Equation (GNODE) Model.
    
    Architecture:
    1. Input projection layer (maps input features to hidden dimension)
    2. ODE solver with graph convolutions (models continuous dynamics)
    3. Output projection layer (maps to class probabilities)
    
    Args:
        in_channels (int): Number of input features per node
        hidden_channels (int): Number of hidden features
        out_channels (int): Number of output classes
        edge_index (torch.Tensor): Graph edge connectivity [2, num_edges]
    """
    def __init__(self, in_channels, hidden_channels, out_channels, edge_index):
        super(GNODEModel, self).__init__()
        
        # Project input features to hidden dimension
        self.input_proj = nn.Linear(in_channels, hidden_channels)
        
        # ODE function for continuous dynamics
        self.odefunc = ODEFunc(hidden_channels, hidden_channels, edge_index)
        
        # Output projection layer
        self.linear = nn.Linear(hidden_channels, out_channels)
        
        # Store configuration
        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.out_channels = out_channels

    def forward(self, x):
        """
        Forward pass through GNODE model.
        
        Args:
            x: Input node features [num_nodes, in_channels]
            
        Returns:
            Output logits [num_nodes, out_channels]
        """
        if not TORCHDIFFEQ_AVAILABLE:
            raise RuntimeError("torchdiffeq is required but not installed")
        
        # Project input to hidden dimension
        x = self.input_proj(x)
        x = F.relu(x)
        
        # Solve ODE from t0=0 to t1=1 using RK4 method
        t = torch.tensor([0.0, 1.0], dtype=torch.float32, device=x.device)
        out = odeint(
            self.odefunc, 
            x, 
            t, 
            method='rk4',  # 4th order Runge-Kutta
            options={'step_size': 0.1}
        )
        
        # Take the last time step
        out = out[-1]
        
        # Project to output classes
        out = self.linear(out)
        
        return out
    
    def predict_proba(self, x):
        """
        Get probability predictions.
        
        Args:
            x: Input node features [num_nodes, in_channels]
            
        Returns:
            Class probabilities [num_nodes, out_channels]
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits, dim=1)
        return probs
    
    def predict(self, x):
        """
        Get class predictions.
        
        Args:
            x: Input node features [num_nodes, in_channels]
            
        Returns:
            Class predictions [num_nodes]
        """
        probs = self.predict_proba(x)
        return probs.argmax(dim=1)


def load_gnode_model(model_path, in_channels, hidden_channels, out_channels, edge_index, device='cpu'):
    """
    Load a trained GNODE model from file.
    
    Args:
        model_path (str): Path to saved model weights (.pth file)
        in_channels (int): Number of input features
        hidden_channels (int): Number of hidden features
        out_channels (int): Number of output classes
        edge_index (torch.Tensor): Graph edge connectivity
        device (str): Device to load model on ('cpu' or 'cuda')
        
    Returns:
        Loaded GNODE model
    """
    model = GNODEModel(
        in_channels=in_channels,
        hidden_channels=hidden_channels,
        out_channels=out_channels,
        edge_index=edge_index
    )
    
    # Load state dict
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    
    return model


# Model configuration from notebook
GNODE_CONFIG = {
    'in_channels': 7,  # Number of features (mw, tissue_sweat, tissue_urine, rms_feat, etc.)
    'hidden_channels': 32,
    'out_channels': 2,  # Binary classification (No Injury=0, Injury=1)
    'learning_rate': 0.01,
    'weight_decay': 5e-4,
    'epochs': 50,
    'ode_method': 'rk4',
    'ode_step_size': 0.1,
    'k_neighbors': 5  # for k-NN graph construction
}


if __name__ == "__main__":
    # Example usage
    print("GNODE Model Configuration:")
    print(f"  Input channels: {GNODE_CONFIG['in_channels']}")
    print(f"  Hidden channels: {GNODE_CONFIG['hidden_channels']}")
    print(f"  Output channels: {GNODE_CONFIG['out_channels']}")
    print(f"  ODE method: {GNODE_CONFIG['ode_method']}")
    print(f"  ODE step size: {GNODE_CONFIG['ode_step_size']}")
    
    if TORCHDIFFEQ_AVAILABLE:
        print("\n✅ torchdiffeq is available - GNODE model ready to use")
    else:
        print("\n❌ torchdiffeq not available - install with: pip install torchdiffeq")
