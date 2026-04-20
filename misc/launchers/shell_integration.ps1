# Shell integration helpers for Content Automation AI
# Drop this file in the repo and add a dot-source line to your PowerShell profile:
#   Add-Content -Path $PROFILE -Value ". 'C:\Users\charm\content_automation_ai\shell_integration.ps1'"
# Then restart PowerShell (or run `. $PROFILE`) to load helpers.

function ca-build-payload {
    param()
    python "$PSScriptRoot\monetization\build_payload.py"
}

function ca-run-flow {
    param()
    python "$PSScriptRoot\monetization\run_flow.py"
}

function ca-generate-outreach {
    param(
        [int]$Count = 50
    )
    python "$PSScriptRoot\monetization\generate_50_list.py"
}

function ca-preview-outreach {
    param(
        [string]$Csv = "$PSScriptRoot\monetization\outreach_list_50.csv",
        [string]$Template = "$PSScriptRoot\monetization\emails\cold_outreach_personalized.md",
        [string]$Out = "$PSScriptRoot\monetization\previews_50.json"
    )
    python "$PSScriptRoot\monetization\agents\personalize_and_preview.py" --csv $Csv --template $Template --out $Out
}

function ca-preview-nurture {
    param()
    python "$PSScriptRoot\monetization\agents\send_sequence.py" --template "$PSScriptRoot\monetization\emails\nurture_emails.md" --dry-run
}

function ca-simulate-purchase {
    param(
        [string]$Email = 'testbuyer@example.com',
        [double]$Price = 17.0
    )
    python "$PSScriptRoot\monetization\checkout_simulator.py" --email $Email --price $Price
    python "$PSScriptRoot\monetization\deliver_payload.py"
}

function ca-dashboard {
    param()
    python "$PSScriptRoot\monetization\dashboard.py"
}

Set-Alias gbp ca-build-payload
Set-Alias runflow ca-run-flow
Set-Alias gen50 ca-generate-outreach
Set-Alias preview50 ca-preview-outreach
Set-Alias prevn ca-preview-nurture
Set-Alias simbuy ca-simulate-purchase
Set-Alias cadash ca-dashboard

Write-Verbose "Content Automation AI shell helpers loaded. Aliases: gbp, runflow, gen50, preview50, prevn, simbuy, cadash"
