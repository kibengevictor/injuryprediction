"""
Email utility for sending assessment results
Supports both SendGrid (recommended) and Gmail SMTP
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os


def send_results_email(to_email, recipient_name, risk_score, risk_level, confidence, key_indicators, recommendations):
    """
    Send assessment results via email.
    
    Tries SendGrid first (if configured), falls back to SMTP
    """
    
    # Check if SendGrid is configured
    USE_SENDGRID = os.getenv('USE_SENDGRID', 'true').lower() == 'true'
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    
    # Try SendGrid first if configured
    if USE_SENDGRID and SENDGRID_API_KEY:
        try:
            from .sendgrid_sender import send_with_sendgrid
            result = send_with_sendgrid(to_email, recipient_name, risk_score, risk_level, confidence, key_indicators, recommendations)
            if result:
                return True
            print("⚠️  SendGrid failed, trying SMTP...")
        except Exception as e:
            print(f"⚠️  SendGrid error: {e}, trying SMTP...")
    
    # Fall back to SMTP (Gmail)
    return send_with_smtp(to_email, recipient_name, risk_score, risk_level, confidence, key_indicators, recommendations)


def send_with_smtp(to_email, recipient_name, risk_score, risk_level, confidence, key_indicators, recommendations):
    """
    Send assessment results via email.
    
    Note: Configure SMTP settings in .env file:
    - EMAIL_HOST (default: smtp.gmail.com)
    - EMAIL_PORT (default: 587)
    - EMAIL_USER (your email)
    - EMAIL_PASSWORD (your app password)
    
    For Gmail: Use App Password from https://myaccount.google.com/apppasswords
    """
    
    # Email configuration from environment variables
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USER = os.getenv('EMAIL_USER')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # Check if email is configured
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("\n" + "="*70)
        print("⚠️  EMAIL NOT CONFIGURED")
        print("="*70)
        print("To enable email sending:")
        print("1. Open backend/.env file")
        print("2. Set EMAIL_USER to your Gmail address")
        print("3. Set EMAIL_PASSWORD to your Gmail App Password")
        print("4. See backend/EMAIL_SETUP.md for detailed instructions")
        print("="*70)
        print(f"\n📧 Email WOULD be sent to: {to_email}")
        print(f"   Recipient: {recipient_name}")
        print(f"   Risk Score: {risk_score}% ({risk_level})")
        print(f"   Confidence: {confidence}%\n")
        # Return False to indicate email wasn't sent
        return False
    
    # Validate email configuration
    if EMAIL_USER == 'your-email@gmail.com' or EMAIL_PASSWORD == 'your-app-specific-password':
        print("\n⚠️  Please update EMAIL_USER and EMAIL_PASSWORD in backend/.env file")
        print("   See backend/EMAIL_SETUP.md for instructions\n")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = EMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = f'🏃 Hamstring Injury Risk Assessment - {risk_level} Risk'
        
        # Get risk emoji
        risk_emoji = {
            'LOW': '✅',
            'MODERATE': '⚠️',
            'HIGH': '🔴',
            'CRITICAL': '🚨'
        }.get(risk_level, '⚠️')
        
        # Create HTML email body
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border-radius: 0 0 10px 10px;
                }}
                .risk-box {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 20px 0;
                    border-left: 5px solid #667eea;
                }}
                .risk-score {{
                    font-size: 48px;
                    font-weight: bold;
                    color: #667eea;
                    margin: 10px 0;
                }}
                .section {{
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    margin: 15px 0;
                }}
                .section h3 {{
                    color: #667eea;
                    margin-top: 0;
                }}
                .recommendation-list {{
                    list-style-type: none;
                    padding-left: 0;
                }}
                .recommendation-list li {{
                    padding: 8px 0;
                    padding-left: 25px;
                    position: relative;
                }}
                .recommendation-list li:before {{
                    content: "▸";
                    position: absolute;
                    left: 0;
                    color: #667eea;
                    font-weight: bold;
                }}
                .footer {{
                    text-align: center;
                    color: #777;
                    font-size: 12px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🏃 Hamstring Injury Risk Assessment</h1>
                <p>Powered by GNODE AI</p>
            </div>
            
            <div class="content">
                <p>Dear {recipient_name},</p>
                
                <p>Your hamstring injury risk assessment has been completed. Here are your results:</p>
                
                <div class="risk-box">
                    <h2 style="margin-top: 0;">Your Risk Assessment</h2>
                    <div class="risk-score">{risk_emoji} {risk_score}%</div>
                    <p style="font-size: 20px; font-weight: bold; color: #333;">Risk Level: {risk_level}</p>
                    <p style="color: #666;">Model Confidence: {confidence}%</p>
                </div>
                
                <div class="section">
                    <h3>📊 Key Indicators</h3>
                    <p>{key_indicators}</p>
                </div>
                
                <div class="section">
                    <h3>⚠️ Immediate Actions</h3>
                    <ul class="recommendation-list">
                        {''.join(f'<li>{item}</li>' for item in recommendations['immediate'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h3>📅 Follow-Up (Within 3-5 Days)</h3>
                    <ul class="recommendation-list">
                        {''.join(f'<li>{item}</li>' for item in recommendations['followUp'])}
                    </ul>
                </div>
                
                <div class="section">
                    <h3>📈 Ongoing Monitoring</h3>
                    <ul class="recommendation-list">
                        {''.join(f'<li>{item}</li>' for item in recommendations['monitoring'])}
                    </ul>
                </div>
                
                <p style="margin-top: 30px;">
                    <strong>Important:</strong> This assessment is for informational purposes. 
                    Please consult with qualified healthcare professionals for medical advice and treatment decisions.
                </p>
                
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>© 2025 Hamstring Injury Risk Predictor | Powered by GNODE AI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        msg.attach(html_part)
        
        # Send email
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False
