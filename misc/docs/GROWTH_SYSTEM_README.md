# Content Automation AI + Social Media Growth System

**Complete system to auto-generate viral videos → build audience → monetize.**

## What You Get

### 1. **Content Generation** (Existing)
- AI script generation with viral psychology
- 6 animation styles + 5 story templates
- Auto-publish to YouTube, TikTok, Instagram, Twitter

### 2. **Batch Production Pipeline** (NEW)
- Generate 5-10 video variations from a single topic
- Schedule automatic daily publishing
- Track what's been published vs. pending

### 3. **Monetization Hooks** (NEW)
- Auto-inject LoveGuard CTAs into every video
- Add affiliate links (dating apps, etc.)
- Include sponsorship opportunities
- Platform-specific CTAs (YouTube, TikTok, etc.)

### 4. **Analytics Dashboard** (NEW)
- Track followers, views, engagement across platforms
- Monitor video performance
- Track revenue from all sources (YouTube, affiliates, LoveGuard, sponsorships)
- Export to CSV for reporting

---

## Revenue Streams (All Automated)

| Source | Setup | Earnings |
|--------|-------|----------|
| **YouTube AdSense** | Auto-enabled at 1k subs + 4k hours | $3-5 per 1k views |
| **Affiliate Links** | `--add-affiliate` in monetization_hooks | $2-10 per signup |
| **LoveGuard Referrals** | `--update-loveguard` with your link | Varies by commission |
| **Sponsorships** | Enable in config, pitch brands at 10k+ followers | $1,000-10,000 per video |

---

## Quick Start (One Workflow)

```powershell
# Load helpers
. .\social_media_helpers.ps1

# 1. Generate 5 videos on a topic
Generate-VideoBatch -Topic "relationship advice for single men" -Count 5 -BatchName week1

# 2. Add monetization (CTAs + affiliates)
Add-MonetizationHooks -BatchName week1 -LoveGuardCTA "Join 10k+ on LoveGuard: [link]"

# 3. Schedule for daily publishing
Schedule-VideoBatch -BatchName week1 -Interval daily

# 4. View analytics
Get-Analytics

# 5. Repeat weekly
#    Generate-VideoBatch -Topic "how to text girls" -Count 5 -BatchName week2
#    Add-MonetizationHooks -BatchName week2
#    Schedule-VideoBatch -BatchName week2
```

---

## File Reference

| File | Purpose | Usage |
|------|---------|-------|
| `content_production_pipeline.py` | Generate batches + schedule publishing | `python content_production_pipeline.py --topic "..." --count 5 --batch-name week1` |
| `monetization_hooks.py` | Add CTAs, affiliate links, sponsorship text | `python monetization_hooks.py --batch week1 --inject` |
| `social_analytics_dashboard.py` | Track views, engagement, revenue | `python social_analytics_dashboard.py --show` |
| `social_media_helpers.ps1` | PowerShell shortcut functions | `. .\social_media_helpers.ps1` then use functions |
| `SOCIAL_MEDIA_GROWTH_GUIDE.md` | Detailed workflows and strategies | Read for full monetization plan |

---

## Key Concepts

### Batch
A set of 5-10 video variations from one topic. Example:
```
week1/
  ├── video_1/  ("Dating advice for men")
  ├── video_2/  ("Why you're single")
  ├── video_3/  ("5 signs she likes you")
  └── manifest.json  (metadata + monetized descriptions)
```

### Schedule
Defines when each video publishes. Example:
```
video_1 → publishes 2025-12-09
video_2 → publishes 2025-12-10
video_3 → publishes 2025-12-11
(daily intervals)
```

### Monetization Hooks
Describes what CTAs/links appear in each description:
- LoveGuard CTA at top/middle/bottom
- Affiliate links (Bumble, Match, etc.)
- Sponsorship text (when enabled)
- Platform-specific CTAs

---

## Workflow Examples

### Weekly Content Creation
```powershell
# Monday: Generate batch
Generate-VideoBatch -Topic "relationship psychology" -Count 5 -BatchName week12

# Tuesday: Add monetization
Add-MonetizationHooks -BatchName week12

# Wednesday: Schedule
Schedule-VideoBatch -BatchName week12 -Interval daily

# Daily: Check if anything published
Publish-Scheduled -DryRun

# Friday: Review analytics
Get-Analytics
```

