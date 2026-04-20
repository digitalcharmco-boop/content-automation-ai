#!/usr/bin/env python3
"""
Initialize Social Media Growth System — First-time setup and test.

Usage:
  python init_growth_system.py --test          # Test full workflow
  python init_growth_system.py --help          # Show examples
"""

import json
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def init_directories():
    """Create all required directories."""
    dirs = [
        Path("content_production"),
        Path("content_production/batches"),
        Path("social_analytics"),
    ]
    
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
    
    logger.info("✓ Directories initialized")


def init_configs():
    """Initialize all config files."""
    
    # Monetization hooks config
    monetization_hooks = {
        "loveguard_cta": {
            "enabled": True,
            "text": "Join 10k+ on LoveGuard for relationship insights: [LOVEGUARD_LINK]",
            "placement": "middle"
        },
        "affiliate_links": {
            "dating_apps": {
                "enabled": True,
                "links": {
                    "bumble": "https://bumble.com?ref=yourname",
                    "match": "https://match.com?ref=yourname",
                    "hinge": "https://hinge.com?ref=yourname"
                }
            }
        },
        "sponsorships": {
            "enabled": False,
            "text": "[SPONSOR MESSAGE]",
            "placement": "top"
        },
        "cta_templates": {
            "youtube": "Subscribe for weekly relationship & dating tips! 💕",
            "tiktok": "Follow for daily dating and relationship advice! 💕",
            "instagram": "DM us your dating questions! 💕",
            "twitter": "Like & Retweet if this helped! 💕"
        }
    }
    
    hooks_path = Path("content_production/monetization_hooks.json")
    with open(hooks_path, 'w') as f:
        json.dump(monetization_hooks, f, indent=2)
    logger.info(f"✓ Created {hooks_path}")
    
    # Analytics files
    analytics_files = {
        "social_analytics/platform_stats.json": {
            "youtube": {"followers": 0, "views": 0, "engagement_rate": 0},
            "tiktok": {"followers": 0, "views": 0, "engagement_rate": 0},
            "instagram": {"followers": 0, "views": 0, "engagement_rate": 0},
            "twitter": {"followers": 0, "views": 0, "engagement_rate": 0}
        },
        "social_analytics/audience_growth.json": {"snapshots": []},
        "social_analytics/video_performance.json": {"videos": []},
        "social_analytics/monetization_summary.json": {
            "total_revenue": 0,
            "affiliate_earnings": 0,
            "youtube_adsense": 0,
            "loveguard_referrals": 0,
            "sponsorships": 0,
            "transactions": []
        }
    }
    
    for file_path, content in analytics_files.items():
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=2)
    logger.info(f"✓ Created analytics files")


def show_quick_start():
    """Display quick start instructions."""
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                     SOCIAL MEDIA GROWTH SYSTEM READY                       ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 QUICK START:

1. Load PowerShell helpers:
   . .\social_media_helpers.ps1

2. Generate your first batch:
   Generate-VideoBatch -Topic "relationship advice for men" -Count 5 -BatchName week1

3. Add monetization hooks:
   Add-MonetizationHooks -BatchName week1

4. Schedule for publishing:
   Schedule-VideoBatch -BatchName week1 -Interval daily

5. Check analytics:
   Get-Analytics

📖 DOCUMENTATION:
   - GROWTH_SYSTEM_README.md      ← Start here
   - SOCIAL_MEDIA_GROWTH_GUIDE.md ← Detailed strategies

📊 AVAILABLE COMMANDS:
   Generate-VideoBatch, Add-MonetizationHooks, Schedule-VideoBatch,
   Publish-Scheduled, Get-Analytics, Record-VideoMetrics, Record-Revenue,
   Export-Analytics, Quick-FullWorkflow

💡 EXAMPLE WORKFLOWS:

   # One-liner workflow
   Quick-FullWorkflow -Topic "how to text girls" -Count 5

   # Manual control
   Generate-VideoBatch -Topic "dating psychology" -Count 10 -BatchName week2
   Add-MonetizationHooks -BatchName week2 -LoveGuardCTA "Join our community!"
   Schedule-VideoBatch -BatchName week2 -Interval daily -StartDate "2025-12-09"
   Publish-Scheduled

   # Track revenue
   Record-Revenue -Type adsense -Platform youtube -Amount 250.00
   Record-Revenue -Type affiliate -Platform dating_apps -Amount 45.50
   Get-Analytics
   Export-Analytics -OutputFile weekly_report.csv

═══════════════════════════════════════════════════════════════════════════════
    """)


def test_workflow():
    """Run a complete test workflow."""
    print("\n" + "="*80)
    print("🧪 RUNNING TEST WORKFLOW")
    print("="*80 + "\n")
    
    # Create test batch
    print("Step 1: Creating test batch...")
    try:
        subprocess.run(
            [sys.executable, "content_production_pipeline.py",
             "--topic", "dating tips for beginners",
             "--count", "2",
             "--batch-name", "test_run"],
            check=False
        )
    except Exception as e:
        logger.warning(f"Test video generation skipped (dependencies may not be ready): {e}")
        print("   Note: Full video generation requires OpenAI API key")
        print("   To test, set: set OPENAI_API_KEY=your_key")
    
    # Initialize analytics
    print("\nStep 2: Initializing analytics...")
    subprocess.run(
        [sys.executable, "social_analytics_dashboard.py", "--show"],
        check=False
    )
    
    # Show monetization config
    print("\nStep 3: Showing monetization config...")
    subprocess.run(
        [sys.executable, "monetization_hooks.py", "--config"],
        check=False
    )
    
    # Show help
    print("\nStep 4: Next, run these commands:")
    print("   Load helpers: . .\social_media_helpers.ps1")
    print("   Generate batch: Generate-VideoBatch -Topic 'your topic' -Count 5 -BatchName week1")
    print("   Add hooks: Add-MonetizationHooks -BatchName week1")
    print("   Schedule: Schedule-VideoBatch -BatchName week1")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialize Social Media Growth System"
    )
    parser.add_argument("--test", action="store_true", help="Run test workflow")
    parser.add_argument("--help-extended", action="store_true", help="Show all examples")
    
    args = parser.parse_args()
    
    # Initialize
    logger.info("Initializing Social Media Growth System...\n")
    
    init_directories()
    init_configs()
    
    if args.test:
        test_workflow()
    elif args.help_extended:
        show_quick_start()
    else:
        show_quick_start()
        print("\n✓ System initialized! Run: . .\social_media_helpers.ps1")


if __name__ == "__main__":
    main()
