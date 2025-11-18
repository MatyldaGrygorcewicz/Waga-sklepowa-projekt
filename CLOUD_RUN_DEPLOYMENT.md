# Google Cloud Run Deployment Guide

This guide explains how to deploy the AI-Powered Shop Scale application to Google Cloud Run.

## Prerequisites

1. Google Cloud account with billing enabled
2. Google Cloud SDK installed (`gcloud` CLI)
3. Docker installed locally (for testing)

## Project Structure

```
/mnt/c/projektyProgramistyczne/Waga sklepowa projekt/
├── Dockerfile                      # Cloud Run optimized Dockerfile
├── .dockerignore                   # Files to exclude from build
├── backend/
│   ├── app.py                     # Flask application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── model_loader.py
│   ├── weight_estimator.py
│   └── database.py
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── fruit_classifier_model.h5      # TensorFlow model (31MB)
└── model_info.json                # Model metadata
```

## Deployment Steps

### 1. Set up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create YOUR-PROJECT-ID --name="AI Shop Scale"

# Set the project
gcloud config set project YOUR-PROJECT-ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### 2. Build and Deploy to Cloud Run

```bash
# Navigate to project directory
cd "/mnt/c/projektyProgramistyczne/Waga sklepowa projekt"

# Deploy to Cloud Run (builds and deploys in one command)
gcloud run deploy ai-shop-scale \
  --source . \
  --platform managed \
  --region europe-central2 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

**Note:** Adjust `--region` to your preferred location (e.g., `us-central1`, `europe-west1`)

### 3. Alternative: Build with Cloud Build, then Deploy

```bash
# Build the container image
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/ai-shop-scale

# Deploy the built image
gcloud run deploy ai-shop-scale \
  --image gcr.io/YOUR-PROJECT-ID/ai-shop-scale \
  --platform managed \
  --region europe-central2 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### 4. Test Local Docker Build (Optional)

```bash
# Build locally
docker build -t ai-shop-scale .

# Run locally
docker run -p 8080:8080 ai-shop-scale

# Test at http://localhost:8080
```

## Configuration Options

### Memory and CPU Settings

The application requires adequate resources due to TensorFlow model:
- **Minimum:** 1Gi memory, 1 CPU
- **Recommended:** 2Gi memory, 2 CPUs (specified in deployment)
- **For high traffic:** 4Gi memory, 2 CPUs

### Timeout

- Set to 300 seconds (5 minutes) to allow for:
  - ML model loading on cold start
  - Image processing for large files
  - TensorFlow inference

### Autoscaling

- `--max-instances 10`: Limits maximum concurrent instances
- `--min-instances 0`: Default, scales to zero when idle (cost savings)
- For consistent performance, set `--min-instances 1`

### Environment Variables (if needed)

```bash
gcloud run deploy ai-shop-scale \
  --set-env-vars "ENV_VAR_NAME=value"
```

## Costs Estimation

Cloud Run pricing (as of 2024):
- **CPU:** $0.00002400 per vCPU-second
- **Memory:** $0.00000250 per GiB-second
- **Requests:** $0.40 per million requests
- **Free tier:** 2 million requests/month, 360,000 GiB-seconds

With 2 vCPUs and 2GiB memory:
- Average request (2s): ~$0.000146
- 1000 requests/day: ~$4.38/month

**Note:** Costs increase with traffic and instance count.

## Docker Image Optimization

The Dockerfile includes several optimizations:

1. **Multi-stage not needed** - slim base image is already small
2. **Layer caching** - requirements.txt copied first
3. **System cleanup** - apt lists removed after installation
4. **No cache** - pip packages installed without cache
5. **Minimal dependencies** - only required system libraries

Expected image size: ~1.5-2GB (due to TensorFlow)

## Monitoring and Logs

```bash
# View logs
gcloud run services logs read ai-shop-scale --region europe-central2

# Monitor in real-time
gcloud run services logs tail ai-shop-scale --region europe-central2
```

Or use Google Cloud Console:
- Cloud Run > ai-shop-scale > Logs
- Cloud Run > ai-shop-scale > Metrics

## Updating the Application

```bash
# Redeploy with latest code
gcloud run deploy ai-shop-scale --source .

# Or with specific image
gcloud run deploy ai-shop-scale --image gcr.io/YOUR-PROJECT-ID/ai-shop-scale:latest
```

## Troubleshooting

### Cold Start Times
- First request after idle period may take 10-30 seconds
- Solution: Set `--min-instances 1` to keep at least one instance warm

### Out of Memory Errors
- Increase memory: `--memory 4Gi`
- Reduce workers in Dockerfile (currently 2)

### Timeout Errors
- Increase timeout: `--timeout 600` (max 60 minutes)
- Check logs for actual issue

### Model Loading Issues
- Ensure model files are in correct location
- Check file permissions in container
- Verify TensorFlow version compatibility

## Security Considerations

1. **Authentication:** Currently set to `--allow-unauthenticated` for public access
2. **For private use:** Remove the flag or use Cloud IAM
3. **API Keys:** Add authentication to Flask endpoints if needed
4. **CORS:** Configured in Flask app for frontend access

## Production Checklist

- [ ] Set appropriate memory/CPU limits
- [ ] Configure autoscaling (min/max instances)
- [ ] Set up monitoring and alerting
- [ ] Review security settings
- [ ] Test cold start performance
- [ ] Verify all endpoints work correctly
- [ ] Check logs for errors
- [ ] Set up custom domain (optional)
- [ ] Configure CDN for static files (optional)

## Support

For issues with:
- **Google Cloud Run:** https://cloud.google.com/run/docs
- **Application errors:** Check application logs
- **Docker build:** Test locally with `docker build`

## Clean Up

```bash
# Delete Cloud Run service
gcloud run services delete ai-shop-scale --region europe-central2

# Delete container images
gcloud container images delete gcr.io/YOUR-PROJECT-ID/ai-shop-scale
```
