#!/usr/bin/env python3
"""
Social Media Autopilot System
Automatically schedules and posts content to multiple platforms with optimal timing.
"""

import os
import json
import schedule
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests
import threading
from typing import Dict, List, Optional

class SocialMediaAutopilot:
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.schedule_file = self.config_dir / "posting_schedule.json"
        self.queue_dir = Path("posting_queue")
        self.queue_dir.mkdir(exist_ok=True)
        
        # Platform configurations
        self.platforms = self.get_platform_configs()
        self.optimal_times = self.get_optimal_posting_times()
        
        # Load existing schedule
        self.posting_schedule = self.load_schedule()
    
    def get_platform_configs(self):
        """Define platform-specific configurations"""
        return {
            "youtube": {
                "name": "YouTube",
                "max_title_length": 100,
                "max_description_length": 5000,
                "max_hashtags": 15,
                "video_required": True,
                "image_required": True,  # Thumbnail
                "supports_scheduling": True,
                "api_endpoint": "youtube_api",
                "content_types": ["long_form", "shorts"]
            },
            "tiktok": {
                "name": "TikTok",
                "max_title_length": 150,
                "max_description_length": 2200,
                "max_hashtags": 20,
                "video_required": True,
                "image_required": False,
                "supports_scheduling": False,  # Third-party tools needed
                "api_endpoint": "tiktok_api",
                "content_types": ["short_form"]
            },
            "instagram": {
                "name": "Instagram",
                "max_title_length": 2200,  # Caption length
                "max_description_length": 2200,
                "max_hashtags": 30,
                "video_required": False,
                "image_required": True,
                "supports_scheduling": True,
                "api_endpoint": "instagram_api",
                "content_types": ["post", "story", "reels"]
            },
            "twitter": {
                "name": "Twitter/X",
                "max_title_length": 280,
                "max_description_length": 280,
                "max_hashtags": 10,
                "video_required": False,
                "image_required": False,
                "supports_scheduling": True,
                "api_endpoint": "twitter_api",
                "content_types": ["tweet", "thread"]
            },
            "facebook": {
                "name": "Facebook",
                "max_title_length": 255,
                "max_description_length": 63206,
                "max_hashtags": 20,
                "video_required": False,
                "image_required": False,
                "supports_scheduling": True,
                "api_endpoint": "facebook_api",
                "content_types": ["post", "story", "reels"]
            },
            "linkedin": {
                "name": "LinkedIn",
                "max_title_length": 150,
                "max_description_length": 3000,
                "max_hashtags": 5,
                "video_required": False,
                "image_required": False,
                "supports_scheduling": True,
                "api_endpoint": "linkedin_api",
                "content_types": ["post", "article"]
            }
        }
    
    def get_optimal_posting_times(self):
        """Define optimal posting times for each platform"""
        return {
            "youtube": {
                "weekdays": ["14:00", "17:00", "20:00"],  # 2PM, 5PM, 8PM
                "weekends": ["10:00", "14:00", "19:00"],   # 10AM, 2PM, 7PM
                "timezone": "UTC"
            },
            "tiktok": {
                "weekdays": ["09:00", "12:00", "19:00"],  # 9AM, 12PM, 7PM
                "weekends": ["11:00", "15:00", "20:00"],   # 11AM, 3PM, 8PM
                "timezone": "UTC"
            },
            "instagram": {
                "weekdays": ["08:00", "13:00", "17:00"],  # 8AM, 1PM, 5PM
                "weekends": ["10:00", "13:00", "16:00"],   # 10AM, 1PM, 4PM
                "timezone": "UTC"
            },
            "twitter": {
                "weekdays": ["09:00", "13:00", "17:00", "20:00"],  # Multiple times
                "weekends": ["10:00", "14:00", "18:00"],
                "timezone": "UTC"
            },
            "facebook": {
                "weekdays": ["13:00", "15:00", "20:00"],
                "weekends": ["12:00", "15:00", "18:00"],
                "timezone": "UTC"
            },
            "linkedin": {
                "weekdays": ["08:00", "12:00", "17:00"],  # Business hours
                "weekends": [],  # Skip weekends for LinkedIn
                "timezone": "UTC"
            }
        }
    
    def create_posting_schedule(self, content_data, platforms, start_date=None, frequency="daily"):
        """Create automated posting schedule"""
        if start_date is None:
            start_date = datetime.now() + timedelta(hours=1)
        
        schedule_items = []
        current_date = start_date
        
        for i, platform in enumerate(platforms):
            if platform not in self.platforms:
                print(f"⚠️ Unknown platform: {platform}")
                continue
            
            platform_config = self.platforms[platform]
            optimal_times = self.optimal_times[platform]
            
            # Skip LinkedIn on weekends
            if platform == "linkedin" and current_date.weekday() >= 5:
                continue
            
            # Select optimal time based on day of week
            if current_date.weekday() < 5:  # Weekday
                time_options = optimal_times["weekdays"]
            else:  # Weekend
                time_options = optimal_times["weekends"]
                if not time_options:  # Skip if no weekend times
                    continue
            
            # Select time based on platform index to spread posts
            selected_time = time_options[i % len(time_options)]
            
            # Create scheduled post
            post_datetime = self._combine_date_time(current_date, selected_time)
            
            # Adapt content for platform
            adapted_content = self.adapt_content_for_platform(content_data, platform)
            
            schedule_item = {
                "id": f"{platform}_{post_datetime.strftime('%Y%m%d_%H%M%S')}",
                "platform": platform,
                "scheduled_time": post_datetime.isoformat(),
                "content": adapted_content,
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            
            schedule_items.append(schedule_item)
            
            # Increment date based on frequency
            if frequency == "daily":
                current_date += timedelta(days=1)
            elif frequency == "weekly":
                current_date += timedelta(days=7)
            elif frequency == "spread":
                # Spread across multiple days
                current_date += timedelta(hours=8)
        
        # Add to schedule
        self.posting_schedule.extend(schedule_items)
        self.save_schedule()
        
        return schedule_items
    
    def adapt_content_for_platform(self, content_data, platform):
        """Adapt content specifically for each platform"""
        platform_config = self.platforms[platform]
        
        # Get viral content elements
        viral_elements = content_data.get('viral_elements', {})
        
        adapted = {
            "platform": platform,
            "video_file": content_data.get('video_file'),
            "thumbnail_file": content_data.get('thumbnail_file')
        }
        
        if platform == "youtube":
            adapted.update({
                "title": self._truncate_text(
                    viral_elements.get('titles', [''])[0] or content_data.get('topic', ''),
                    platform_config["max_title_length"]
                ),
                "description": self._create_youtube_description(content_data, viral_elements),
                "tags": self._select_hashtags(viral_elements.get('hashtags', []), 15),
                "category": "22",  # People & Blogs
                "privacy": "public",
                "thumbnail": content_data.get('thumbnail_file')
            })
        
        elif platform == "tiktok":
            adapted.update({
                "caption": self._create_tiktok_caption(content_data, viral_elements),
                "hashtags": self._select_hashtags(viral_elements.get('hashtags', []), 20),
                "video": content_data.get('video_file'),
                "allow_duet": True,
                "allow_stitch": True
            })
        
        elif platform == "instagram":
            adapted.update({
                "caption": self._create_instagram_caption(content_data, viral_elements),
                "hashtags": self._select_hashtags(viral_elements.get('hashtags', []), 30),
                "media": content_data.get('video_file') or content_data.get('thumbnail_file'),
                "location": None
            })
        
        elif platform == "twitter":
            adapted.update({
                "text": self._create_twitter_content(content_data, viral_elements),
                "media": [content_data.get('thumbnail_file')] if content_data.get('thumbnail_file') else [],
                "thread": self._create_twitter_thread(content_data) if len(content_data.get('script', '')) > 200 else None
            })
        
        elif platform == "facebook":
            adapted.update({
                "message": self._create_facebook_post(content_data, viral_elements),
                "link": content_data.get('youtube_url'),
                "media": content_data.get('thumbnail_file'),
                "targeting": None
            })
        
        elif platform == "linkedin":
            adapted.update({
                "text": self._create_linkedin_post(content_data, viral_elements),
                "media": content_data.get('thumbnail_file'),
                "article": None
            })
        
        return adapted
    
    def _create_youtube_description(self, content_data, viral_elements):
        """Create optimized YouTube description"""
        hooks = viral_elements.get('hooks', [])
        engagement_questions = viral_elements.get('engagement_questions', [])
        
        description_parts = []
        
        # Hook
        if hooks:
            description_parts.append(hooks[0])
            description_parts.append("")
        
        # Main content summary
        script = content_data.get('script', '')
        if script:
            summary = script[:500] + "..." if len(script) > 500 else script
            description_parts.append(summary)
            description_parts.append("")
        
        # Engagement question
        if engagement_questions:
            description_parts.append("💬 " + engagement_questions[0])
            description_parts.append("")
        
        # Call to action
        description_parts.extend([
            "🔔 Subscribe for more amazing content!",
            "👍 Like if this helped you!",
            "📢 Share with someone who needs to see this!",
            "",
            "📱 Follow us on other platforms:",
            "• TikTok: @yourhandle",
            "• Instagram: @yourhandle",
            "• Twitter: @yourhandle"
        ])
        
        return "\n".join(description_parts)
    
    def _create_tiktok_caption(self, content_data, viral_elements):
        """Create TikTok caption with hooks and hashtags"""
        hooks = viral_elements.get('hooks', [])
        captions = viral_elements.get('captions', {}).get('tiktok', [])
        
        if captions:
            return captions[0]
        elif hooks:
            return f"{hooks[0]} 🤯 Follow for more mind-blowing facts! ✨"
        else:
            return f"🔥 {content_data.get('topic', 'Amazing content')} - you won't believe this! 💯"
    
    def _create_instagram_caption(self, content_data, viral_elements):
        """Create Instagram caption with storytelling"""
        captions = viral_elements.get('captions', {}).get('instagram', [])
        hooks = viral_elements.get('hooks', [])
        
        if captions:
            return captions[0]
        
        caption_parts = []
        
        # Hook
        if hooks:
            caption_parts.append(hooks[0] + " 🤯")
            caption_parts.append("")
        
        # Story element
        caption_parts.append(f"Here's what most people don't realize about {content_data.get('topic', 'this topic')}...")
        caption_parts.append("")
        
        # Call to action
        caption_parts.extend([
            "💭 What do you think? Drop your thoughts below! 👇",
            "",
            "🔥 Follow @yourhandle for more content like this!",
            "💾 Save this post for later!"
        ])
        
        return "\n".join(caption_parts)
    
    def _create_twitter_content(self, content_data, viral_elements):
        """Create Twitter content optimized for engagement"""
        hooks = viral_elements.get('hooks', [])
        
        if hooks:
            hook = hooks[0]
            if len(hook) > 200:
                return f"{hook[:200]}... 🧵"
            else:
                return f"{hook} 🔥\n\nWhat's your experience with this? 💭"
        
        return f"🤯 Mind-blowing fact about {content_data.get('topic', 'this topic')}...\n\nThread 👇"
    
    def _create_facebook_post(self, content_data, viral_elements):
        """Create Facebook post with community engagement"""
        hooks = viral_elements.get('hooks', [])
        
        post_parts = []
        
        if hooks:
            post_parts.append(hooks[0] + " 🤯")
            post_parts.append("")
        
        post_parts.extend([
            f"I just learned something incredible about {content_data.get('topic', 'this topic')} and had to share it with you all! 💡",
            "",
            "Check out the full video here: [LINK]",
            "",
            "What surprises you most about this? Let me know in the comments! 👇"
        ])
        
        return "\n".join(post_parts)
    
    def _create_linkedin_post(self, content_data, viral_elements):
        """Create professional LinkedIn post"""
        hooks = viral_elements.get('hooks', [])
        
        post_parts = []
        
        # Professional hook
        if hooks:
            professional_hook = hooks[0].replace("🤯", "").replace("🔥", "").strip()
            post_parts.append(f"Professional insight: {professional_hook}")
        else:
            post_parts.append(f"Key insights about {content_data.get('topic', 'this topic')} that professionals should know:")
        
        post_parts.append("")
        post_parts.extend([
            "In my latest research, I discovered some fascinating patterns that could impact how we approach this field.",
            "",
            "What are your thoughts on this topic? Have you experienced similar insights in your work?",
            "",
            "#ProfessionalDevelopment #Industry #Knowledge"
        ])
        
        return "\n".join(post_parts)
    
    def _create_twitter_thread(self, content_data):
        """Create Twitter thread from content"""
        script = content_data.get('script', '')
        if not script:
            return None
        
        # Split into tweet-sized chunks
        sentences = script.split('. ')
        tweets = []
        current_tweet = ""
        
        for sentence in sentences:
            if len(current_tweet + sentence) < 250:
                current_tweet += sentence + ". "
            else:
                if current_tweet:
                    tweets.append(current_tweet.strip())
                current_tweet = sentence + ". "
        
        if current_tweet:
            tweets.append(current_tweet.strip())
        
        # Number the tweets
        numbered_tweets = []
        for i, tweet in enumerate(tweets, 1):
            if i == 1:
                numbered_tweets.append(f"{tweet} 🧵")
            else:
                numbered_tweets.append(f"{i}/{len(tweets)} {tweet}")
        
        return numbered_tweets
    
    def _truncate_text(self, text, max_length):
        """Truncate text to fit platform limits"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."
    
    def _select_hashtags(self, hashtags, max_count):
        """Select optimal hashtags for platform"""
        if not hashtags:
            return []
        return hashtags[:max_count]
    
    def _combine_date_time(self, date, time_str):
        """Combine date and time string"""
        hour, minute = map(int, time_str.split(':'))
        return date.replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    def setup_automated_posting(self):
        """Setup automated posting scheduler"""
        print("🚀 Setting up automated posting scheduler...")
        
        # Schedule periodic checks
        schedule.every(5).minutes.do(self.check_and_post)
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        
        print("✅ Automated posting scheduler is running!")
        return scheduler_thread
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def check_and_post(self):
        """Check for posts that need to be published"""
        current_time = datetime.now()
        
        for post in self.posting_schedule:
            if post["status"] != "scheduled":
                continue
            
            scheduled_time = datetime.fromisoformat(post["scheduled_time"])
            
            # Check if it's time to post (within 5 minute window)
            if abs((current_time - scheduled_time).total_seconds()) <= 300:
                print(f"📤 Posting to {post['platform']} at {current_time}")
                
                success = self.publish_to_platform(post)
                
                if success:
                    post["status"] = "published"
                    post["published_at"] = current_time.isoformat()
                    print(f"✅ Successfully posted to {post['platform']}")
                else:
                    post["status"] = "failed"
                    post["failed_at"] = current_time.isoformat()
                    print(f"❌ Failed to post to {post['platform']}")
                
                self.save_schedule()
    
    def publish_to_platform(self, post_data):
        """Publish content to specific platform"""
        platform = post_data["platform"]
        content = post_data["content"]
        
        try:
            if platform == "youtube":
                return self._publish_to_youtube(content)
            elif platform == "tiktok":
                return self._publish_to_tiktok(content)
            elif platform == "instagram":
                return self._publish_to_instagram(content)
            elif platform == "twitter":
                return self._publish_to_twitter(content)
            elif platform == "facebook":
                return self._publish_to_facebook(content)
            elif platform == "linkedin":
                return self._publish_to_linkedin(content)
            else:
                print(f"⚠️ Unsupported platform: {platform}")
                return False
        
        except Exception as e:
            print(f"❌ Error posting to {platform}: {str(e)}")
            return False
    
    def _publish_to_youtube(self, content):
        """Publish to YouTube"""
        # Implementation would use YouTube API
        print(f"📺 Would publish to YouTube: {content['title']}")
        return True  # Placeholder
    
    def _publish_to_tiktok(self, content):
        """Publish to TikTok"""
        # Implementation would use TikTok API or third-party service
        print(f"🎵 Would publish to TikTok: {content['caption']}")
        return True  # Placeholder
    
    def _publish_to_instagram(self, content):
        """Publish to Instagram"""
        # Implementation would use Instagram API
        print(f"📸 Would publish to Instagram: {content['caption'][:50]}...")
        return True  # Placeholder
    
    def _publish_to_twitter(self, content):
        """Publish to Twitter"""
        # Implementation would use Twitter API
        print(f"🐦 Would publish to Twitter: {content['text'][:50]}...")
        return True  # Placeholder
    
    def _publish_to_facebook(self, content):
        """Publish to Facebook"""
        # Implementation would use Facebook API
        print(f"👥 Would publish to Facebook: {content['message'][:50]}...")
        return True  # Placeholder
    
    def _publish_to_linkedin(self, content):
        """Publish to LinkedIn"""
        # Implementation would use LinkedIn API
        print(f"💼 Would publish to LinkedIn: {content['text'][:50]}...")
        return True  # Placeholder
    
    def load_schedule(self):
        """Load existing posting schedule"""
        if self.schedule_file.exists():
            with open(self.schedule_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_schedule(self):
        """Save posting schedule to file"""
        with open(self.schedule_file, 'w', encoding='utf-8') as f:
            json.dump(self.posting_schedule, f, indent=2, ensure_ascii=False)
    
    def add_content_to_autopilot(self, content_data, platforms=None, viral_elements=None, start_date=None):
        """Add content to automated posting schedule"""
        if platforms is None:
            platforms = ["youtube", "tiktok", "instagram", "twitter", "facebook"]
        
        # Merge viral elements into content data
        if viral_elements:
            content_data["viral_elements"] = viral_elements
        
        # Create posting schedule
        scheduled_posts = self.create_posting_schedule(
            content_data, 
            platforms, 
            start_date,
            frequency="spread"
        )
        
        print(f"📅 Scheduled {len(scheduled_posts)} posts across {len(platforms)} platforms")
        
        # Show schedule preview
        for post in scheduled_posts:
            scheduled_time = datetime.fromisoformat(post["scheduled_time"])
            print(f"  📱 {post['platform'].title()}: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
        
        return scheduled_posts
    
    def get_schedule_status(self):
        """Get status of scheduled posts"""
        status_counts = {"scheduled": 0, "published": 0, "failed": 0}
        
        for post in self.posting_schedule:
            status_counts[post["status"]] = status_counts.get(post["status"], 0) + 1
        
        return status_counts

def main():
    """Interactive social media autopilot setup"""
    autopilot = SocialMediaAutopilot()
    
    print("🚀 SOCIAL MEDIA AUTOPILOT")
    print("=" * 40)
    
    # Mock content data for demonstration
    content_data = {
        "topic": "Amazing Science Facts",
        "script": "Did you know that octopuses have three hearts? This incredible fact shows how diverse nature can be...",
        "video_file": "example_video.mp4",
        "thumbnail_file": "example_thumbnail.jpg"
    }
    
    # Mock viral elements
    viral_elements = {
        "hooks": ["🤯 This will blow your mind about octopuses", "Stop scrolling if you love ocean facts"],
        "titles": ["3 Hearts? The Shocking Truth About Octopuses", "Ocean Facts That Will Amaze You"],
        "hashtags": ["#octopus", "#oceanfacts", "#science", "#nature", "#mindblown", "#facts"],
        "engagement_questions": ["What's the coolest ocean fact you know?", "Have you ever seen an octopus in real life?"]
    }
    
    print("📱 Available platforms:")
    platforms = list(autopilot.platforms.keys())
    for i, platform in enumerate(platforms, 1):
        print(f"  {i}. {platform.title()}")
    
    # Platform selection
    selected_platforms = input(f"\nSelect platforms (1-{len(platforms)}, comma-separated, or 'all'): ").strip()
    
    if selected_platforms.lower() == 'all':
        target_platforms = platforms
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selected_platforms.split(',')]
            target_platforms = [platforms[i] for i in indices if 0 <= i < len(platforms)]
        except:
            target_platforms = ["youtube", "instagram", "twitter"]
    
    print(f"\n📅 Selected platforms: {', '.join(target_platforms)}")
    
    # Schedule content
    scheduled_posts = autopilot.add_content_to_autopilot(
        content_data, 
        target_platforms, 
        viral_elements
    )
    
    # Setup automated posting
    setup_autopilot = input("\n🤖 Start automated posting? (y/n): ").strip().lower() == 'y'
    
    if setup_autopilot:
        autopilot.setup_automated_posting()
        print("✅ Autopilot is running! Posts will be published automatically.")
        print("📊 Check posting_queue/ folder for scheduled content.")
        
        # Keep running
        try:
            while True:
                time.sleep(60)
                status = autopilot.get_schedule_status()
                print(f"📈 Status: {status['scheduled']} scheduled, {status['published']} published, {status['failed']} failed")
        except KeyboardInterrupt:
            print("\n🛑 Autopilot stopped.")
    else:
        print("📋 Content scheduled but autopilot not started.")
        print("Run with autopilot enabled when ready!")

if __name__ == "__main__":
    main()