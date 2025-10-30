"""
Test script for the Flask API
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_prediction():
    """Test prediction endpoint with sample data"""
    print("\n=== Testing Prediction ===")
    
    # Sample biomarker data
    data = {
        "saliva": {
            "cortisol": 8.5,
            "testosterone": 95.0,
            "iga": 180.0
        },
        "sweat": {
            "sodium": 1.8,
            "lactate": 3.5,
            "glucose": 110.0
        },
        "urine": {
            "creatinine": 150.0,
            "protein": 8.0,
            "ph": 6.2
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_high_risk_scenario():
    """Test with high-risk biomarker values"""
    print("\n=== Testing High Risk Scenario ===")
    
    # High lactate = high risk
    data = {
        "sweat": {
            "lactate": 3.8,
            "sodium": 2.5,
            "glucose": 140.0
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print(f"Risk Score: {result.get('riskScore')}%")
        print(f"Risk Level: {result.get('riskLevel')}")
        print(f"Confidence: {result.get('confidence')}%")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_invalid_data():
    """Test with invalid data"""
    print("\n=== Testing Invalid Data ===")
    
    data = {
        "invalid_tissue": {
            "invalid_biomarker": 123
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/predict",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return response.status_code == 400  # Should return error
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_metabolites_endpoint():
    """Test metabolites database endpoint"""
    print("\n=== Testing Metabolites Endpoint ===")
    try:
        response = requests.get(f"{BASE_URL}/metabolites")
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Tissues available: {list(data.keys())}")
        print(f"Sweat biomarkers: {list(data.get('sweat', {}).keys())}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Flask API Test Suite")
    print("=" * 60)
    print("\nMake sure the Flask server is running on http://localhost:5000")
    print("Start it with: python app.py")
    input("\nPress Enter to continue...")
    
    results = {
        "Health Check": test_health_check(),
        "Normal Prediction": test_prediction(),
        "High Risk Scenario": test_high_risk_scenario(),
        "Invalid Data": test_invalid_data(),
        "Metabolites Endpoint": test_metabolites_endpoint()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
