import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Model settings
    MODEL_PATH = os.getenv('MODEL_PATH', 'models/gnode_model.pth')  # Fixed: .pth not .pt
    MODEL_TYPE = 'GNODE'
    
    # API settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    JSON_SORT_KEYS = False
    
    # Biomarker settings
    REQUIRED_FEATURES = ['mw', 'tissue_sweat', 'tissue_urine', 'rms_feat', 
                        'zero_crossings', 'skewness', 'waveform_length']
    
    # Default EMG feature values (when not provided)
    DEFAULT_EMG_VALUES = {
        'rms_feat': 0.0,
        'zero_crossings': 0.0,
        'skewness': 0.0,
        'waveform_length': 0.0
    }
