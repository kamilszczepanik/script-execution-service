#!/bin/bash

set -e

PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="safe-script-execution-service"
REGION="us-west2"

echo "Deploying to Google Cloud Run in project: $PROJECT_ID"

echo "Building and pushing container image..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
  --platform managed \
  --allow-unauthenticated \
  --region $REGION \
  --memory 512Mi \
  --cpu 1 \
  --port 8080

echo "Deployment completed successfully!"
echo "Your service will be available at the URL shown above." 