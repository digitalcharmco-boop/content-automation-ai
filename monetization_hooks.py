#!/usr/bin/env python3
"""
Monetization Hooks — Auto-inject LoveGuard CTAs, affiliate links, and sponsorship text into video descriptions.

Usage:
  python monetization_hooks.py --batch week1 --add-loveguard "Try LoveGuard: [link]"
  python monetization_hooks.py --batch week1 --add-affiliate dating "https://dating-app.com/ref=you"
  python monetization_hooks.py --generate-descriptions --batch week1
"""

import json
import argparse
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MonetizationHooks:
    def __init__(self):
        self.batches_dir = Path("content_production") / "batches"
        self.hooks_config_file = Path("content_production") / "monetization_hooks.json"
        self._initialize_config()
    
    def _initialize_config(self):
        """Create default hooks config if it doesn't exist."""
        if not self.hooks_config_file.exists():
            default_config = {
                "loveguard_cta": {
                    "enabled": True,
                    "text": "Try LoveGuard Premium and unlock relationship insights: [LOVEGUARD_LINK]",
                    "placement": "middle"  # top, middle, bottom
                },
                "affiliate_links": {
                    "dating_apps": {
                        "enabled": True,
                        "links": {
                            "match": "https://www.match.com?ref=yourname",
                            "bumble": "https://bumble.com?ref=yourname"
                        }
                    }
                },
                "sponsorships": {
                    "enabled": False,
                    "text": "[SPONSOR_MESSAGE]",
                    "placement": "top"
                },
                "cta_templates": {
                    "youtube": "Subscribe for more dating & relationship tips! 💕",
                    "tiktok": "Follow for daily relationship advice! 💕",
                    "instagram": "DM us your dating questions! 💕",
                    "twitter": "Retweet if you found this helpful! 💕"
                }
            }
            
            with open(self.hooks_config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2)
            
            logger.info(f"Created default hooks config: {self.hooks_config_file}")
    
    def load_config(self):
        """Load monetization hooks config."""
        with open(self.hooks_config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self, config):
        """Save monetization hooks config."""
        with open(self.hooks_config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
    def update_loveguard_cta(self, text, placement="middle"):
        """Update LoveGuard CTA text and placement."""
        config = self.load_config()
        config["loveguard_cta"]["text"] = text
        config["loveguard_cta"]["placement"] = placement
        self.save_config(config)
        logger.info(f"✓ Updated LoveGuard CTA: {text[:50]}...")
    
    def add_affiliate_link(self, category, platform_name, url):
        """Add an affiliate link."""
        config = self.load_config()
        
        if category not in config["affiliate_links"]:
            config["affiliate_links"][category] = {
                "enabled": True,
                "links": {}
            }
        
        config["affiliate_links"][category]["links"][platform_name] = url
        self.save_config(config)
        logger.info(f"✓ Added affiliate link: {platform_name} in {category}")
    
    def generate_video_description(self, video_title, platform="youtube", 
                                  custom_intro=None):
        """Generate a monetized video description with CTAs and affiliate links."""
        config = self.load_config()
        
        description_parts = []
        
        # Intro
        if custom_intro:
            description_parts.append(custom_intro)
        else:
            description_parts.append(f"Watch: {video_title}\n")
        
        # LoveGuard CTA (top)
        loveguard_cta = config.get("loveguard_cta", {})
        if loveguard_cta.get("enabled") and loveguard_cta.get("placement") == "top":
            description_parts.append(f"\n{loveguard_cta['text']}\n")
        
        # Affiliate links (as section)
        description_parts.append("\n--- RECOMMENDED RESOURCES ---\n")
        affiliate_links = config.get("affiliate_links", {})
        for category, category_data in affiliate_links.items():
            if category_data.get("enabled"):
                description_parts.append(f"\n{category.replace('_', ' ').title()}:")
                for name, url in category_data.get("links", {}).items():
                    description_parts.append(f"  • {name}: {url}")
        
        # LoveGuard CTA (middle/bottom)
        if loveguard_cta.get("enabled") and loveguard_cta.get("placement") in ["middle", "bottom"]:
            description_parts.append(f"\n{loveguard_cta['text']}\n")
        
        # Platform-specific CTA
        platform_cta = config.get("cta_templates", {}).get(platform, "")
        if platform_cta:
            description_parts.append(f"\n{platform_cta}\n")
        
        # Sponsorship (if enabled)
        sponsorship = config.get("sponsorships", {})
        if sponsorship.get("enabled"):
            description_parts.append(f"\n{sponsorship['text']}\n")
        
        # Hashtags
        description_parts.append("\n#LoveGuard #DatingAdvice #Relationships #SingleLife")
        
        return "\n".join(description_parts)
    
    def inject_into_batch(self, batch_name):
        """Inject monetization descriptions into a batch manifest."""
        batch_dir = self.batches_dir / batch_name
        manifest_path = batch_dir / "manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Batch '{batch_name}' not found")
            return
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            batch_manifest = json.load(f)
        
        # Generate descriptions for each video
        descriptions = {}
        for video in batch_manifest.get("videos", []):
            video_title = video.get("hook", "Video")
            platforms = batch_manifest.get("platforms", ["youtube"])
            
            video_descriptions = {}
            for platform in platforms:
                desc = self.generate_video_description(
                    video_title=video_title,
                    platform=platform
                )
                video_descriptions[platform] = desc
            
            descriptions[f"video_{video['video_num']}"] = video_descriptions
        
        # Save to batch
        batch_manifest["monetized_descriptions"] = descriptions
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(batch_manifest, f, indent=2)
        
        logger.info(f"✓ Injected monetization descriptions into batch '{batch_name}'")
        logger.info(f"  Total videos: {len(batch_manifest['videos'])}")
        
        return descriptions
    
    def preview_description(self, batch_name, video_num=1, platform="youtube"):
        """Preview a monetized description for a specific video."""
        batch_dir = self.batches_dir / batch_name
        manifest_path = batch_dir / "manifest.json"
        
        if not manifest_path.exists():
            logger.error(f"Batch '{batch_name}' not found")
            return
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            batch_manifest = json.load(f)
        
        # Generate for requested video
        video_title = batch_manifest["videos"][video_num - 1].get("hook", "Video")
        description = self.generate_video_description(
            video_title=video_title,
            platform=platform
        )
        
        print(f"\n{'='*70}")
        print(f"PREVIEW: {batch_name} - Video {video_num} ({platform})")
        print(f"{'='*70}\n")
        print(description)
        print(f"\n{'='*70}\n")
    
    def list_config(self):
        """List current monetization configuration."""
        config = self.load_config()
        
        print("\n" + "="*70)
        print("MONETIZATION HOOKS CONFIGURATION")
        print("="*70)
        
        print("\n🎯 LoveGuard CTA")
        loveguard = config.get("loveguard_cta", {})
        print(f"  Status: {'ENABLED' if loveguard.get('enabled') else 'DISABLED'}")
        print(f"  Text: {loveguard.get('text', 'N/A')}")
        print(f"  Placement: {loveguard.get('placement', 'N/A')}")
        
        print("\n🔗 Affiliate Links")
        for category, cat_data in config.get("affiliate_links", {}).items():
            print(f"  {category.replace('_', ' ').title()}: {'ENABLED' if cat_data.get('enabled') else 'DISABLED'}")
            for platform, url in cat_data.get("links", {}).items():
                print(f"    • {platform}: {url}")
        
        print("\n📣 Sponsorship")
        sponsor = config.get("sponsorships", {})
        print(f"  Status: {'ENABLED' if sponsor.get('enabled') else 'DISABLED'}")
        
        print("\n📱 Platform CTAs")
        for platform, cta in config.get("cta_templates", {}).items():
            print(f"  {platform}: {cta}")
        
        print("\n" + "="*70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Auto-inject monetization CTAs, affiliate links, and sponsorships into video descriptions"
    )
    
    parser.add_argument('--config', action='store_true', help='Show current configuration')
    parser.add_argument('--update-loveguard', type=str, help='Update LoveGuard CTA text')
    parser.add_argument('--placement', type=str, default='middle', 
                       choices=['top', 'middle', 'bottom'],
                       help='CTA placement in description')
    
    parser.add_argument('--add-affiliate', nargs=2, metavar=('CATEGORY', 'URL'),
                       help='Add affiliate link (category url)')
    parser.add_argument('--affiliate-platform', type=str, default='platform',
                       help='Platform name for affiliate link')
    
    parser.add_argument('--batch', type=str, help='Batch name to operate on')
    parser.add_argument('--inject', action='store_true', 
                       help='Inject monetization descriptions into batch')
    parser.add_argument('--preview', action='store_true', help='Preview description')
    parser.add_argument('--video', type=int, default=1, help='Video number to preview')
    parser.add_argument('--platform', type=str, default='youtube',
                       help='Platform for preview')
    
    args = parser.parse_args()
    
    hooks = MonetizationHooks()
    
    # Show config
    if args.config:
        hooks.list_config()
    
    # Update LoveGuard CTA
    if args.update_loveguard:
        hooks.update_loveguard_cta(
            text=args.update_loveguard,
            placement=args.placement
        )
    
    # Add affiliate
    if args.add_affiliate:
        hooks.add_affiliate_link(
            category=args.add_affiliate[0],
            platform_name=args.affiliate_platform,
            url=args.add_affiliate[1]
        )
    
    # Inject into batch
    if args.batch and args.inject:
        hooks.inject_into_batch(args.batch)
    
    # Preview
    if args.batch and args.preview:
        hooks.preview_description(
            batch_name=args.batch,
            video_num=args.video,
            platform=args.platform
        )


if __name__ == '__main__':
    main()
