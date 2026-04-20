# Social Media Growth System - PowerShell Helpers
# Add these to your profile or run: . ./social_media_helpers.ps1

function Generate-VideoBatch {
    param(
        [string]$Topic,
        [int]$Count = 5,
        [string]$BatchName = (Get-Date -Format "yyyyMMdd"),
        [string]$Style = "realistic"
    )
    
    Write-Host "🎬 Generating $Count videos: $Topic" -ForegroundColor Cyan
    python content_production_pipeline.py --topic "$Topic" --count $Count --batch-name $BatchName --style $Style
}

function Add-MonetizationHooks {
    param(
        [string]$BatchName,
        [string]$LoveGuardCTA = $null,
        [string]$AffiliateLink = $null,
        [string]$AffiliatePlatform = $null
    )
    
    if ($LoveGuardCTA) {
        Write-Host "💚 Adding LoveGuard CTA" -ForegroundColor Cyan
        python monetization_hooks.py --update-loveguard $LoveGuardCTA
    }
    
    if ($AffiliateLink -and $AffiliatePlatform) {
        Write-Host "🔗 Adding affiliate link: $AffiliatePlatform" -ForegroundColor Cyan
        python monetization_hooks.py --add-affiliate dating "$AffiliateLink" --affiliate-platform $AffiliatePlatform
    }
    
    Write-Host "📝 Injecting into batch: $BatchName" -ForegroundColor Cyan
    python monetization_hooks.py --batch $BatchName --inject
}

function Schedule-VideoBatch {
    param(
        [string]$BatchName,
        [string]$Interval = "daily",
        [string]$StartDate = $null
    )
    
    $args = @("--batch", $BatchName, "--schedule", "--interval", $Interval)
    if ($StartDate) {
        $args += @("--start-date", $StartDate)
    }
    
    Write-Host "📅 Scheduling batch: $BatchName ($Interval)" -ForegroundColor Cyan
    python content_production_pipeline.py @args
}

function Publish-Scheduled {
    param(
        [switch]$DryRun
    )
    
    $args = @("--publish")
    if ($DryRun) {
        $args += "--dry-run"
        Write-Host "🔍 DRY-RUN: Showing what would be published" -ForegroundColor Yellow
    } else {
        Write-Host "🚀 PUBLISHING scheduled videos" -ForegroundColor Green
    }
    
    python content_production_pipeline.py @args
}

function Get-Analytics {
    Write-Host "📊 Social Media Analytics Dashboard" -ForegroundColor Cyan
    python social_analytics_dashboard.py --show
}

function Record-VideoMetrics {
    param(
        [string]$VideoID,
        [string]$Platform = "youtube",
        [string]$Title,
        [int]$Views = 0,
        [int]$Likes = 0,
        [int]$Comments = 0,
        [double]$Engagement = 0
    )
    
    Write-Host "📈 Recording metrics for: $Title" -ForegroundColor Cyan
    python social_analytics_dashboard.py --track-video $VideoID --platform $Platform --title "$Title" --views $Views --likes $Likes --comments $Comments --engagement $Engagement
}

function Record-Revenue {
    param(
        [string]$Type,  # adsense, affiliate, sponsorship, loveguard_referral
        [string]$Platform,
        [double]$Amount
    )
    
    Write-Host "💰 Recording revenue: $Type on $Platform = \$$Amount" -ForegroundColor Green
    python social_analytics_dashboard.py --record-revenue $Type --platform $Platform --amount $Amount
}

function Export-Analytics {
    param(
        [string]$OutputFile = "analytics_export.csv"
    )
    
    Write-Host "📤 Exporting analytics to: $OutputFile" -ForegroundColor Cyan
    python social_analytics_dashboard.py --export $OutputFile
}

function Preview-Description {
    param(
        [string]$BatchName,
        [int]$VideoNum = 1,
        [string]$Platform = "youtube"
    )
    
    Write-Host "👀 Previewing description" -ForegroundColor Cyan
    python monetization_hooks.py --batch $BatchName --preview --video $VideoNum --platform $Platform
}

function Show-MonetizationConfig {
    Write-Host "⚙️  Monetization Hooks Configuration" -ForegroundColor Cyan
    python monetization_hooks.py --config
}

# Quick one-liners
function Quick-FullWorkflow {
    param(
        [string]$Topic,
        [int]$Count = 5
    )
    
    # Generate
    $batch = Get-Date -Format "yyyyMMdd"
    Generate-VideoBatch -Topic $Topic -Count $Count -BatchName $batch
    
    # Monetize
    Add-MonetizationHooks -BatchName $batch -LoveGuardCTA "Join 10k+ on LoveGuard for relationship insights"
    
    # Schedule
    Schedule-VideoBatch -BatchName $batch -Interval daily
    
    # Show stats
    Get-Analytics
}

Write-Host "✓ Social Media Growth Helpers loaded!" -ForegroundColor Green
Write-Host "Available functions:" -ForegroundColor Cyan
Write-Host "  Generate-VideoBatch -Topic 'your topic' -Count 5"
Write-Host "  Add-MonetizationHooks -BatchName week1"
Write-Host "  Schedule-VideoBatch -BatchName week1"
Write-Host "  Publish-Scheduled -DryRun"
Write-Host "  Get-Analytics"
Write-Host "  Record-VideoMetrics -VideoID vid123 -Platform youtube -Title 'My Video' -Views 1000"
Write-Host "  Record-Revenue -Type affiliate -Platform dating_apps -Amount 50"
Write-Host "  Export-Analytics"
Write-Host "  Quick-FullWorkflow -Topic 'dating advice'"

