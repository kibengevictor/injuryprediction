# 🚀 Crane Cloud Deployment Guide

## Overview
This guide will help you deploy the Hamstring Injury Prediction App to Crane Cloud.

---

## 📋 Prerequisites

1. **Crane Cloud Account**
   - Sign up at: https://cranecloud.io
   - Verify your email
   - Add payment method (if required)

2. **Git Repository**
   - Push your code to GitHub/GitLab
   - Make sure `.dockerignore` files are committed
   - Ensure `Dockerfile` files are in both frontend and backend folders

3. **Environment Variables**
   - Have your SendGrid API key ready
   - Note down any other secrets

---

## 🔧 Backend Deployment (Flask API)

### Step 1: Prepare Backend

1. **Update `app.py` for production**
   - Host should be `0.0.0.0`
   - Port should be `5001` (or use environment variable)
   - Already configured ✅

2. **Verify requirements.txt includes all dependencies**
   ```bash
   cd backend
   pip freeze > requirements.txt
   ```

### Step 2: Deploy to Crane Cloud

1. **Login to Crane Cloud Dashboard**
   - Go to https://cranecloud.io/dashboard

2. **Create New App**
   - Click "Create New App"
   - Choose "Docker" deployment
   - Name: `hamstring-backend` (or your preferred name)

3. **Connect Repository**
   - Connect your GitHub/GitLab account
   - Select your repository
   - Branch: `main` (or `master`)
   - Dockerfile path: `backend/Dockerfile`

4. **Configure Environment Variables**
   ```
   SENDGRID_API_KEY=SG.your_api_key_here
   SENDGRID_FROM_EMAIL=bulasiokibenge@gmail.com
   SENDGRID_FROM_NAME=Hamstring Injury Predictor
   USE_SENDGRID=true
   SECRET_KEY=your-production-secret-key-here
   DEBUG=False
   MODEL_PATH=models/gnode_model.pth
   CORS_ORIGINS=https://your-frontend-url.cranecloud.io
   ```

5. **Set Resources**
   - RAM: 1GB (minimum, 2GB recommended for PyTorch)
   - CPU: 0.5 cores (1 core recommended)
   - Storage: 1GB

6. **Deploy**
   - Click "Deploy"
   - Wait for build to complete (~5-10 minutes for PyTorch)
   - Note your backend URL: `https://hamstring-backend-xxxxx.cranecloud.io`

### Step 3: Upload Model File

**Important:** The `gnode_model.pth` file (13 KB) needs to be in the container.

**Option A: Include in Git (Recommended for small model)**
```bash
cd backend/models
git add gnode_model.pth
git commit -m "Add trained GNODE model"
git push
```

**Option B: Use Crane Cloud Persistent Storage**
1. Create a volume in Crane Cloud dashboard
2. Mount it to `/app/models`
3. Upload `gnode_model.pth` via dashboard or CLI

---

## 🎨 Frontend Deployment (React App)

### Step 1: Update API URL

1. **Create production environment file**
   
   Create `frontend/.env.production`:
   ```
   REACT_APP_API_URL=https://hamstring-backend-xxxxx.cranecloud.io
   ```

2. **Update `api.js` to use environment variable**
   
   Already configured ✅ (uses `process.env.REACT_APP_API_URL`)

### Step 2: Deploy to Crane Cloud

1. **Create New App**
   - Name: `hamstring-frontend`
   - Deployment type: Docker
   - Repository: Same as backend
   - Dockerfile path: `frontend/Dockerfile`

2. **Set Build Arguments** (if needed)
   ```
   REACT_APP_API_URL=https://hamstring-backend-xxxxx.cranecloud.io
   ```

3. **Set Resources**
   - RAM: 512MB
   - CPU: 0.25 cores
   - Storage: 500MB

4. **Deploy**
   - Click "Deploy"
   - Wait for build (~3-5 minutes)
   - Your app will be available at: `https://hamstring-frontend-xxxxx.cranecloud.io`

---

## 🔐 Post-Deployment Configuration

### 1. Update CORS

Update backend environment variable:
```
CORS_ORIGINS=https://hamstring-frontend-xxxxx.cranecloud.io
```

Redeploy backend for changes to take effect.

### 2. Test the Application

1. **Test Backend API**
   ```bash
   curl https://hamstring-backend-xxxxx.cranecloud.io/api/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "model": "GNODE",
     "version": "1.0.0"
   }
   ```

2. **Test Frontend**
   - Open `https://hamstring-frontend-xxxxx.cranecloud.io`
   - Complete a full assessment
   - Check PDF download
   - Test email functionality

