"""Test if GNODE model loads correctly"""

print("\n" + "="*60)
print("TESTING GNODE MODEL LOADING")
print("="*60 + "\n")

# Test 1: Check config
print("1. Checking config...")
from config import Config
print(f"   MODEL_PATH from config: {Config.MODEL_PATH}")

# Test 2: Check if file exists
from pathlib import Path
model_path = Path(Config.MODEL_PATH)
print(f"   Absolute path: {model_path.absolute()}")
print(f"   File exists: {model_path.exists()}")

if model_path.exists():
    print(f"   File size: {model_path.stat().st_size} bytes")
else:
    print(f"   ⚠️  FILE NOT FOUND!")
    # List what IS in models directory
    models_dir = Path("models")
    if models_dir.exists():
        print(f"\n   Files in models directory:")
        for f in models_dir.iterdir():
            print(f"      - {f.name}")

# Test 3: Try loading model
print("\n2. Loading model...")
from utils.model_loader import get_model

model = get_model()
print(f"\n3. Model loaded: {model.model is not None}")
if model.model:
    print(f"   Model type: {type(model.model)}")
    print(f"   Device: {model.device}")
else:
    print(f"   ⚠️  Model is None - will use mock predictions")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
