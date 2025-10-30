# 🐳 Docker & Kubernetes Guide

## Local Development with Docker Compose

### Quick Start
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Individual Services
```bash
# Backend only
docker-compose up -d backend

# Frontend only
docker-compose up -d frontend

# Rebuild after changes
docker-compose up -d --build
```

### Environment Variables
Create a `.env` file in the root directory:
```bash
# SendGrid
SENDGRID_API_KEY=your_key_here
SENDGRID_FROM_EMAIL=your_email@example.com

# Production URLs (for docker-compose.prod.yml)
BACKEND_URL=https://backend.yourdomain.com
FRONTEND_URL=https://yourdomain.com
SECRET_KEY=your-production-secret
```

## Production Deployment

### Using Docker Compose (Production)
```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
```

### Using Kubernetes

#### 1. Apply Configurations
```bash
# Create namespace
kubectl create namespace hamstring-app

# Apply backend deployment
kubectl apply -f k8s/backend-deployment.yaml -n hamstring-app

# Apply frontend deployment
kubectl apply -f k8s/frontend-deployment.yaml -n hamstring-app
```

#### 2. Create Secrets
```bash
# Create secret for sensitive data
kubectl create secret generic app-secrets \
  --from-literal=secret-key='your-secret-key' \
  --from-literal=sendgrid-api-key='your-api-key' \
  -n hamstring-app
```

#### 3. Verify Deployment
```bash
# Check pods
kubectl get pods -n hamstring-app

# Check services
kubectl get svc -n hamstring-app

# Check logs
kubectl logs -f deployment/hamstring-backend -n hamstring-app
```

## CI/CD with GitHub Actions

### Setup GitHub Secrets
Go to Repository Settings → Secrets and add:

```
CRANE_API_KEY          - Crane Cloud API key
SECRET_KEY             - Flask secret key
SENDGRID_API_KEY       - SendGrid API key
SENDGRID_FROM_EMAIL    - Your verified email
BACKEND_URL            - Backend URL after deployment
FRONTEND_URL           - Frontend URL after deployment
```

### Workflows Available

1. **`ci-cd.yml`** - Full CI/CD pipeline
   - Runs on every push to main
   - Tests both backend and frontend
   - Builds Docker images
   - Pushes to GitHub Container Registry
   - Deploys to Crane Cloud

2. **`deploy-crane.yml`** - Direct deployment
   - Manual trigger or push to main
   - Builds and deploys directly to Crane Cloud
   - Includes health checks

### Manual Deployment
```bash
# Trigger deployment manually
gh workflow run deploy-crane.yml

# Or using the web interface
# Go to Actions → Deploy to Crane Cloud → Run workflow
```

## Crane Cloud Specific

### Using the Deployment Script
```bash
# Make script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

The script will:
1. Check Crane CLI installation
2. Authenticate with Crane Cloud
3. Deploy backend with environment variables
4. Deploy frontend with correct API URL
5. Update CORS settings
6. Run health checks
7. Display deployment URLs

### Manual Crane Deployment
```bash
# Install Crane CLI
curl -sSL https://cranecloud.io/install.sh | bash

# Login
crane auth login

# Deploy backend
cd backend
crane deploy \
  --app hamstring-backend \
  --env SECRET_KEY="your-secret" \
  --env SENDGRID_API_KEY="your-key" \
  --memory 2048 \
  --cpu 1

# Deploy frontend
cd ../frontend
crane deploy \
  --app hamstring-frontend \
  --build-arg REACT_APP_API_URL="https://backend-url" \
  --memory 512 \
  --cpu 0.5
```

## Docker Commands Reference

### Building Images
```bash
# Backend
docker build -t hamstring-backend:latest ./backend

# Frontend (development)
docker build -f Dockerfile.dev -t hamstring-frontend:dev ./frontend

# Frontend (production)
docker build -t hamstring-frontend:latest ./frontend
```

### Running Containers
```bash
# Backend
docker run -d \
  -p 5001:5001 \
  --name backend \
  --env-file backend/.env \
  hamstring-backend:latest

# Frontend
docker run -d \
  -p 3000:3000 \
  --name frontend \
  -e REACT_APP_API_URL=http://localhost:5001 \
  hamstring-frontend:dev
```

### Debugging
```bash
# Access container shell
docker exec -it backend /bin/bash

# View logs
docker logs -f backend

# Inspect container
docker inspect backend

# Check resource usage
docker stats
```

## Monitoring & Logging

### Docker Compose Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100
```

### Kubernetes Logs
```bash
# Pod logs
kubectl logs -f pod/hamstring-backend-xxxxx -n hamstring-app

# Deployment logs
kubectl logs -f deployment/hamstring-backend -n hamstring-app

# Previous container logs
kubectl logs pod/hamstring-backend-xxxxx --previous -n hamstring-app
```

### Crane Cloud Logs
```bash
# Follow logs
crane logs hamstring-backend --follow

# Recent logs
crane logs hamstring-backend --tail 100
```

## Scaling

### Docker Compose
```bash
# Scale backend to 3 instances
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Kubernetes
```bash
# Scale backend
kubectl scale deployment hamstring-backend --replicas=3 -n hamstring-app

# Auto-scaling
kubectl autoscale deployment hamstring-backend \
  --cpu-percent=70 \
  --min=2 \
  --max=5 \
  -n hamstring-app
```

### Crane Cloud
```bash
# Scale via CLI
crane scale hamstring-backend --replicas 3

# Or via dashboard: Apps → hamstring-backend → Scale
```

## Health Checks

### Check Backend
```bash
curl https://your-backend-url.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model": "GNODE",
  "version": "1.0.0"
}
```

### Check Frontend
```bash
curl -I https://your-frontend-url.com
```

Should return `200 OK`

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker logs backend

# Check events (Kubernetes)
kubectl describe pod hamstring-backend-xxxxx -n hamstring-app
```

### Out of Memory
```bash
# Check resource usage
docker stats

# Increase memory in docker-compose.yml or k8s yaml
```

### Network Issues
```bash
# Test connectivity between services
docker exec backend ping frontend

# Check network
docker network inspect hamstring-network
```

## Clean Up

### Docker Compose
```bash
# Stop and remove containers
docker-compose down

# Remove volumes too
docker-compose down -v

# Remove everything including images
docker-compose down --rmi all -v
```

### Kubernetes
```bash
# Delete all resources
kubectl delete namespace hamstring-app
```

### Crane Cloud
```bash
# Delete apps
crane apps delete hamstring-backend
crane apps delete hamstring-frontend
```

---

## Best Practices

1. **Never commit secrets** - Use environment variables or secret management
2. **Use multi-stage builds** - Reduces image size
3. **Health checks** - Always implement liveness and readiness probes
4. **Resource limits** - Set CPU and memory limits
5. **Logging** - Use structured logging (JSON)
6. **Monitoring** - Set up alerts for errors and high resource usage
7. **Backups** - Regular backups of model files and data
8. **Security** - Keep base images updated, scan for vulnerabilities

---

*For more details, see individual deployment guides:*
- `CRANE_CLOUD_DEPLOYMENT.md`
- `QUICK_DEPLOY_GUIDE.md`
