# DIGIFORMATION LTD — Lead Hunter Health Check
$url = "http://127.0.0.1:8000/api/health"
Write-Host "Checking Lead Hunter backend health at $url..." -ForegroundColor Cyan
try {
    $res = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 5
    Write-Host "Status: OK" -ForegroundColor Green
    $res | Format-List
} catch {
    Write-Host "Failed to connect to backend: $_" -ForegroundColor Red
}
