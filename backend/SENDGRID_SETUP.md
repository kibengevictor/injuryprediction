# SendGrid Email Setup (EASIEST METHOD)

## Why SendGrid?
- ✅ **No App Passwords needed**
- ✅ **Free tier: 100 emails/day**
- ✅ **Works with any email account**
- ✅ **More reliable delivery**
- ✅ **Simple API key setup**

## Setup Steps (5 minutes):

### 1. Create Free SendGrid Account
1. Go to https://signup.sendgrid.com/
2. Sign up with your email
3. Verify your email address
4. Complete the account setup

### 2. Get API Key
1. Log in to SendGrid Dashboard
2. Go to **Settings** → **API Keys** (https://app.sendgrid.com/settings/api_keys)
3. Click **"Create API Key"**
4. Name it: `Hamstring Injury App`
5. Choose **"Full Access"** permissions
6. Click **"Create & View"**
7. **COPY the API key** (starts with `SG.`...) - you won't see it again!

### 3. Update `.env` file
Open `backend/.env` and add:

```env
# SendGrid Configuration
USE_SENDGRID=true
SENDGRID_API_KEY=SG.your_api_key_here
SENDGRID_FROM_EMAIL=your-email@gmail.com
SENDGRID_FROM_NAME=Hamstring Injury Predictor
```

Replace:
- `SG.your_api_key_here` with your actual SendGrid API key
- `your-email@gmail.com` with the email you want to send FROM

### 4. Verify Sender Email (Required for Free Tier)
1. Go to **Settings** → **Sender Authentication** → **Single Sender Verification**
2. Click **"Create New Sender"**
3. Fill in your details (use your Gmail)
4. Check your email and click verification link
5. **IMPORTANT:** Use this verified email in `SENDGRID_FROM_EMAIL`

### 5. Restart Flask Server
Stop and restart your Flask backend server.

### 6. Test!
Click "Email Results" in your app and send a test email!

## Alternative: Gmail SMTP (If App Passwords Work)

If you can enable 2-Step Verification and get App Passwords:

```env
# Gmail SMTP Configuration
USE_SENDGRID=false
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
```

## Troubleshooting

**"Authentication failed" with SendGrid:**
- Verify your API key is correct (starts with `SG.`)
- Make sure no extra spaces in `.env` file

**"Sender email not verified":**
- You must verify sender email in SendGrid dashboard first
- Check spam folder for verification email

**Email not received:**
- Check spam/junk folder
- Verify recipient email is correct
- Check SendGrid dashboard for delivery logs

## Which Method to Use?

| Method | Pros | Cons |
|--------|------|------|
| **SendGrid** ✅ | Easy setup, no 2FA needed, reliable | Requires account signup |
| **Gmail SMTP** | Direct, no 3rd party | Needs 2FA + App Password |

**Recommendation:** Use SendGrid for easiest setup!
