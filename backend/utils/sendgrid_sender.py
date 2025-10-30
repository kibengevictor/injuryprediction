"""
SendGrid email sender - Alternative to Gmail SMTP
Easier setup, no App Passwords needed
"""

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime


def send_with_sendgrid(to_email, recipient_name, risk_score, risk_level, confidence, key_indicators, recommendations):
    """Send email using SendGrid API"""
    
    SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
    FROM_EMAIL = os.getenv('SENDGRID_FROM_EMAIL', os.getenv('EMAIL_USER'))
    FROM_NAME = os.getenv('SENDGRID_FROM_NAME', 'Hamstring Injury Predictor')
    
    if not SENDGRID_API_KEY:
        print("\n⚠️  SendGrid not configured")
        print("   See backend/SENDGRID_SETUP.md for setup instructions\n")
        return False
    
    if not FROM_EMAIL:
        print("\n⚠️  No sender email configured (SENDGRID_FROM_EMAIL)\n")
        return False
    
    try:
        # Get risk emoji
        risk_emoji = {
            'LOW': '✅',
            'MODERATE': '⚠️',
            'HIGH': '🔴',
            'CRITICAL': '🚨'
        }.get(risk_level, '⚠️')
        
        # Create HTML email body
        html_content = f"""
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
                
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                    <p>© 2025 Hamstring Injury Risk Predictor | Powered by GNODE AI</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create SendGrid message
        message = Mail(
            from_email=Email(FROM_EMAIL, FROM_NAME),
            to_emails=To(to_email),
            subject=f'🏃 Hamstring Injury Risk Assessment - {risk_level} Risk',
            html_content=Content("text/html", html_content)
        )
        
        # Send email
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Email sent successfully via SendGrid to {to_email}")
            print(f"   Status Code: {response.status_code}")
            return True
        else:
            print(f"❌ SendGrid returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ SendGrid error: {e}")
        return False
