$ErrorActionPreference = "Stop"

function Test-Url {
    param([string]$Url, [string]$Method="GET")
    try {
        $response = Invoke-WebRequest -Uri $Url -Method $Method -UseBasicParsing -TimeoutSec 5
        Write-Host "✅ Success: $Url ($($response.StatusCode))" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed: $Url - $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

Write-Host "🔍 Testing Backend Connectivity..."
$root = Test-Url "http://localhost:8000/"
$api = Test-Url "http://localhost:8000/api/vision/identify" "POST"

if ($root -or $api) {
    Write-Host "`n✅ Backend appears to be running." -ForegroundColor Green
} else {
    Write-Host "`n❌ Backend appears to be DOWN or unreachable." -ForegroundColor Red
    Write-Host "Please ensure the backend server is running." -ForegroundColor Yellow
}
