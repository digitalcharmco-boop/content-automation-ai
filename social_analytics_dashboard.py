#!/usr/bin/env python3
"""
Analytics Dashboard — Track video performance, engagement, and follower growth.

Usage:
  python social_analytics_dashboard.py --update  # Fetch latest stats from platforms
  python social_analytics_dashboard.py --show    # Display dashboard
  python social_analytics_dashboard.py --export csv  # Export to CSV
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SocialAnalyticsDashboard:
    def __init__(self):
        self.analytics_dir = Path("social_analytics")
        self.analytics_dir.mkdir(exist_ok=True)
        
        self.platform_stats_file = self.analytics_dir / "platform_stats.json"
        self.video_performance_file = self.analytics_dir / "video_performance.json"
        self.audience_growth_file = self.analytics_dir / "audience_growth.json"
        self.monetization_file = self.analytics_dir / "monetization_summary.json"
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Create default analytics files if they don't exist."""
        if not self.platform_stats_file.exists():
            default_platforms = {
                "youtube": {"followers": 0, "views": 0, "engagement_rate": 0},
                "tiktok": {"followers": 0, "views": 0, "engagement_rate": 0},
                "instagram": {"followers": 0, "views": 0, "engagement_rate": 0},
                "twitter": {"followers": 0, "views": 0, "engagement_rate": 0}
            }
            with open(self.platform_stats_file, 'w') as f:
                json.dump(default_platforms, f, indent=2)
        
        if not self.audience_growth_file.exists():
            with open(self.audience_growth_file, 'w') as f:
                json.dump({"snapshots": []}, f, indent=2)
        
        if not self.video_performance_file.exists():
            with open(self.video_performance_file, 'w') as f:
                json.dump({"videos": []}, f, indent=2)
        
        if not self.monetization_file.exists():
            with open(self.monetization_file, 'w') as f:
                json.dump({
                    "total_revenue": 0,
                    "affiliate_earnings": 0,
                    "youtube_adsense": 0,
                    "loveguard_referrals": 0,
                    "sponsorships": 0,
                    "transactions": []
                }, f, indent=2)
    
    def track_video_performance(self, video_id, platform, title, views=0, likes=0, 
                               comments=0, shares=0, engagement_rate=0):
        """Log individual video performance."""
        with open(self.video_performance_file, 'r') as f:
            data = json.load(f)
        
        video_entry = {
            "video_id": video_id,
            "platform": platform,
            "title": title,
            "views": views,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "engagement_rate": engagement_rate,
            "tracked_at": datetime.now().isoformat()
        }
        
        data["videos"].append(video_entry)
        
        with open(self.video_performance_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✓ Tracked: {title} on {platform} ({views} views)")
    
    def update_platform_stats(self, platform, followers, total_views, engagement_rate):
        """Update aggregated platform statistics."""
        with open(self.platform_stats_file, 'r') as f:
            platforms = json.load(f)
        
        if platform in platforms:
            platforms[platform] = {
                "followers": followers,
                "views": total_views,
                "engagement_rate": engagement_rate,
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.platform_stats_file, 'w') as f:
                json.dump(platforms, f, indent=2)
            
            logger.info(f"✓ Updated {platform}: {followers} followers, {total_views} views")
    
    def snapshot_audience_growth(self):
        """Create a daily snapshot of audience growth across platforms."""
        with open(self.platform_stats_file, 'r') as f:
            platforms = json.load(f)
        
        with open(self.audience_growth_file, 'r') as f:
            growth_data = json.load(f)
        
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "platforms": platforms
        }
        
        growth_data["snapshots"].append(snapshot)
        
        with open(self.audience_growth_file, 'w') as f:
            json.dump(growth_data, f, indent=2)
        
        logger.info("✓ Captured audience growth snapshot")
    
    def record_monetization(self, transaction_type, platform, amount, details=None):
        """Record revenue from any source (ads, affiliates, sponsorships, referrals)."""
        with open(self.monetization_file, 'r') as f:
            mon_data = json.load(f)
        
        transaction = {
            "type": transaction_type,  # adsense, affiliate, sponsorship, loveguard_referral
            "platform": platform,
            "amount": amount,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        
        mon_data["transactions"].append(transaction)
        mon_data["total_revenue"] += amount
        
        # Update category totals
        if transaction_type == "youtube_adsense":
            mon_data["youtube_adsense"] += amount
        elif transaction_type == "affiliate":
            mon_data["affiliate_earnings"] += amount
        elif transaction_type == "sponsorship":
            mon_data["sponsorships"] += amount
        elif transaction_type == "loveguard_referral":
            mon_data["loveguard_referrals"] += amount
        
        with open(self.monetization_file, 'w') as f:
            json.dump(mon_data, f, indent=2)
        
        logger.info(f"✓ Recorded {transaction_type}: ${amount:.2f}")
    
    def get_dashboard_data(self):
        """Aggregate all analytics for dashboard display."""
        with open(self.platform_stats_file, 'r') as f:
            platforms = json.load(f)
        
        with open(self.video_performance_file, 'r') as f:
            video_data = json.load(f)
        
        with open(self.audience_growth_file, 'r') as f:
            growth_data = json.load(f)
        
        with open(self.monetization_file, 'r') as f:
            mon_data = json.load(f)
        
        # Calculate growth metrics
        total_followers = sum(p.get("followers", 0) for p in platforms.values())
        total_views = sum(p.get("views", 0) for p in platforms.values())
        
        growth_snapshots = growth_data.get("snapshots", [])
        follower_growth = 0
        if len(growth_snapshots) > 1:
            current = sum(p.get("followers", 0) for p in growth_snapshots[-1].get("platforms", {}).values())
            previous = sum(p.get("followers", 0) for p in growth_snapshots[-2].get("platforms", {}).values())
            follower_growth = current - previous
        
        # Top performing videos
        videos = sorted(
            video_data.get("videos", []),
            key=lambda v: v.get("views", 0),
            reverse=True
        )[:5]
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_followers": total_followers,
            "total_views": total_views,
            "follower_growth_snapshot": follower_growth,
            "platforms": platforms,
            "top_videos": videos,
            "monetization": {
                "total_revenue": mon_data.get("total_revenue", 0),
                "youtube_adsense": mon_data.get("youtube_adsense", 0),
                "affiliate_earnings": mon_data.get("affiliate_earnings", 0),
                "loveguard_referrals": mon_data.get("loveguard_referrals", 0),
                "sponsorships": mon_data.get("sponsorships", 0)
            }
        }
    
    def print_dashboard(self):
        """Print formatted dashboard to console."""
        dashboard = self.get_dashboard_data()
        
        print("\n" + "="*70)
        print("📊 SOCIAL MEDIA ANALYTICS DASHBOARD")
        print("="*70)
        
        print(f"\n👥 AUDIENCE")
        print(f"  Total Followers: {dashboard['total_followers']:,}")
        print(f"  Total Views: {dashboard['total_views']:,}")
        print(f"  Growth (snapshot): +{dashboard['follower_growth_snapshot']:,} followers")
        
        print(f"\n📱 PLATFORM BREAKDOWN")
        for platform, stats in dashboard["platforms"].items():
            print(f"  {platform.upper()}")
            print(f"    Followers: {stats.get('followers', 0):,}")
            print(f"    Views: {stats.get('views', 0):,}")
            print(f"    Engagement: {stats.get('engagement_rate', 0):.1f}%")
        
        print(f"\n🎬 TOP PERFORMING VIDEOS")
        for idx, video in enumerate(dashboard["top_videos"], 1):
            print(f"  {idx}. {video['title'][:50]}")
            print(f"     Platform: {video['platform']} | Views: {video['views']:,} | Engagement: {video['engagement_rate']:.1f}%")
        
        print(f"\n💰 MONETIZATION")
        mon = dashboard["monetization"]
        print(f"  Total Revenue: ${mon['total_revenue']:.2f}")
        print(f"  YouTube AdSense: ${mon['youtube_adsense']:.2f}")
        print(f"  Affiliate Links: ${mon['affiliate_earnings']:.2f}")
        print(f"  LoveGuard Referrals: ${mon['loveguard_referrals']:.2f}")
        print(f"  Sponsorships: ${mon['sponsorships']:.2f}")
        
        print("\n" + "="*70 + "\n")
    
    def export_csv(self, output_file="analytics_export.csv"):
        """Export analytics to CSV."""
        import csv
        
        dashboard = self.get_dashboard_data()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow(["Analytics Export", datetime.now().isoformat()])
            writer.writerow([])
            
            # Summary
            writer.writerow(["Metric", "Value"])
            writer.writerow(["Total Followers", dashboard["total_followers"]])
            writer.writerow(["Total Views", dashboard["total_views"]])
            writer.writerow(["Total Revenue", f"${dashboard['monetization']['total_revenue']:.2f}"])
            writer.writerow([])
            
            # Platform breakdown
            writer.writerow(["Platform", "Followers", "Views", "Engagement %"])
            for platform, stats in dashboard["platforms"].items():
                writer.writerow([
                    platform,
                    stats.get("followers", 0),
                    stats.get("views", 0),
                    f"{stats.get('engagement_rate', 0):.1f}"
                ])
            
            writer.writerow([])
            writer.writerow(["Top Videos"])
            writer.writerow(["Title", "Platform", "Views", "Likes", "Comments", "Engagement %"])
            for video in dashboard["top_videos"]:
                writer.writerow([
                    video["title"],
                    video["platform"],
                    video["views"],
                    video["likes"],
                    video["comments"],
                    f"{video['engagement_rate']:.1f}"
                ])
        
        logger.info(f"✓ Exported analytics to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Track and display social media analytics")
    
    parser.add_argument('--track-video', type=str, help='Video ID to track')
    parser.add_argument('--platform', type=str, help='Platform (youtube, tiktok, instagram, twitter)')
    parser.add_argument('--title', type=str, help='Video title')
    parser.add_argument('--views', type=int, default=0)
    parser.add_argument('--likes', type=int, default=0)
    parser.add_argument('--comments', type=int, default=0)
    parser.add_argument('--shares', type=int, default=0)
    parser.add_argument('--engagement', type=float, default=0)
    
    parser.add_argument('--update-platform', type=str, help='Update platform stats')
    parser.add_argument('--followers', type=int, help='Follower count')
    parser.add_argument('--total-views', type=int, help='Total platform views')
    parser.add_argument('--engagement-rate', type=float, help='Average engagement rate')
    
    parser.add_argument('--snapshot', action='store_true', help='Capture growth snapshot')
    
    parser.add_argument('--record-revenue', type=str, help='Revenue type (adsense, affiliate, sponsorship, loveguard_referral)')
    parser.add_argument('--amount', type=float, help='Revenue amount')
    
    parser.add_argument('--show', action='store_true', help='Show dashboard')
    parser.add_argument('--export', type=str, default=None, help='Export to CSV')
    
    args = parser.parse_args()
    
    dashboard = SocialAnalyticsDashboard()
    
    # Track video
    if args.track_video:
        dashboard.track_video_performance(
            video_id=args.track_video,
            platform=args.platform or "youtube",
            title=args.title or "Untitled",
            views=args.views,
            likes=args.likes,
            comments=args.comments,
            shares=args.shares,
            engagement_rate=args.engagement
        )
    
    # Update platform
    if args.update_platform:
        dashboard.update_platform_stats(
            platform=args.update_platform,
            followers=args.followers or 0,
            total_views=args.total_views or 0,
            engagement_rate=args.engagement_rate or 0
        )
    
    # Snapshot growth
    if args.snapshot:
        dashboard.snapshot_audience_growth()
    
    # Record revenue
    if args.record_revenue:
        dashboard.record_monetization(
            transaction_type=args.record_revenue,
            platform=args.platform or "unknown",
            amount=args.amount or 0
        )
    
    # Show dashboard
    if args.show:
        dashboard.print_dashboard()
    
    # Export
    if args.export:
        dashboard.export_csv(output_file=args.export)


if __name__ == '__main__':
    main()
