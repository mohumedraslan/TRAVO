$port = 8000
$ruleName = "TRAVO Backend API"

# Check if rule exists
$exists = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($exists) {
    Write-Host "Rule '$ruleName' already exists. Removing old rule..."
    Remove-NetFirewallRule -DisplayName $ruleName
}

Write-Host "Creating firewall rule '$ruleName' to allow TCP port $port..."
New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -LocalPort $port -Protocol TCP -Action Allow -Profile Any

Write-Host "✅ Firewall rule created successfully!"
Write-Host "Make sure to run the backend with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
