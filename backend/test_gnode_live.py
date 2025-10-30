"""Test if GNODE model is being used by the live API"""
import requests
import json

url = "http://127.0.0.1:5001/api/predict"
payload = {
    "sweat": {
        "sodium": 1.5,
        "lactate": 2.5
    },
    "urine": {
        "creatinine": 150
    }
}

print("🧪 Testing Live API - Check Flask logs for model type\n")
print(f"Sending request to: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}\n")

response = requests.post(url, json=payload)
print(f"✅ Response Status: {response.status_code}")
print(f"Response Data:")
print(json.dumps(response.json(), indent=2))
print("\n💡 Check the Flask server terminal for '✅ GNODE prediction' or '⚠️ Using mock prediction'")
