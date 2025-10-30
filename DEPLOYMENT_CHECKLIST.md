# ✅ Pre-Deployment Checklist

## Files Created ✅

- [x] `backend/Dockerfile` - Backend container configuration
- [x] `backend/.dockerignore` - Files to exclude from backend build
- [x] `backend/.env.production.example` - Production environment template
- [x] `frontend/Dockerfile` - Frontend container configuration  
- [x] `frontend/nginx.conf` - Nginx web server configuration
- [x] `frontend/.dockerignore` - Files to exclude from frontend build
- [x] `frontend/.env.production` - Frontend production environment
- [x] `.gitignore` - Git ignore rules
- [x] `CRANE_CLOUD_DEPLOYMENT.md` - Detailed deployment guide
- [x] `QUICK_DEPLOY_GUIDE.md` - Quick start guide

## Before You Deploy

### 1. Verify Files Exist
```bash
# Check backend files
ls backend/Dockerfile
ls backend/models/gnode_model.pth

# Check frontend files  
ls frontend/Dockerfile
ls frontend/nginx.conf
```

### 2. Test Locally One More Time
```bash
# Backend (Terminal 1)
cd backend
python app.py

# Frontend (Terminal 2)
cd frontend
npm start

# Visit http://localhost:3000 and test everything
```

### 3. Prepare Git Repository

#### Option A: New Repository
```bash
cd "c:\Users\VICTOR KIBENGE\Desktop\Dep\dep"
git init
git add .
git commit -m "Initial commit - Hamstring Injury Predictor with GNODE model"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/hamstring-predictor.git
git push -u origin main
```

#### Option B: Existing Repository
```bash
cd "c:\Users\VICTOR KIBENGE\Desktop\Dep\dep"
git add .
git commit -m "Add Crane Cloud deployment files"
git push
```

### 4. Important: Model File

Make sure `gnode_model.pth` is included:
```bash
# Remove it from .gitignore (already done in the .gitignore file)
# Verify it's tracked
git add backend/models/gnode_model.pth -f
git commit -m "Add trained GNODE model"
```

**File size check:**
- Your model: ~13 KB ✅ (small enough for Git)
- If it was larger (>100MB), you'd need Git LFS

### 5. Environment Variables Ready

Create `backend/.env.production` (copy from example):
```bash
cp backend/.env.production.example backend/.env.production
# Edit and add your real values
```

**DO NOT commit `.env.production`** - it's in `.gitignore`

You'll add these values in Crane Cloud dashboard instead.

## Deployment Steps (Quick Reference)

### Step 1: Deploy Backend
1. Crane Cloud Dashboard → New App
2. Connect GitHub repo
3. Dockerfile: `backend/Dockerfile`
4. Add environment variables
5. RAM: 2GB, CPU: 1 core
6. Deploy (wait ~10 min)
7. **Copy backend URL**

### Step 2: Update Frontend Config
Update `frontend/.env.production`:
```
REACT_APP_API_URL=<your-backend-url-here>
```

Commit and push:
```bash
git add frontend/.env.production
git commit -m "Update API URL for production"
git push
```

### Step 3: Deploy Frontend
1. Crane Cloud Dashboard → New App
2. Connect same GitHub repo
3. Dockerfile: `frontend/Dockerfile`
4. Build arg: `REACT_APP_API_URL=<backend-url>`
5. RAM: 512MB, CPU: 0.5 core
6. Deploy (wait ~5 min)
7. **Copy frontend URL**

### Step 4: Update Backend CORS
1. Backend app → Environment Variables
2. Update `CORS_ORIGINS=<frontend-url>`
3. Restart backend

### Step 5: Test Everything! 🎉
Visit your frontend URL and test:
- ✅ Form submission
- ✅ Risk prediction
- ✅ PDF download
- ✅ Email sending
- ✅ History viewing

## Estimated Costs

**Crane Cloud Pricing:**
- Backend (2GB RAM, 1 CPU): ~$15-20/month
- Frontend (512MB RAM): ~$5/month
- **Total: ~$20-25/month** for production

**Free tier available?** Check Crane Cloud docs for current offers.

## Next Steps After Deployment

1. **Custom Domain** (Optional)
   - Buy domain (e.g., hamstringai.com)
   - Point to Crane Cloud URL
   - Add SSL certificate

2. **Monitoring**
   - Set up health check alerts
   - Monitor error logs
   - Track usage metrics

3. **Backups**
   - Export model file regularly
   - Backup environment variables
   - Document configuration

4. **Documentation**
   - Update README with live URLs
   - Create user guide
   - Add API documentation

## Troubleshooting

### Build Fails
- Check Dockerfile syntax
- Verify all files are committed
- Check build logs in Crane Cloud

### App Crashes
- Check logs: `crane logs <app-name>`
- Verify environment variables
- Check resource limits (RAM/CPU)

### Can't Connect Frontend to Backend
- Verify CORS settings
- Check API URL in frontend
- Test backend health endpoint directly

## Support Resources

- **Crane Cloud Docs**: https://docs.cranecloud.io
- **Crane Cloud Support**: support@cranecloud.io
- **Your Deployment Guides**: 
  - `CRANE_CLOUD_DEPLOYMENT.md` (detailed)
  - `QUICK_DEPLOY_GUIDE.md` (quick start)

---

## Ready to Deploy? 🚀

Follow `QUICK_DEPLOY_GUIDE.md` for step-by-step instructions!

**Good luck! Your AI-powered hamstring injury predictor will be live soon! 🎯**
