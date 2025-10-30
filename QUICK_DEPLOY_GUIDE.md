# 🚀 Quick Start Guide for Crane Cloud Deployment

## Prerequisites
1. Create account at https://cranecloud.io
2. Install Git (if not already installed)
3. Push your code to GitHub/GitLab

## Step-by-Step Deployment

### 1️⃣ Push to Git (if not done yet)

```bash
cd "c:\Users\VICTOR KIBENGE\Desktop\Dep\dep"

# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Ready for Crane Cloud deployment"

# Add your remote repository
git remote add origin https://github.com/yourusername/hamstring-predictor.git

# Push
git push -u origin main
```

### 2️⃣ Deploy Backend

1. Go to https://cranecloud.io/dashboard
2. Click **"New App"**
3. Select **"From GitHub"** (or GitLab)
4. Choose your repository
5. Configure:
   - **App Name**: `hamstring-backend`
   - **Branch**: `main`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Port**: `5001`
   - **Resources**: 
     - RAM: 2GB (for PyTorch)
     - CPU: 1 core

6. **Environment Variables** - Click "Add Variable":
   ```
   SECRET_KEY = your-random-secret-key-123456
   DEBUG = False
   MODEL_PATH = models/gnode_model.pth
   SENDGRID_API_KEY = SG.your_actual_key
   SENDGRID_FROM_EMAIL = bulasiokibenge@gmail.com
   USE_SENDGRID = true
   CORS_ORIGINS = * (update after frontend deployment)
   ```

7. Click **"Deploy"**
8. Wait ~10 minutes (PyTorch is large)
9. Copy your backend URL: `https://hamstring-backend-xxxxx.cranecloud.io`

### 3️⃣ Deploy Frontend

1. In Crane Cloud dashboard, click **"New App"** again
2. Select **"From GitHub"**
3. Choose same repository
4. Configure:
   - **App Name**: `hamstring-frontend`
   - **Branch**: `main`
   - **Dockerfile Path**: `frontend/Dockerfile`
   - **Port**: `80`
   - **Resources**:
     - RAM: 512MB
     - CPU: 0.5 core

5. **Build Arguments**:
   ```
   REACT_APP_API_URL = https://hamstring-backend-xxxxx.cranecloud.io
   ```
   (Use the backend URL from step 2)

6. Click **"Deploy"**
7. Wait ~5 minutes
8. Your app is live! 🎉

### 4️⃣ Update Backend CORS

1. Go to backend app in Crane Cloud
2. Click **"Environment Variables"**
3. Edit `CORS_ORIGINS`:
   ```
   CORS_ORIGINS = https://hamstring-frontend-xxxxx.cranecloud.io
   ```
4. Click **"Restart App"**

### 5️⃣ Test Your App

Visit: `https://hamstring-frontend-xxxxx.cranecloud.io`

Test all features:
- ✅ Enter biomarker data
- ✅ Get risk prediction
- ✅ Download PDF
- ✅ Send email
- ✅ View history

---

## 💡 Costs (Estimated)

**Development Tier:**
- Backend: ~$15/month (2GB RAM, 1 CPU)
- Frontend: ~$5/month (512MB RAM)
- **Total: ~$20/month**

**Production Tier (with auto-scaling):**
- Backend: ~$40-80/month
- Frontend: ~$10-20/month
- **Total: ~$50-100/month**

---

## 🆘 Common Issues

### Backend Build Fails
**Problem**: PyTorch installation timeout
**Solution**: Contact Crane Cloud support to increase build timeout

### Frontend Can't Reach Backend
**Problem**: CORS error
**Solution**: 
1. Check backend `CORS_ORIGINS` has correct frontend URL
2. Restart backend app

### Model Not Loading
**Problem**: `gnode_model.pth` not found
**Solution**:
1. Make sure file is in git: `git add backend/models/gnode_model.pth`
2. Or use Crane Cloud persistent storage

---

## 📞 Need Help?

- Crane Cloud Docs: https://docs.cranecloud.io
- Email: support@cranecloud.io
- Your app is using: GNODE model (81.99% accuracy)

---

**That's it! Your AI-powered hamstring injury prediction app is now live on Crane Cloud! 🚀**
