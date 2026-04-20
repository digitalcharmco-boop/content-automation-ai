# QUICK REFERENCE CARD

## One-Page Cheat Sheet

### Load Helpers (First Time)
```powershell
. .\social_media_helpers.ps1
```

### Weekly Workflow (Copy & Paste)
```powershell
# Monday - Generate
Generate-VideoBatch -Topic "relationship psychology tips" -Count 5 -BatchName week1

# Tuesday - Monetize
Add-MonetizationHooks -BatchName week1

# Wednesday - Schedule
Schedule-VideoBatch -BatchName week1 -Interval daily

# Thursday-Sunday - Monitor
Get-Analytics
```

### All Commands Cheat Sheet

| What | PowerShell | Python |
|------|-----------|--------|
| **Generate videos** | `Generate-VideoBatch -Topic "..." -Count 5 -BatchName week1` | `python content_production_pipeline.py --topic "..." --count 5 --batch-name week1` |
| **Add CTAs/links** | `Add-MonetizationHooks -BatchName week1` | `python monetization_hooks.py --batch week1 --inject` |
| **Schedule publish** | `Schedule-VideoBatch -BatchName week1 -Interval daily` | `python content_production_pipeline.py --batch week1 --schedule --interval daily` |
| **View analytics** | `Get-Analytics` | `python social_analytics_dashboard.py --show` |
| **Record revenue** | `Record-Revenue -Type adsense -Platform youtube -Amount 100` | `python social_analytics_dashboard.py --record-revenue youtube_adsense --platform youtube --amount 100` |
| **Export report** | `Export-Analytics -OutputFile report.csv` | `python social_analytics_dashboard.py --export report.csv` |
| **Preview CTA** | N/A | `python monetization_hooks.py --batch week1 --preview --video 1 --platform youtube` |
| **Update CTA** | N/A | `python monetization_hooks.py --update-loveguard "Your text"` |
| **Add affiliate** | N/A | `python monetization_hooks.py --add-affiliate dating "https://url.com" --affiliate-platform name` |

---

## File Locations

```
Your project root: c:\Users\charm\content_automation_ai\

Generated content:
  content_production/batches/week1/
  content_production/batches/week2/
  ...

Configuration files:
  content_production/schedule.json
  content_production/monetization_hooks.json

Analytics:
  social_analytics/platform_stats.json
  social_analytics/video_performance.json
  social_analytics/audience_growth.json
  social_analytics/monetization_summary.json

Scripts:
  content_production_pipeline.py
  monetization_hooks.py
  social_analytics_dashboard.py
  social_media_helpers.ps1

Guides:
  GROWTH_SYSTEM_README.md
  SOCIAL_MEDIA_GROWTH_GUIDE.md
  SYSTEM_DIAGRAMS.md
  IMPLEMENTATION_SUMMARY.md
```

---

## Revenue Per Action

| Action | Revenue |
|--------|---------|
| 1,000 YouTube views | $3-5 |
| Affiliate conversion | $2-10 |
| LoveGuard referral | $5-15 |
| Sponsored video | $1,000-10,000 |

---

## Milestones

| Milestone | Followers | Revenue/Month | Timeline |
|-----------|-----------|---------------|----------|
| Start earning (YouTube) | 1,000 | $50-200 | Month 1 |
| YouTube AdSense active | 1,000 | $300-1,000 | Month 2 |
| Sponsorship opportunities | 10,000 | $1,500+ | Month 3 |
| Full monetization | 50,000+ | $5,000+ | Month 6 |

---

## Quick Troubleshooting

### Problem: Videos not generating
**Solution:** `set OPENAI_API_KEY=your_key`

### Problem: Schedule not publishing
**Solution:** `cat content_production/schedule.json`

### Problem: Analytics zeros
**Solution:** `Record-VideoMetrics -VideoID test -Platform youtube -Title "Test" -Views 100`

### Problem: Helpers not loading
**Solution:** `. "c:\Users\charm\content_automation_ai\social_media_helpers.ps1"`

---

## Key Numbers

- **Content per week:** 5-10 videos
- **Batches to have:** 10-20 before going "viral"
- **Total videos needed:** 50-100 for passive income
- **Upload frequency:** 1 video/day minimum
- **Time per workflow:** 1 hour/week
- **Followers to earn $5k/month:** 200,000+
- **Views per 1000:** ~$3-5 revenue

