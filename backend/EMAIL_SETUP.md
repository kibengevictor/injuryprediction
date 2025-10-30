# Email Configuration Instructions

## Gmail Setup (Recommended)

To enable email sending, follow these steps:

### 1. Enable 2-Step Verification
1. Go to https://myaccount.google.com/security
2. Click "2-Step Verification"
3. Follow the prompts to enable it

### 2. Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" as the app
3. Select "Windows Computer" or "Other" as the device
4. Click "Generate"
5. Copy the 16-character password (it will look like: xxxx xxxx xxxx xxxx)

### 3. Update .env file
Open `backend/.env` and update:

```
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
```

Replace:
- `your-email@gmail.com` with your actual Gmail address
- `xxxx xxxx xxxx xxxx` with the 16-character app password

### 4. Test the Configuration
Run the backend server and click "Email Results" in the app.

## Alternative: Other Email Providers

### Outlook/Hotmail
```
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USER=your-email@outlook.com
EMAIL_PASSWORD=your-password
```

### Yahoo Mail
```
EMAIL_HOST=smtp.mail.yahoo.com
EMAIL_PORT=587
EMAIL_USER=your-email@yahoo.com
EMAIL_PASSWORD=your-app-password
```

### Custom SMTP Server
```
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_USER=your-username
EMAIL_PASSWORD=your-password
```

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file to git/GitHub
- Use App Passwords, not regular passwords
- The `.env` file is already in `.gitignore`
- For production, use environment variables on your hosting platform

## Troubleshooting

**"Authentication failed" error:**
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2-Step Verification is enabled
- Check that EMAIL_USER and EMAIL_PASSWORD are correct in .env

**"Connection refused" error:**
- Check your firewall settings
- Verify EMAIL_HOST and EMAIL_PORT are correct
- Make sure you have internet connection

**Email not received:**
- Check spam/junk folder
- Verify the recipient email address is correct
- Wait a few minutes (email can be delayed)
