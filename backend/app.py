"""
Flask backend for Hamstring Injury Risk Predictor
Main application entry point
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from utils.biomarker_processor import (
    validate_biomarker_data,
    prepare_model_features
)
from utils.model_loader import predict_injury_risk
from utils.recommendation_generator import (
    generate_recommendations,
    get_key_indicators_text
)
import traceback


def create_app(config_class=Config):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'model': 'GNODE',
            'version': '1.0.0'
        })
    
    @app.route('/api/predict', methods=['POST'])
    def predict():
        """
        Main prediction endpoint.
        
        Expected input:
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
        
        Returns:
        {
            "riskScore": 51,
            "riskLevel": "HIGH",
            "confidence": 87,
            "keyIndicators": "...",
            "recommendations": {
                "immediate": [...],
                "followUp": [...],
                "monitoring": [...]
            }
        }
        """
        try:
            # Get request data
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'error': 'No data provided',
                    'message': 'Request body must contain biomarker data'
                }), 400
            
            # Validate biomarker data
            is_valid, errors = validate_biomarker_data(data)
            
            if not is_valid:
                return jsonify({
                    'error': 'Invalid biomarker data',
                    'details': errors
                }), 400
            
            # Prepare features for model
            try:
                model_features, metadata = prepare_model_features(data)
            except ValueError as e:
                return jsonify({
                    'error': 'Feature preparation failed',
                    'message': str(e)
                }), 400
            
            # Make prediction
            # Pass metadata to model for better mock predictions
            model_features_with_metadata = {**model_features, 'metadata': metadata}
            risk_score = predict_injury_risk(model_features_with_metadata)
            risk_score = round(risk_score, 1)
            
            # Determine risk level
            if risk_score < 25:
                risk_level = 'LOW'
            elif risk_score < 50:
                risk_level = 'MODERATE'
            elif risk_score < 75:
                risk_level = 'HIGH'
            else:
                risk_level = 'CRITICAL'
            
            # Generate recommendations
            recommendations = generate_recommendations(risk_score, metadata)
            
            # Generate key indicators text
            key_indicators = get_key_indicators_text(metadata)
            
            # Calculate confidence (mock for now - can be improved with model uncertainty)
            confidence = calculate_confidence(metadata, risk_score)
            
            # Prepare response
            response = {
                'riskScore': int(risk_score),
                'riskLevel': risk_level,
                'confidence': confidence,
                'keyIndicators': key_indicators,
                'recommendations': recommendations
            }
            
            return jsonify(response), 200
            
        except Exception as e:
            # Log error
            print(f"Error in prediction endpoint: {e}")
            print(traceback.format_exc())
            
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred during prediction',
                'details': str(e) if app.config['DEBUG'] else None
            }), 500
    
    @app.route('/api/metabolites', methods=['GET'])
    def get_metabolites():
        """Get available metabolites and their info"""
        from utils.metabolite_database import METABOLITE_DATABASE
        return jsonify(METABOLITE_DATABASE)
    
    @app.route('/api/email-results', methods=['POST'])
    def email_results():
        """Send assessment results via email"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'error': 'No data provided',
                    'message': 'Request body must contain email data'
                }), 400
            
            email = data.get('email')
            recipient_name = data.get('recipientName')
            results = data.get('results')
            
            if not email or not recipient_name or not results:
                return jsonify({
                    'error': 'Missing required fields',
                    'message': 'email, recipientName, and results are required'
                }), 400
            
            # Import email utility
            from utils.email_sender import send_results_email
            
            # Send email
            success = send_results_email(
                to_email=email,
                recipient_name=recipient_name,
                risk_score=results['riskScore'],
                risk_level=results['riskLevel'],
                confidence=results['confidence'],
                key_indicators=results['keyIndicators'],
                recommendations=results['recommendations']
            )
            
            if success:
                return jsonify({
                    'status': 'success',
                    'message': f'Email sent successfully to {email}'
                }), 200
            else:
                return jsonify({
                    'error': 'Email sending failed',
                    'message': 'Unable to send email. Please check configuration.'
                }), 500
                
        except Exception as e:
            print(f"Error in email endpoint: {e}")
            print(traceback.format_exc())
            
            return jsonify({
                'error': 'Internal server error',
                'message': 'An unexpected error occurred while sending email',
                'details': str(e) if app.config['DEBUG'] else None
            }), 500
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested endpoint does not exist'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred'
        }), 500
    
    return app


def calculate_confidence(metadata, risk_score):
    """
    Calculate confidence score based on data quality and model certainty.
    Returns confidence percentage (0-100)
    """
    # Base confidence
    confidence = 70
    
    # Boost confidence if primary tissue is sweat (most relevant)
    if metadata.get('primary_tissue') == 'sweat':
        confidence += 10
    elif metadata.get('primary_tissue') == 'urine':
        confidence += 5
    
    # Boost confidence if primary biomarker is lactate (most important)
    if metadata.get('primary_biomarker') == 'lactate':
        confidence += 10
    
    # Boost if multiple tissues have data
    tissue_scores = metadata.get('tissue_scores', {})
    if len(tissue_scores) >= 2:
        confidence += 5
    if len(tissue_scores) >= 3:
        confidence += 2
    
    # Reduce confidence for extreme risk scores (less certain)
    if risk_score < 10 or risk_score > 90:
        confidence -= 5
    
    # Cap confidence
    confidence = max(60, min(95, confidence))
    
    return confidence


if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Hamstring Injury Risk Predictor API")
    print(f"   Model: {app.config['MODEL_TYPE']}")
    print(f"   Debug: {app.config['DEBUG']}")
    print(f"   CORS Origins: {app.config['CORS_ORIGINS']}")
    print("\n   Available endpoints:")
    print("   - GET  /api/health")
    print("   - POST /api/predict")
    print("   - GET  /api/metabolites")
    print("   - POST /api/email-results")
    print()
    
    # Disable reloader when using PyTorch (prevents Windows DLL conflicts)
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=app.config['DEBUG'],
        use_reloader=False  # Fixes PyTorch + Flask reloader conflict on Windows
    )
