# Content Automation AI - PowerShell Launcher
# Run this script to start the automation system

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CONTENT AUTOMATION AI - LAUNCHER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if OPENAI_API_KEY is set
if (-not $env:OPENAI_API_KEY) {
    Write-Host "[WARNING] OPENAI_API_KEY is not set." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To set it for this session:" -ForegroundColor Yellow
    Write-Host '  $env:OPENAI_API_KEY="your-api-key-here"' -ForegroundColor White
    Write-Host ""
    Write-Host "Or permanently:" -ForegroundColor Yellow
    Write-Host '  [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key", "User")' -ForegroundColor White
    Write-Host ""
    Write-Host "The system will run in demo mode without actual content generation." -ForegroundColor Yellow
    Write-Host ""
    Pause
}

function Show-Menu {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  MENU - Select an option:" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "  1. Run system test" -ForegroundColor White
    Write-Host "  2. Generate video batch (requires API key)" -ForegroundColor White
    Write-Host "  3. View statistics" -ForegroundColor White
    Write-Host "  4. Add monetization hooks" -ForegroundColor White
    Write-Host "  5. Schedule batch for publishing" -ForegroundColor White
    Write-Host "  6. Load PowerShell helpers" -ForegroundColor White
    Write-Host "  7. View documentation" -ForegroundColor White
    Write-Host "  8. Exit" -ForegroundColor White
    Write-Host ""
}

function Run-Test {
    Write-Host ""
    Write-Host "Running system test..." -ForegroundColor Green
    & .\.venv\Scripts\python.exe simple_test.py
    Pause
}

function Generate-Batch {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  GENERATE VIDEO BATCH" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""

    $topic = Read-Host "Enter topic (e.g., 'relationship psychology facts')"
    $count = Read-Host "Enter number of videos (default 5)"
    $batch = Read-Host "Enter batch name (default: auto-generated)"

    if ([string]::IsNullOrWhiteSpace($count)) { $count = 5 }

    if ([string]::IsNullOrWhiteSpace($batch)) {
        & .\.venv\Scripts\python.exe content_production_pipeline.py --topic "$topic" --count $count
    } else {
        & .\.venv\Scripts\python.exe content_production_pipeline.py --topic "$topic" --count $count --batch-name $batch
    }

    Write-Host ""
    Write-Host "Batch generation complete!" -ForegroundColor Green
    Pause
}

function Show-Stats {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  STATISTICS" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    & .\.venv\Scripts\python.exe content_production_pipeline.py --stats
    Pause
}

function Add-Monetization {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  ADD MONETIZATION HOOKS" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""

    $batch = Read-Host "Enter batch name"
    $cta = Read-Host "Enter CTA text (e.g., 'Try LoveGuard Premium!')"

    & .\.venv\Scripts\python.exe content_production_pipeline.py --batch $batch --add-cta "$cta"

    Write-Host ""
    Write-Host "Monetization hooks added!" -ForegroundColor Green
    Pause
}

function Schedule-Batch {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  SCHEDULE BATCH FOR PUBLISHING" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""

    $batch = Read-Host "Enter batch name"
    $interval = Read-Host "Enter interval (daily/weekly, default: daily)"

    if ([string]::IsNullOrWhiteSpace($interval)) { $interval = "daily" }

    & .\.venv\Scripts\python.exe content_production_pipeline.py --batch $batch --schedule --interval $interval

    Write-Host ""
    Write-Host "Batch scheduled!" -ForegroundColor Green
    Pause
}

function Load-Helpers {
    Write-Host ""
    Write-Host "Loading PowerShell helpers..." -ForegroundColor Green
    . .\social_media_helpers.ps1
    Write-Host "Helpers loaded! Type 'Get-Command *Video*' to see available commands." -ForegroundColor Green
    Pause
}

function Show-Docs {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "  DOCUMENTATION" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available documentation files:" -ForegroundColor White
    Write-Host "  - 00_START_HERE.md - Quick start guide" -ForegroundColor Gray
    Write-Host "  - GROWTH_SYSTEM_README.md - Complete system overview" -ForegroundColor Gray
    Write-Host "  - QUICK_REFERENCE.md - Command reference" -ForegroundColor Gray
    Write-Host "  - SOCIAL_MEDIA_GROWTH_GUIDE.md - Growth strategies" -ForegroundColor Gray
    Write-Host ""
    Write-Host "For PowerShell helpers:" -ForegroundColor White
    Write-Host "  . .\social_media_helpers.ps1" -ForegroundColor Gray
    Write-Host ""
    Pause
}

# Main loop
while ($true) {
    Show-Menu
    $choice = Read-Host "Enter your choice (1-8)"

    switch ($choice) {
        "1" { Run-Test }
        "2" { Generate-Batch }
        "3" { Show-Stats }
        "4" { Add-Monetization }
        "5" { Schedule-Batch }
        "6" { Load-Helpers }
        "7" { Show-Docs }
        "8" {
            Write-Host ""
            Write-Host "Thank you for using Content Automation AI!" -ForegroundColor Cyan
            Write-Host ""
            exit
        }
        default {
            Write-Host "Invalid choice. Please try again." -ForegroundColor Red
            Pause
        }
    }
}
