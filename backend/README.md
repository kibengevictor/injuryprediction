# Hamstring Injury Risk Predictor - Backend API

Flask-based REST API for hamstring injury risk prediction using GNODE (Graph Neural ODE) model.

## 🚀 Features

- **Intelligent Tissue Selection**: Automatically determines optimal tissue type (saliva/sweat/urine) based on elevation scores and clinical relevance
- **Metabolite Prioritization**: Selects primary biomarker using importance weighting and deviation analysis
- **GNODE Model Integration**: Uses Graph Neural ODE for accurate injury risk prediction
- **Comprehensive Recommendations**: Generates personalized action plans based on risk level
- **RESTful API**: Clean endpoints with proper error handling and validation

## 📋 Requirements

- Python 3.8+
- PyTorch 2.0+
- Flask 3.0+
- See `requirements.txt` for full list

## 🛠️ Installation

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create `.env` file:
```bash
copy .env.example .env
```

6. Edit `.env` with your configuration

## 🏃 Running the Server

### Development Mode
```bash
python app.py
```

The server will start on `http://localhost:5000`

### Production Mode
```bash
# Using Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Waitress (Windows)
pip install waitress
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "model": "GNODE",
  "version": "1.0.0"
}
```

### Predict Injury Risk
```http
POST /api/predict
Content-Type: application/json
```

Request Body:
```json
{
  "saliva": {
    "cortisol": 5.2,
    "testosterone": 85.0,
    "iga": 150.0
  },
  "sweat": {
    "sodium": 1.5,
    "lactate": 3.2,
    "glucose": 95.0
  },
  "urine": {
    "creatinine": 120.0,
    "protein": 5.0,
    "ph": 6.5
  }
}
```

Response:
```json
{
  "riskScore": 51,
  "riskLevel": "HIGH",
  "confidence": 87,
  "keyIndicators": "Analysis of your sweat biomarkers shows elevated lactate levels...",
  "recommendations": {
    "immediate": [
      "Rest hamstring muscles for 24-48 hours",
      "Apply ice/compression if pain present",
      ...
    ],
    "followUp": [
      "Re-test biomarkers within 3-5 days",
      ...
    ],
    "monitoring": [
      "Monitor for pain, tightness, or reduced flexibility",
      ...
    ]
  }
}
```

### Get Metabolite Database
```http
GET /api/metabolites
```

Returns complete metabolite database with molecular weights, normal ranges, and importance scores.

## 🧪 Testing

Test the API using curl:

```bash
# Health check
curl http://localhost:5000/api/health

# Prediction with sample data
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sweat": {
      "lactate": 3.5,
      "sodium": 1.8,
      "glucose": 110
    }
  }'
```

Or use the provided test script:
```bash
python test_api.py
```

## 📁 Project Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── models/                     # Model files directory
│   └── gnode_model.pt         # Trained GNODE model (add yours)
└── utils/                      # Utility modules
    ├── biomarker_processor.py # Tissue selection & feature prep
    ├── metabolite_database.py # Biomarker database
    ├── model_loader.py        # Model loading & inference
    └── recommendation_generator.py # Recommendation logic
```

## 🔧 Configuration

### Environment Variables (`.env`)

- `SECRET_KEY`: Flask secret key for session management
- `DEBUG`: Enable debug mode (True/False)
- `CORS_ORIGINS`: Allowed origins for CORS (comma-separated)
- `MODEL_PATH`: Path to trained GNODE model file

### Model File

Place your trained GNODE model at `models/gnode_model.pt`. The model should be a PyTorch model compatible with the feature input format.

**Note**: If no model file is found, the system will use mock predictions for testing.

## 🧠 How It Works

### 1. Tissue Selection Algorithm
```python
score = elevation_score + clinical_relevance + data_completeness
# elevation_score: 0-2 (deviation from normal)
# clinical_relevance: sweat=1.0, urine=0.7, saliva=0.5
# data_completeness: 0-0.3
```

### 2. Metabolite Selection
```python
score = importance * deviation
# importance: 0-1 (lactate=1.0 highest)
# deviation: 0-2 (distance from normal range)
```

### 3. Feature Encoding
- **Molecular Weight**: Continuous value in Daltons
- **Tissue Type**: One-hot encoded (drop_first)
  - Saliva: [0, 0]
  - Sweat: [1, 0]
  - Urine: [0, 1]
- **EMG Features**: Default to 0.0 if not provided

### 4. Risk Classification
- **LOW**: 0-24%
- **MODERATE**: 25-49%
- **HIGH**: 50-74%
- **CRITICAL**: 75-100%

## 🐛 Troubleshooting

### CORS Errors
Ensure frontend URL is in `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=http://localhost:3000
```

### Model Not Loading
Check that:
1. Model file exists at `models/gnode_model.pt`
2. Model is compatible with PyTorch version
3. PATH in `.env` is correct

### Import Errors
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## 📈 Performance

- Average response time: <100ms (without model)
- Average response time: <500ms (with model)
- Concurrent requests: Supports multiple simultaneous predictions

## 🔒 Security Considerations

- Enable HTTPS in production
- Set strong `SECRET_KEY`
- Disable `DEBUG` mode in production
- Implement rate limiting
- Add authentication for production use
- Validate and sanitize all inputs

## 📝 License

Copyright © 2025 Hamstring Injury Predictor

## 🤝 Contributing

This is a private project. Contact the development team for contribution guidelines.

## 📧 Support

For issues or questions, contact the development team.
