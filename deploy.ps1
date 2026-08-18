# Marquee Deployment Script (PowerShell)
# This script sets up Secret Manager and deploys the services to Google Cloud Run.

$PROJECT_ID = "gen-lang-client-0094400410"
$REGION = "us-central1"

Write-Host "Configuring Google Cloud CLI..."
gcloud config set project $PROJECT_ID

Write-Host "Creating Secrets in Secret Manager..."
# Parse .env ignoring comments and empty lines
$envLines = Get-Content .env | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '=' }

$secretMappings = @()

foreach ($line in $envLines) {
    # Split by the first '=' to get key and value
    $index = $line.IndexOf('=')
    if ($index -gt 0) {
        $key = $line.Substring(0, $index).Trim()
        $value = $line.Substring($index + 1).Trim()
        
        Write-Host "Processing secret $key..."
        
        # Check if secret exists
        $exists = gcloud secrets describe $key --project=$PROJECT_ID 2>$null
        if (-not $exists) {
            gcloud secrets create $key --replication-policy="automatic" --project=$PROJECT_ID
        }
        
        # Write value to a temporary file (without BOM and without trailing newline) to avoid PowerShell pipe issues
        $tempFile = [System.IO.Path]::GetTempFileName()
        [System.IO.File]::WriteAllText($tempFile, $value, [System.Text.Encoding]::UTF8)
        
        # Add new version
        gcloud secrets versions add $key --data-file=$tempFile --project=$PROJECT_ID
        
        # Cleanup
        Remove-Item $tempFile

        # Add to mappings for Cloud Run (exclude PORT as Cloud Run injects it)
        if ($key -ne "PORT") {
            $secretMappings += "$($key)=$($key):latest"
        }
    }
}

$secretsFlag = $secretMappings -join ","

Write-Host "Granting Secret Accessor role to default compute service account..."
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:321849204854-compute@developer.gserviceaccount.com" --role="roles/secretmanager.secretAccessor"

Write-Host "Deploying Backend to Cloud Run..."
gcloud run deploy marquee-backend `
    --source . `
    --region $REGION `
    --project $PROJECT_ID `
    --allow-unauthenticated `
    --update-secrets=$secretsFlag `
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