### Scaling to 100+ Videos
```powershell
# Week 1: 5 videos
# Week 2: 10 videos
# Week 3: 15 videos
# ...
# Week 10: 50+ total videos publishing daily

# By month 3: Videos auto-publishing daily = 50k+ views/week = passive income
```

### Recording Revenue
```powershell
# When YouTube sends AdSense payment
Record-Revenue -Type adsense -Platform youtube -Amount 250.00

# When affiliate link converts
Record-Revenue -Type affiliate -Platform dating_apps -Amount 15.00

# When LoveGuard user signs up via your link
Record-Revenue -Type loveguard_referral -Platform loveguard -Amount 8.50
```

---

## Directory Structure

```
content_automation_ai/
├── content_production_pipeline.py
├── monetization_hooks.py
├── social_analytics_dashboard.py
├── social_media_helpers.ps1
├── SOCIAL_MEDIA_GROWTH_GUIDE.md
│
├── content_production/
│   ├── batches/
│   │   ├── week1/
│   │   │   ├── video_1/ (generated video files)
│   │   │   ├── video_2/
│   │   │   └── manifest.json
│   │   ├── week2/
│   │   └── ...
│   ├── schedule.json
│   └── monetization_hooks.json
│
├── social_analytics/
│   ├── platform_stats.json (followers, views by platform)
│   ├── video_performance.json (views, likes, comments per video)
│   ├── audience_growth.json (daily snapshots)
│   └── monetization_summary.json (revenue tracking)
```

---

## Analytics Interpretation

**From `python social_analytics_dashboard.py --show`:**

```
📊 SOCIAL MEDIA ANALYTICS DASHBOARD

👥 AUDIENCE
  Total Followers: 125,000
  Total Views: 2,500,000
  Growth (snapshot): +5,000 followers (from last snapshot)

📱 PLATFORM BREAKDOWN
  YOUTUBE: 75,000 followers | 1,500,000 views | 4.5% engagement
  TIKTOK: 35,000 followers | 800,000 views | 8.2% engagement
  INSTAGRAM: 10,000 followers | 150,000 views | 6.1% engagement
  TWITTER: 5,000 followers | 50,000 views | 3.2% engagement

💰 MONETIZATION
  Total Revenue: $3,847.50
  YouTube AdSense: $2,500.00
  Affiliate Links: $897.50
  LoveGuard Referrals: $300.00
  Sponsorships: $150.00
```

---

## Troubleshooting

### Error: "Batch not found"
- Check: `ls content_production/batches/`
- Make sure batch name matches exactly

### Schedule not working
- Check: `cat content_production/schedule.json`
- Manually test: `python content_production_pipeline.py --publish --dry-run`

### Revenue not tracking
- Initialize: `python social_analytics_dashboard.py --show`
- Then manually log: `python social_analytics_dashboard.py --record-revenue youtube_adsense --platform youtube --amount 100`

### Videos not generating
- Check API keys: `echo $env:OPENAI_API_KEY`
- Install dependencies: `pip install -r requirements.txt`

---

## Next Steps

1. **Read** `SOCIAL_MEDIA_GROWTH_GUIDE.md` for detailed monetization strategy
2. **Generate first batch** → `Generate-VideoBatch -Topic "your topic" -Count 5`
3. **Add hooks** → `Add-MonetizationHooks -BatchName week1`
4. **Schedule** → `Schedule-VideoBatch -BatchName week1`
5. **Monitor** → `Get-Analytics` (weekly)
6. **Repeat weekly** to build library

---

## Revenue Timeline (Estimate)

| Timeline | Followers | Views/Month | Revenue/Month |
|----------|-----------|-------------|--------------|
| Month 1 | 1,000 | 50,000 | $50 (affiliates) |
| Month 3 | 10,000 | 250,000 | $300 (ads + affiliates) |
| Month 6 | 50,000 | 1,000,000 | $1,500 (diversified) |
| Month 12 | 200,000 | 3,000,000 | $5,000+ (scaled) |

*Actual results depend on niche, consistency, and content quality.*

---

**Questions?** See the docstrings in each Python script for detailed usage examples.

**Ready?** Start with: `Generate-VideoBatch -Topic "relationship advice" -Count 5 -BatchName week1`