### 3. Monitor Logs

**Backend logs:**
```bash
crane logs hamstring-backend --follow
```

**Frontend logs:**
```bash
crane logs hamstring-frontend --follow
```

---

## 📊 Scaling & Performance

### Auto-scaling Configuration

**Backend:**
- Min instances: 1
- Max instances: 3
- Scale trigger: CPU > 70%

**Frontend:**
- Min instances: 1
- Max instances: 2
- Scale trigger: CPU > 80%

### Cost Optimization

**Development/Testing:**
- Backend: 512MB RAM, 0.25 CPU
- Frontend: 256MB RAM, 0.25 CPU
- Estimated: $10-20/month

**Production (with traffic):**
- Backend: 2GB RAM, 1 CPU
- Frontend: 512MB RAM, 0.5 CPU
- Estimated: $50-100/month

---

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `DEBUG=False` in production
- [ ] Use HTTPS only (Crane Cloud provides free SSL)
- [ ] Secure environment variables (never commit to Git)
- [ ] Enable rate limiting (optional)
- [ ] Set up monitoring/alerting
- [ ] Regular backups of model file

---

## 🐛 Troubleshooting

### Backend Won't Start

1. **Check logs:**
   ```bash
   crane logs hamstring-backend --tail 100
   ```

2. **Common issues:**
   - PyTorch installation timeout → Increase build time limit
   - Model file not found → Check model path or upload file
   - Out of memory → Increase RAM allocation

### Frontend Can't Reach Backend

1. **Check CORS configuration**
   - Verify `CORS_ORIGINS` includes frontend URL
   - Check backend logs for CORS errors

2. **Check API URL**
   - Verify `.env.production` has correct backend URL
   - Rebuild frontend after changing environment variables

### Model Predictions Failing

1. **Check model file exists:**
   ```bash
   crane exec hamstring-backend -- ls -lh models/
   ```

2. **Verify PyTorch installation:**
   ```bash
   crane exec hamstring-backend -- python -c "import torch; print(torch.__version__)"
   ```

---

## 🚀 Alternative: Quick Deploy Script

Create `deploy.sh` in project root:

```bash
#!/bin/bash

echo "🚀 Deploying Hamstring Injury Predictor to Crane Cloud"

# Backend
echo "📦 Deploying Backend..."
cd backend
crane deploy --app hamstring-backend \
  --dockerfile Dockerfile \
  --env-file .env.production

# Frontend  
echo "🎨 Deploying Frontend..."
cd ../frontend
crane deploy --app hamstring-frontend \
  --dockerfile Dockerfile \
  --build-arg REACT_APP_API_URL=$BACKEND_URL

echo "✅ Deployment complete!"
echo "Backend: https://hamstring-backend-xxxxx.cranecloud.io"
echo "Frontend: https://hamstring-frontend-xxxxx.cranecloud.io"
```

---

## 📝 CI/CD Setup (Optional)

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Crane Cloud

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Backend
        run: |
          crane deploy --app hamstring-backend \
            --dockerfile backend/Dockerfile
        env:
          CRANE_API_KEY: ${{ secrets.CRANE_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: deploy-backend
    steps:
      - uses: actions/checkout@v2
      - name: Deploy Frontend
        run: |
          crane deploy --app hamstring-frontend \
            --dockerfile frontend/Dockerfile
        env:
          CRANE_API_KEY: ${{ secrets.CRANE_API_KEY }}
```

---

## 📞 Support

- **Crane Cloud Docs:** https://docs.cranecloud.io
- **Crane Cloud Support:** support@cranecloud.io
- **Community Slack:** cranecloud.slack.com

---

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code pushed to GitHub/GitLab
- [ ] Dockerfiles created
- [ ] Environment variables documented
- [ ] Model file ready (gnode_model.pth)
- [ ] SendGrid configured and tested

### Backend Deployment
- [ ] App created on Crane Cloud
- [ ] Repository connected
- [ ] Environment variables set
- [ ] Model file uploaded
- [ ] Health endpoint tested
- [ ] Logs checked

### Frontend Deployment
- [ ] App created on Crane Cloud
- [ ] API URL configured
- [ ] Build successful
- [ ] CORS configured on backend
- [ ] Full user flow tested

### Post-Deployment
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Documentation updated with URLs
- [ ] Team notified

---

**Your app is now live! 🎉**

Share your URL: `https://hamstring-frontend-xxxxx.cranecloud.io`

---

*Last Updated: October 30, 2025*
*Deployment Platform: Crane Cloud*
