#!/bin/bash

# 🚀 Crane Cloud Deployment Script
# This script deploys both backend and frontend to Crane Cloud

set -e  # Exit on error

echo "🚀 Starting Crane Cloud Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Crane CLI is installed
if ! command -v crane &> /dev/null; then
    echo -e "${RED}❌ Crane CLI not found. Installing...${NC}"
    curl -sSL https://cranecloud.io/install.sh | bash
    export PATH="$PATH:$HOME/.crane/bin"
fi

# Check if logged in
echo -e "${YELLOW}🔐 Checking Crane Cloud authentication...${NC}"
if ! crane auth check &> /dev/null; then
    echo -e "${YELLOW}Please log in to Crane Cloud:${NC}"
    crane auth login
fi

# Load environment variables
if [ -f ".env.production" ]; then
    source .env.production
else
    echo -e "${RED}❌ .env.production not found. Please create it first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environment loaded${NC}"

# Deploy Backend
echo -e "${YELLOW}📦 Deploying Backend...${NC}"
cd backend

crane deploy \
    --app hamstring-backend \
    --dockerfile Dockerfile \
    --env SECRET_KEY="${SECRET_KEY}" \
    --env DEBUG="False" \
    --env MODEL_PATH="models/gnode_model.pth" \
    --env SENDGRID_API_KEY="${SENDGRID_API_KEY}" \
    --env SENDGRID_FROM_EMAIL="${SENDGRID_FROM_EMAIL}" \
    --env SENDGRID_FROM_NAME="${SENDGRID_FROM_NAME}" \
    --env USE_SENDGRID="true" \
    --memory 2048 \
    --cpu 1

# Get backend URL
BACKEND_URL=$(crane apps get hamstring-backend --format json | jq -r '.url')
echo -e "${GREEN}✅ Backend deployed at: ${BACKEND_URL}${NC}"

cd ..

# Update frontend environment with backend URL
echo -e "${YELLOW}🔧 Updating frontend configuration...${NC}"
export REACT_APP_API_URL="${BACKEND_URL}"

# Deploy Frontend
echo -e "${YELLOW}🎨 Deploying Frontend...${NC}"
cd frontend

crane deploy \
    --app hamstring-frontend \
    --dockerfile Dockerfile \
    --build-arg REACT_APP_API_URL="${BACKEND_URL}" \
    --memory 512 \
    --cpu 0.5

# Get frontend URL
FRONTEND_URL=$(crane apps get hamstring-frontend --format json | jq -r '.url')
echo -e "${GREEN}✅ Frontend deployed at: ${FRONTEND_URL}${NC}"

cd ..

# Update backend CORS with frontend URL
echo -e "${YELLOW}🔄 Updating backend CORS settings...${NC}"
crane env set hamstring-backend CORS_ORIGINS="${FRONTEND_URL}"
crane apps restart hamstring-backend

# Health checks
echo -e "${YELLOW}🏥 Running health checks...${NC}"
sleep 10

# Check backend health
if curl -f "${BACKEND_URL}/api/health" &> /dev/null; then
    echo -e "${GREEN}✅ Backend is healthy${NC}"
else
    echo -e "${RED}❌ Backend health check failed${NC}"
fi

# Check frontend
if curl -f "${FRONTEND_URL}" &> /dev/null; then
    echo -e "${GREEN}✅ Frontend is accessible${NC}"
else
    echo -e "${RED}❌ Frontend health check failed${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo -e "${YELLOW}Backend URL:${NC}  ${BACKEND_URL}"
echo -e "${YELLOW}Frontend URL:${NC} ${FRONTEND_URL}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Visit ${FRONTEND_URL} to test your app"
echo "2. Update DNS if using custom domain"
echo "3. Monitor logs: crane logs hamstring-backend --follow"
echo ""
