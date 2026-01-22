$url = 'https://majdkassawat.github.io/RecycleWebsite/_badge_generator.html'
$maxAttempts = 30

Write-Host 'Checking GitHub Pages URL directly...' -ForegroundColor Cyan
Write-Host "URL: $url`n"

$attempt = 0
while ($attempt -lt $maxAttempts) {
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            Write-Host "SUCCESS! Page is now available!" -ForegroundColor Green
            Write-Host "Status: $($response.StatusCode)"
            Write-Host "Direct link: $url"
            exit 0
        }
    }
    catch {
        Write-Host "[Attempt $attempt/30] Checking..." -ForegroundColor Yellow
    }
    
    if ($attempt -lt $maxAttempts) {
        Start-Sleep -Seconds 2
    }
}

Write-Host 'Timeout' -ForegroundColor Red
