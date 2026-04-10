# TRAVO Backend Endpoint Testing Script
# Run this script to test all backend endpoints

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "TRAVO Backend Endpoint Testing" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:8000"

# Test 1: Root endpoint
Write-Host "Test 1: Testing root endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/" -Method Get
    Write-Host "✅ Root endpoint working" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Root endpoint failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 2: API spec endpoint
Write-Host "Test 2: Testing API spec endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api-spec" -Method Get
    Write-Host "✅ API spec endpoint working" -ForegroundColor Green
} catch {
    Write-Host "❌ API spec endpoint failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 3: Itinerary test endpoint
Write-Host "Test 3: Testing itinerary test endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "$baseUrl/api/itineraries/test" -Method Get
    Write-Host "✅ Itinerary test endpoint working" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Itinerary test endpoint failed: $_" -ForegroundColor Red
}
Write-Host ""

# Test 4: Login endpoint (should fail without credentials, but endpoint should exist)
Write-Host "Test 4: Testing login endpoint..." -ForegroundColor Yellow
try {
    $body = @{
        username = ""
        password = ""
    }
    $response = Invoke-RestMethod -Uri "$baseUrl/api/user/login" -Method Post -Body $body -ContentType "application/x-www-form-urlencoded"
    Write-Host "✅ Login endpoint exists" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 401 -or $_.Exception.Response.StatusCode -eq 422) {
        Write-Host "✅ Login endpoint exists (returned expected error)" -ForegroundColor Green
    } else {
        Write-Host "❌ Login endpoint failed: $_" -ForegroundColor Red
    }
}
Write-Host ""

# Test 5: Vision identify endpoint (should fail without image, but endpoint should exist)
Write-Host "Test 5: Testing vision identify endpoint..." -ForegroundColor Yellow
try {
    $body = @{
        image = ""
    } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "$baseUrl/api/vision/identify" -Method Post -Body $body -ContentType "application/json"
    Write-Host "✅ Vision identify endpoint exists" -ForegroundColor Green
} catch {
    if ($_.Exception.Response.StatusCode -eq 422 -or $_.Exception.Response.StatusCode -eq 400) {
        Write-Host "✅ Vision identify endpoint exists (returned expected error)" -ForegroundColor Green
    } else {
        Write-Host "❌ Vision identify endpoint failed: $_" -ForegroundColor Red
    }
}
Write-Host ""

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Testing Complete!" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. If any tests failed, make sure the backend is running" -ForegroundColor White
Write-Host "2. Restart the backend server to load new routes" -ForegroundColor White
Write-Host "3. Test from mobile app: npx expo start -c" -ForegroundColor White
Write-Host ""
