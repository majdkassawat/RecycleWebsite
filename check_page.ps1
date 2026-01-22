$url = 'https://tadweer-tech-sy.org/badge_generator.html'
$maxAttempts = 60
$attempt = 0

Write-Host 'Checking if badge generator is available...' -ForegroundColor Cyan
Write-Host "URL: $url`n"

while ($attempt -lt $maxAttempts) {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "SUCCESS! Page is now available (Attempt $attempt)" -ForegroundColor Green
            Write-Host "Status: $($response.StatusCode) - Page is live!"
            exit 0
        }
    }
    catch {
        Write-Host "[Attempt $attempt/60] Still deploying..." -ForegroundColor Yellow
    }
    
    if ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 2
    }
}

Write-Host 'Timeout: Page did not become available within 2 minutes' -ForegroundColor Red
