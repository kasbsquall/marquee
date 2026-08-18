# Marquee Deployment Script (PowerShell)
# This script sets up Secret Manager and deploys the services to Google Cloud Run.

$PROJECT_ID = "gen-lang-client-0094400410"
$REGION = "us-central1"

Write-Host "Configuring Google Cloud CLI..."
gcloud config set project $PROJECT_ID

Write-Host "Creating Secrets in Secret Manager..."
# Assuming .env contains GEMINI_API_KEY, GRAFANA_URL, GRAFANA_TOKEN, OTLP_ENDPOINT
# Extract variables from .env
$envVars = Get-Content .env | Where-Object { $_ -match "^[^#]*=" } | ConvertFrom-StringData

foreach ($key in $envVars.Keys) {
    $value = $envVars[$key]
    Write-Host "Creating secret $key..."
    # Check if secret exists
    $exists = gcloud secrets describe $key --project=$PROJECT_ID 2>$null
    if (-not $exists) {
        gcloud secrets create $key --replication-policy="automatic" --project=$PROJECT_ID
    }
    # Add new version
    $value | gcloud secrets versions add $key --data-file=- --project=$PROJECT_ID
}

Write-Host "Deploying Backend to Cloud Run..."
gcloud run deploy marquee-backend `
    --source . `
    --region $REGION `
    --project $PROJECT_ID `
    --allow-unauthenticated `
    --update-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,GRAFANA_URL=GRAFANA_URL:latest,GRAFANA_TOKEN=GRAFANA_TOKEN:latest,OTLP_ENDPOINT=OTLP_ENDPOINT:latest,OTLP_INSTANCE_ID=OTLP_INSTANCE_ID:latest" `
    --quiet

Write-Host "Deploying Frontend to Cloud Run..."
Set-Location frontend
gcloud run deploy marquee-frontend `
    --source . `
    --region $REGION `
    --project $PROJECT_ID `
    --allow-unauthenticated `
    --quiet
Set-Location ..

Write-Host "Deployment Complete! Check the Cloud Run console for the public URLs."
