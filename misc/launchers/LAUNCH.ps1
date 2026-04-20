# Quick Launch Script - Copy and paste into PowerShell

# Set working directory
cd "c:\Users\charm\content_automation_ai"

# Load all helpers
Write-Host "Loading Social Media Growth System..." -ForegroundColor Cyan
. .\social_media_helpers.ps1

Write-Host "`n" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "  SOCIAL MEDIA GROWTH SYSTEM READY!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════════" -ForegroundColor Green

Write-Host "`n📖 READ FIRST:" -ForegroundColor Cyan
Write-Host "  1. GROWTH_SYSTEM_README.md"
Write-Host "  2. QUICK_REFERENCE.md"

Write-Host "`n🚀 QUICK START:" -ForegroundColor Yellow
Write-Host "  # Generate 5 videos"
Write-Host '  Generate-VideoBatch -Topic "relationship advice" -Count 5 -BatchName week1' -ForegroundColor White

Write-Host "`n  # Add monetization" -ForegroundColor Yellow
Write-Host "  Add-MonetizationHooks -BatchName week1" -ForegroundColor White

Write-Host "`n  # Schedule for publishing" -ForegroundColor Yellow
Write-Host "  Schedule-VideoBatch -BatchName week1" -ForegroundColor White

Write-Host "`n  # View analytics" -ForegroundColor Yellow
Write-Host "  Get-Analytics" -ForegroundColor White

Write-Host "`n💰 REVENUE TRACKING:" -ForegroundColor Yellow
Write-Host "  Record-Revenue -Type adsense -Platform youtube -Amount 100" -ForegroundColor White
Write-Host "  Get-Analytics" -ForegroundColor White

Write-Host "`n📊 AVAILABLE FUNCTIONS:" -ForegroundColor Cyan
Write-Host "  Generate-VideoBatch"
Write-Host "  Add-MonetizationHooks"
Write-Host "  Schedule-VideoBatch"
Write-Host "  Publish-Scheduled"
Write-Host "  Get-Analytics"
Write-Host "  Record-VideoMetrics"
Write-Host "  Record-Revenue"
Write-Host "  Export-Analytics"
Write-Host "  Preview-Description"
Write-Host "  Quick-FullWorkflow"

Write-Host "`n════════════════════════════════════════════════════════`n" -ForegroundColor Green

# Optional: Show monetization config
# python monetization_hooks.py --config
