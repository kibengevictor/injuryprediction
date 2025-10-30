"""
Test script to verify prediction varies with different inputs
"""
import requests
import json

API_URL = "http://localhost:5001/api/predict"

# Test 1: Normal values (should be LOW risk)
test1_normal = {
    "saliva": {
        "cortisol": 3.5,
        "testosterone": 90.0,
        "iga": 150.0
    },
    "sweat": {
        "sodium": 25.0,
        "lactate": 2.0,
        "glucose": 90.0
    },
    "urine": {
        "creatinine": 100.0,
        "protein": 3.0,
        "ph": 6.5
    }
}

# Test 2: High lactate in sweat (should be HIGH risk)
test2_high_lactate = {
    "saliva": {
        "cortisol": 3.5,
        "testosterone": 90.0,
        "iga": 150.0
    },
    "sweat": {
        "sodium": 25.0,
        "lactate": 8.0,  # Very high!
        "glucose": 90.0
    },
    "urine": {
        "creatinine": 100.0,
        "protein": 3.0,
        "ph": 6.5
    }
}

# Test 3: Everything elevated (should be CRITICAL risk)
test3_critical = {
    "saliva": {
        "cortisol": 15.0,  # Very high
        "testosterone": 200.0,  # Very high
        "iga": 500.0  # Very high
    },
    "sweat": {
        "sodium": 80.0,  # Very high
        "lactate": 10.0,  # Very high
        "glucose": 150.0  # High
    },
    "urine": {
        "creatinine": 300.0,  # Very high
        "protein": 50.0,  # Very high
        "ph": 8.5
    }
}

def test_prediction(test_name, data):
    print(f"\n{'='*60}")
    print(f"Testing: {test_name}")
    print(f"{'='*60}")
    
    try:
        response = requests.post(API_URL, json=data, headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Risk Score: {result['riskScore']}%")
            print(f"   Risk Level: {result['riskLevel']}")
            print(f"   Confidence: {result['confidence']}%")
            print(f"   Key Indicators: {result['keyIndicators'][:100]}...")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("\n🧪 Testing Prediction API with Different Inputs\n")
    
    test_prediction("Normal Values (Expected: LOW RISK)", test1_normal)
    test_prediction("High Lactate (Expected: HIGH RISK)", test2_high_lactate)
    test_prediction("All Elevated (Expected: CRITICAL RISK)", test3_critical)
    
    print(f"\n{'='*60}")
    print("✅ Test complete!")
    print(f"{'='*60}\n")