---

## Monthly Checklist

- [ ] Generated new batch(es)
- [ ] Added monetization hooks
- [ ] Scheduled for publishing
- [ ] Reviewed analytics (Get-Analytics)
- [ ] Updated LoveGuard CTA if needed
- [ ] Added new affiliate links if needed
- [ ] Logged revenue (Record-Revenue)
- [ ] Exported monthly report (Export-Analytics)
- [ ] Identified top-performing content
- [ ] Planned next month's topics

---

## Documentation Map

| Document | Purpose | Read When |
|----------|---------|-----------|
| `README.md` | Original system overview | First time setup |
| `GROWTH_SYSTEM_README.md` | Complete growth system | Before first batch |
| `SOCIAL_MEDIA_GROWTH_GUIDE.md` | Detailed monetization strategies | Planning content |
| `SYSTEM_DIAGRAMS.md` | Visual architecture & flows | Understanding the system |
| `IMPLEMENTATION_SUMMARY.md` | What was built & why | Overview of components |
| This file | Quick reference | Daily use |

---

## PowerShell Function Signatures

```powershell
# Generate videos
Generate-VideoBatch -Topic <string> -Count <int> -BatchName <string> -Style <string>

# Add monetization
Add-MonetizationHooks -BatchName <string> -LoveGuardCTA <string> -AffiliateLink <string> -AffiliatePlatform <string>

# Schedule publishing
Schedule-VideoBatch -BatchName <string> -Interval daily|weekly -StartDate <string>

# Publish videos
Publish-Scheduled [-DryRun]

# View analytics
Get-Analytics

# Record metrics
Record-VideoMetrics -VideoID <string> -Platform <string> -Title <string> -Views <int> -Likes <int> -Comments <int> -Engagement <double>

# Record revenue
Record-Revenue -Type adsense|affiliate|sponsorship|loveguard_referral -Platform <string> -Amount <double>

# Export data
Export-Analytics [-OutputFile <string>]

# Preview description
Preview-Description -BatchName <string> -VideoNum <int> -Platform <string>

# One-liner workflow
Quick-FullWorkflow -Topic <string> [-Count <int>]
```

---

## Common Configurations

### Standard Dating Content
```powershell
Generate-VideoBatch -Topic "relationship psychology" -Count 5 -BatchName week1
Generate-VideoBatch -Topic "how to text girls" -Count 5 -BatchName week2
Generate-VideoBatch -Topic "dating advice for men" -Count 5 -BatchName week3
```

### Monetization Setup
```powershell
python monetization_hooks.py --update-loveguard "Try LoveGuard Premium: https://loveguard.app/ref/yourname"
python monetization_hooks.py --add-affiliate dating "https://bumble.com?ref=you" --affiliate-platform bumble
python monetization_hooks.py --add-affiliate dating "https://match.com?ref=you" --affiliate-platform match
```

### Publishing Schedule
```powershell
# Daily videos for 2 months (60 videos)
Schedule-VideoBatch -BatchName week1 -Interval daily
Schedule-VideoBatch -BatchName week2 -Interval daily -StartDate "2025-12-16"
# ... repeat for weeks 3-12

# Then check what's scheduled
cat content_production/schedule.json
```

### Revenue Tracking
```powershell
# Daily
Get-Analytics

# When you get paid
Record-Revenue -Type adsense -Platform youtube -Amount <amount>
Record-Revenue -Type affiliate -Platform dating_apps -Amount <amount>
Record-Revenue -Type loveguard_referral -Platform loveguard -Amount <amount>

# Monthly
Export-Analytics -OutputFile "analytics_$(Get-Date -Format 'yyyy-MM').csv"
```

---

## Quick Math

**If you reach these numbers by month 3:**
- 50,000 followers
- 10,000 views/day average
- 300,000 views/month

**Revenue estimate:**
- YouTube AdSense (3% CTR, $4 CPM): $1,200/month
- Affiliate clicks (1% CTR, 5% convert, $5 commission): $750/month  
- LoveGuard referrals (0.5% CTR, 10% convert, $10): $150/month
- Total: **~$2,100/month** (conservative)

**With sponsorships (month 4+):** Add $1,000-5,000/month

---

**Last Updated:** December 8, 2025
**System Version:** Social Media Growth 1.0
