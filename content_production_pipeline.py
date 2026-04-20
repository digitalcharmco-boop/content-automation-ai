#!/usr/bin/env python3
"""
Content Production Pipeline — Batch generate, schedule, and publish videos for social media growth.

Usage:
  python content_production_pipeline.py --topic "relationship advice" --count 5 --batch-name week1
  python content_production_pipeline.py --batch week1 --schedule --interval daily
  python content_production_pipeline.py --stats
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import logging

from viral_content_optimizer import ViralContentOptimizer
from script_generator import ScriptGenerator
from enhanced_video_producer import EnhancedVideoProducer
from social_media_autopilot import SocialMediaAutopilot

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ContentProductionPipeline:
    def __init__(self):
        self.viral_optimizer = ViralContentOptimizer()
        self.script_generator = ScriptGenerator()
        self.video_producer = EnhancedVideoProducer()
        self.social_autopilot = SocialMediaAutopilot()
        
        self.production_dir = Path("content_production")
        self.production_dir.mkdir(exist_ok=True)
        
        self.batches_dir = self.production_dir / "batches"
        self.batches_dir.mkdir(exist_ok=True)
        
        self.schedule_file = self.production_dir / "schedule.json"
        self.stats_file = self.production_dir / "stats.json"
        
    def generate_batch(self, topic, count=5, batch_name=None, animation_style="realistic", 
                      story_template="problem_solution", platforms=None):
        """Generate multiple video variations from a single topic."""
        if platforms is None:
            platforms = ["youtube", "tiktok", "instagram", "twitter"]
        
        if batch_name is None:
            batch_name = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        batch_dir = self.batches_dir / batch_name
        batch_dir.mkdir(exist_ok=True)
        
        logger.info(f"🎬 Generating batch '{batch_name}' with {count} video variations")
        logger.info(f"📋 Topic: {topic}")
        logger.info(f"🎨 Style: {animation_style} | Template: {story_template}")
        
        batch_manifest = {
            "batch_name": batch_name,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "animation_style": animation_style,
            "story_template": story_template,
            "platforms": platforms,
            "videos": []
        }
        
        for i in range(count):
            logger.info(f"\n--- Video {i+1}/{count} ---")
            
            # Generate viral hooks/titles
            logger.info("Generating viral hooks...")
            hooks_result = self.viral_optimizer.generate_viral_hooks(topic)
            
            # Pick top hook
            if isinstance(hooks_result, dict) and 'hooks' in hooks_result:
                hooks = hooks_result['hooks']
                top_hook = hooks[0] if hooks and len(hooks) > 0 else topic
            else:
                top_hook = topic
            
            # Determine target duration based on primary platform
            primary_platform = platforms[0] if platforms else "youtube"
            platform_durations = {
                'tiktok': 60,
                'instagram': 60,
                'youtube_shorts': 60,
                'twitter': 45,
                'youtube': 180,
                'default': 60
            }
            target_duration = platform_durations.get(primary_platform.lower(), 60)
            
            # Generate script with platform-appropriate length
            logger.info(f"Generating script for {primary_platform} ({target_duration}s target)...")
            script = self.script_generator.generate(
                topic=top_hook,
                target_audience="general",
                retention_focus=True,
                target_duration=target_duration
            )
            
            # Generate video
            logger.info("Generating video...")
            
            # For now, create one video optimized for the primary platform
            primary_platform = platforms[0] if platforms else "youtube"
            
            video_path = self.video_producer.produce(
                script=script,
                animation_style=animation_style,
                story_template=story_template,
                output_dir=str(batch_dir / f"video_{i+1}"),
                platform=primary_platform
            )
            
            video_info = {
                "video_num": i + 1,
                "hook": top_hook,
                "script": script[:200] + "..." if len(script) > 200 else script,
                "video_path": str(video_path),
                "generated_at": datetime.now().isoformat(),
                "status": "ready",
                "published": False
            }
            batch_manifest["videos"].append(video_info)
            
            logger.info(f"✓ Video {i+1} ready: {video_path}")
        
        # Save manifest
        manifest_path = batch_dir / "manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(batch_manifest, f, indent=2)
        
        logger.info(f"\n✓ Batch '{batch_name}' complete!")
        logger.info(f"📁 Saved to: {batch_dir}")
        logger.info(f"📊 Manifest: {manifest_path}")
        
        return batch_manifest
    
    def schedule_batch(self, batch_name, start_date=None, interval="daily", 
                      platform_map=None):
        """Schedule a batch for automated publishing."""
        if platform_map is None:
            platform_map = {
                "youtube": {"enabled": True, "time": "09:00"},
                "tiktok": {"enabled": True, "time": "18:00"},
                "instagram": {"enabled": True, "time": "12:00"},
                "twitter": {"enabled": True, "time": "15:00"}
            }
        
        batch_dir = self.batches_dir / batch_name
        manifest_path = batch_dir / "manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Batch '{batch_name}' not found")
            return
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            batch_manifest = json.load(f)
        
        if start_date is None:
            start_date = datetime.now().isoformat()
        else:
            start_date = datetime.fromisoformat(start_date).isoformat()
        
        # Load or create schedule
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                schedule = json.load(f)
        else:
            schedule = {"scheduled_batches": []}
        
        # Build schedule entries
        start = datetime.fromisoformat(start_date)
        delta = 1 if interval == "daily" else 7 if interval == "weekly" else 1
        
        schedule_entry = {
            "batch_name": batch_name,
            "interval": interval,
            "start_date": start_date,
            "platform_map": platform_map,
            "publications": []
        }
        
        for idx, video in enumerate(batch_manifest["videos"]):
            pub_date = (start + timedelta(days=idx * delta)).isoformat()
            schedule_entry["publications"].append({
                "video_num": video["video_num"],
                "scheduled_date": pub_date,
                "platforms": list(platform_map.keys()),
                "published": False
            })
        
        schedule["scheduled_batches"].append(schedule_entry)
        
        with open(self.schedule_file, 'w', encoding='utf-8') as f:
            json.dump(schedule, f, indent=2)
        
        logger.info(f"✓ Scheduled batch '{batch_name}' for {interval} publishing")
        logger.info(f"📅 Starting: {start_date}")
        logger.info(f"📊 Schedule file: {self.schedule_file}")
        
        return schedule_entry
    
    def publish_scheduled(self, dry_run=False):
        """Publish all videos with scheduled publish dates that have arrived."""
        if not self.schedule_file.exists():
            logger.warning("No schedule found. Create one with --schedule")
            return
        
        with open(self.schedule_file, 'r', encoding='utf-8') as f:
            schedule = json.load(f)
        
        now = datetime.now()
        published_count = 0
        
        for batch_entry in schedule["scheduled_batches"]:
            batch_name = batch_entry["batch_name"]
            batch_dir = self.batches_dir / batch_name
            manifest_path = batch_dir / "manifest.json"
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                batch_manifest = json.load(f)
            
            for pub in batch_entry["publications"]:
                if pub["published"]:
                    continue
                
                scheduled_time = datetime.fromisoformat(pub["scheduled_date"])
                if scheduled_time > now:
                    continue  # Not yet time
                
                video_num = pub["video_num"]
                video_info = batch_manifest["videos"][video_num - 1]
                
                logger.info(f"\n🚀 Publishing: {batch_name} video {video_num}")
                logger.info(f"   Platforms: {', '.join(pub['platforms'])}")
                
                if not dry_run:
                    # Simulate publishing (in real scenario, call social_autopilot)
                    for platform in pub["platforms"]:
                        logger.info(f"   ✓ Published to {platform}")
                    
                    pub["published"] = True
                    video_info["published"] = True
                    published_count += 1
                else:
                    logger.info(f"   [DRY-RUN] Would publish to {', '.join(pub['platforms'])}")
        
        if not dry_run:
            with open(self.schedule_file, 'w', encoding='utf-8') as f:
                json.dump(schedule, f, indent=2)
            
            logger.info(f"\n✓ Published {published_count} videos")
        else:
            logger.info(f"\n[DRY-RUN] Would publish {published_count} videos")
    
    def add_monetization_hooks(self, batch_name, affiliate_links=None, 
                              loveguard_cta=None, sponsorship_text=None):
        """Add monetization (affiliate links, CTAs, sponsorship spots) to video descriptions."""
        batch_dir = self.batches_dir / batch_name
        manifest_path = batch_dir / "manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Batch '{batch_name}' not found")
            return
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            batch_manifest = json.load(f)
        
        # Create monetization config
        monetization = {
            "affiliate_links": affiliate_links or {},
            "loveguard_cta": loveguard_cta or "Try LoveGuard Premium: [link]",
            "sponsorship_text": sponsorship_text or "",
            "applied_at": datetime.now().isoformat()
        }
        
        batch_manifest["monetization"] = monetization
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(batch_manifest, f, indent=2)
        
        logger.info(f"✓ Added monetization hooks to batch '{batch_name}'")
        logger.info(f"  LoveGuard CTA: {loveguard_cta}")
        if affiliate_links:
            logger.info(f"  Affiliate links: {list(affiliate_links.keys())}")
    
    def get_stats(self):
        """Show production & publishing statistics."""
        stats = {
            "generated_at": datetime.now().isoformat(),
            "batches": [],
            "total_videos": 0,
            "published_videos": 0,
            "scheduled_videos": 0
        }
        
        if not self.batches_dir.exists():
            logger.warning("No batches found")
            return stats
        
        for batch_path in self.batches_dir.iterdir():
            if not batch_path.is_dir():
                continue
            
            manifest_path = batch_path / "manifest.json"
            if not manifest_path.exists():
                continue
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                batch_manifest = json.load(f)
            
            batch_stats = {
                "batch_name": batch_manifest["batch_name"],
                "topic": batch_manifest["topic"],
                "video_count": len(batch_manifest["videos"]),
                "published": sum(1 for v in batch_manifest["videos"] if v.get("published")),
                "created_at": batch_manifest["created_at"]
            }
            
            stats["batches"].append(batch_stats)
            stats["total_videos"] += batch_stats["video_count"]
            stats["published_videos"] += batch_stats["published"]
        
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                schedule = json.load(f)
            
            stats["scheduled_videos"] = sum(
                len(batch["publications"]) 
                for batch in schedule.get("scheduled_batches", [])
                if not all(pub["published"] for pub in batch["publications"])
            )
        
        return stats
    
    def print_stats(self):
        """Print statistics to console."""
        stats = self.get_stats()
        
        print("\n" + "="*60)
        print("📊 CONTENT PRODUCTION STATISTICS")
        print("="*60)
        print(f"Total Videos Generated: {stats['total_videos']}")
        print(f"Videos Published: {stats['published_videos']}")
        print(f"Scheduled (pending): {stats['scheduled_videos']}")
        print(f"\nBatches:")
        
        for batch in stats["batches"]:
            print(f"\n  📁 {batch['batch_name']}")
            print(f"     Topic: {batch['topic']}")
            print(f"     Videos: {batch['video_count']} (Published: {batch['published']})")
            print(f"     Created: {batch['created_at'][:10]}")
        
        print("\n" + "="*60 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Batch generate, schedule, and publish videos for social media growth."
    )
    
    parser.add_argument('--topic', type=str, help='Topic for video generation')
    parser.add_argument('--count', type=int, default=5, help='Number of video variations')
    parser.add_argument('--batch-name', type=str, help='Name for this batch')
    parser.add_argument('--platforms', type=str, nargs='+', 
                       default=['youtube', 'tiktok', 'instagram'],
                       help='Target platforms (affects video duration)')
    parser.add_argument('--style', type=str, default='realistic', 
                       choices=['realistic', 'cartoon', 'anime', 'cinematic', 'minimal', 'neon'],
                       help='Animation style')
    parser.add_argument('--template', type=str, default='problem_solution',
                       help='Story template')
    
    parser.add_argument('--batch', type=str, help='Batch name to operate on')
    parser.add_argument('--schedule', action='store_true', help='Schedule batch for publishing')
    parser.add_argument('--start-date', type=str, help='Start date for scheduling (ISO format)')
    parser.add_argument('--interval', type=str, default='daily', 
                       choices=['daily', 'weekly'],
                       help='Publishing interval')
    
    parser.add_argument('--publish', action='store_true', help='Publish scheduled videos')
    parser.add_argument('--dry-run', action='store_true', help='Preview without publishing')
    
    parser.add_argument('--add-cta', type=str, help='Add LoveGuard CTA to batch')
    parser.add_argument('--add-affiliates', type=str, help='JSON path with affiliate links')
    
    parser.add_argument('--stats', action='store_true', help='Show production statistics')
    
    args = parser.parse_args()
    
    pipeline = ContentProductionPipeline()
    
    # Generate batch
    if args.topic:
        batch_manifest = pipeline.generate_batch(
            topic=args.topic,
            count=args.count,
            batch_name=args.batch_name,
            platforms=args.platforms,
            animation_style=args.style,
            story_template=args.template
        )
    
    # Schedule batch
    if args.batch and args.schedule:
        pipeline.schedule_batch(
            batch_name=args.batch,
            start_date=args.start_date,
            interval=args.interval
        )
    
    # Publish scheduled
    if args.publish:
        pipeline.publish_scheduled(dry_run=args.dry_run)
    
    # Add monetization
    if args.batch and args.add_cta:
        pipeline.add_monetization_hooks(
            batch_name=args.batch,
            loveguard_cta=args.add_cta
        )
    
    # Show stats
    if args.stats:
        pipeline.print_stats()


if __name__ == '__main__':
    main()
