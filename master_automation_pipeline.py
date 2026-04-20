
#!/usr/bin/env python3
"""Master Automation Pipeline
Orchestrates the complete content creation and distribution workflow.

This module supports both interactive and non-interactive (CLI) usage.
Use `--auto-approve` and provide `--topic` or `--batch-file` for headless runs.
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Import our modules
from viral_content_optimizer import ViralContentOptimizer
from script_generator import ScriptGenerator
from enhanced_video_producer import EnhancedVideoProducer
from social_media_autopilot import SocialMediaAutopilot


class MasterAutomationPipeline:
    def __init__(self):
        self.viral_optimizer = ViralContentOptimizer()
        self.script_generator = ScriptGenerator()
        self.video_producer = EnhancedVideoProducer()
        self.social_autopilot = SocialMediaAutopilot()

        self.pipeline_dir = Path("pipeline_runs")
        self.pipeline_dir.mkdir(exist_ok=True)

    def run_complete_pipeline(self, topic, target_audience="general", platforms=None,
                              animation_style="realistic", story_template="problem_solution",
                              schedule_start=None, auto_approve=False):
        """Run the complete automation pipeline"""

        if platforms is None:
            platforms = ["youtube", "tiktok", "instagram", "twitter", "facebook"]

        pipeline_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        print(f"🚀 Starting Master Automation Pipeline: {pipeline_id}")
        print(f"📋 Topic: {topic}")
        print(f"👥 Audience: {target_audience}")
        print(f"📱 Platforms: {', '.join(platforms)}")
        print(f"🎨 Style: {animation_style}")
        print(f"📖 Template: {story_template}")
        print("=" * 60)

        pipeline_results = {
            "pipeline_id": pipeline_id,
            "topic": topic,
            "target_audience": target_audience,
            "platforms": platforms,
            "animation_style": animation_style,
            "story_template": story_template,
            "started_at": datetime.now().isoformat(),
            "steps": {}
        }

        try:
            # Step 1: Generate Viral Content Package
            print("📈 STEP 1: Generating viral content package...")
            viral_package = self.viral_optimizer.generate_complete_viral_package(
                topic, target_audience, platforms[0] if platforms else "youtube"
            )

            if "error" in viral_package:
                raise Exception(f"Viral content generation failed: {viral_package['error']}")

            pipeline_results["steps"]["viral_content"] = {
                "status": "completed",
                "package_file": f"viral_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "hooks_generated": len(viral_package.get("hooks", {}).get("hooks", [])),
                "titles_generated": len(viral_package.get("titles", {}).get("titles", [])),
                "captions_generated": len(viral_package.get("captions", {}).get("captions", []))
            }
            print(f"✅ Generated viral content package with {pipeline_results['steps']['viral_content']['hooks_generated']} hooks")

            if not auto_approve:
                proceed = input("🤔 Review viral content package. Continue? (y/n): ").strip().lower()
                if proceed != 'y':
                    print("❌ Pipeline stopped by user after viral content generation.")
                    return pipeline_results

            # Step 2: Generate Optimized Script
            print("\n📝 STEP 2: Generating viral-optimized script...")

            # Use best viral elements for script generation
            best_hook = viral_package.get("hooks", {}).get("hooks", [""])[0]
            outline = f"Hook: {best_hook}\nMain content about {topic}\nCall to action"

            script_data = self.script_generator.generate_script_draft(topic, outline, 300)

            if "error" in script_data:
                raise Exception(f"Script generation failed: {script_data['error']}")

            # Auto-approve script if requested
            if auto_approve:
                script_data["approved"] = True
                script_data["approved_at"] = datetime.now().isoformat()

            script_filename = self.script_generator.save_draft(script_data)

            if auto_approve:
                self.script_generator.approve_script(script_filename)

            pipeline_results["steps"]["script"] = {
                "status": "completed" if auto_approve else "needs_approval",
                "script_file": script_filename,
                "word_count": script_data["word_count"],
                "approved": auto_approve
            }

            print(f"✅ Generated script with {script_data['word_count']} words")

            if not auto_approve:
                print(f"⚠️ Script saved to: {script_filename}")
                proceed = input("📖 Review and approve script. Continue? (y/n): ").strip().lower()
                if proceed != 'y':
                    print("❌ Pipeline stopped by user after script generation.")
                    return pipeline_results
                # Manual approval needed here
                self.script_generator.approve_script(script_filename)
                pipeline_results["steps"]["script"]["approved"] = True

            # Step 3: Produce Enhanced Video
            print(f"\n🎬 STEP 3: Producing {animation_style} style video...")

            video_result = self.video_producer.produce_enhanced_video(
                script_filename,
                style=animation_style,
                template=story_template,
                rare_facts_mode=("facts" in topic.lower() or "science" in topic.lower())
            )

            pipeline_results["steps"]["video"] = {
                "status": "completed",
                "video_file": video_result["video_file"],
                "thumbnail_file": video_result["thumbnail_file"],
                "duration": video_result["duration"],
                "style": video_result["style"],
                "template": video_result["template"]
            }

            print(f"✅ Created {animation_style} video: {video_result['duration']:.1f}s duration")

            # Step 4: Setup Social Media Autopilot
            print(f"\n📱 STEP 4: Setting up social media autopilot...")

            # Prepare content data for social media
            content_data = {
                "topic": topic,
                "script": script_data["script"],
                "video_file": video_result["video_file"],
                "thumbnail_file": video_result["thumbnail_file"],
                "duration": video_result["duration"],
                "style": animation_style,
                "template": story_template
            }

            # Extract viral elements for social media
            viral_elements = {
                "hooks": viral_package.get("hooks", {}).get("hooks", []),
                "titles": viral_package.get("titles", {}).get("titles", []),
                "captions": viral_package.get("captions", {}).get("captions", []),
                "engagement_questions": viral_package.get("engagement_questions", {}).get("questions", []),
                "hashtags": self._extract_hashtags_from_viral_package(viral_package)
            }

            # Schedule posts
            start_time = schedule_start or (datetime.now() + timedelta(hours=2))
            scheduled_posts = self.social_autopilot.add_content_to_autopilot(
                content_data,
                platforms,
                viral_elements,
                start_time
            )

            pipeline_results["steps"]["social_media"] = {
                "status": "scheduled",
                "platforms": platforms,
                "scheduled_posts": len(scheduled_posts),
                "start_time": start_time.isoformat(),
                "posts": [
                    {
                        "platform": post["platform"],
                        "scheduled_time": post["scheduled_time"]
                    } for post in scheduled_posts
                ]
            }

            print(f"✅ Scheduled {len(scheduled_posts)} posts across {len(platforms)} platforms")

            # Step 5: Start Autopilot (Optional)
            if not auto_approve:
                start_autopilot = input("\n🤖 Start automated posting now? (y/n): ").strip().lower() == 'y'
            else:
                start_autopilot = True

            if start_autopilot:
                self.social_autopilot.setup_automated_posting()
                pipeline_results["steps"]["autopilot"] = {
                    "status": "running",
                    "started_at": datetime.now().isoformat()
                }
                print("🚀 Autopilot started! Posts will be published automatically.")
            else:
                pipeline_results["steps"]["autopilot"] = {
                    "status": "manual",
                    "note": "Autopilot not started - manual posting required"
                }
                print("📋 Autopilot not started - you can start it later.")

            # Save pipeline results
            pipeline_results["status"] = "completed"
            pipeline_results["completed_at"] = datetime.now().isoformat()

            results_file = self.pipeline_dir / f"pipeline_{pipeline_id}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_results, f, indent=2, ensure_ascii=False)

            print(f"\n🎉 PIPELINE COMPLETED SUCCESSFULLY!")
            print(f"📁 Results saved to: {results_file}")
            print(f"📹 Video: {video_result['video_file']}")
            print(f"📅 {len(scheduled_posts)} posts scheduled across {len(platforms)} platforms")

            return pipeline_results

        except Exception as e:
            pipeline_results["status"] = "failed"
            pipeline_results["error"] = str(e)
            pipeline_results["failed_at"] = datetime.now().isoformat()

            print(f"❌ Pipeline failed: {str(e)}")

            # Save failed results
            results_file = self.pipeline_dir / f"pipeline_failed_{pipeline_id}.json"
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(pipeline_results, f, indent=2, ensure_ascii=False)

            return pipeline_results

    def _extract_hashtags_from_viral_package(self, viral_package):
        """Extract hashtags from various parts of viral package"""
        hashtags = []

        # Extract from captions
        captions = viral_package.get("captions", {}).get("captions", [])
        for caption in captions:
            if isinstance(caption, str) and "#" in caption:
                tags = [word for word in caption.split() if word.startswith("#")]
                hashtags.extend(tags)

        # Add topic-based hashtags
        topic = viral_package.get("topic", "")
        if topic:
            topic_words = topic.lower().split()
            for word in topic_words:
                if len(word) > 3:  # Only meaningful words
                    hashtags.append(f"#{word}")

        # Remove duplicates and return
        return list(set(hashtags))

    def run_batch_pipeline(self, topics_list, config=None):
        """Run pipeline for multiple topics"""
        default_config = {
            "target_audience": "general",
            "platforms": ["youtube", "tiktok", "instagram"],
            "animation_style": "realistic",
            "story_template": "problem_solution",
            "auto_approve": False,
            "delay_between_topics": 1  # hours
        }

        config = {**default_config, **(config or {})}

        print(f"🚀 Starting Batch Pipeline for {len(topics_list)} topics")

        results = []
        start_time = datetime.now()

        for i, topic in enumerate(topics_list):
            print(f"\n📋 Processing topic {i+1}/{len(topics_list)}: {topic}")

            # Calculate staggered start time
            schedule_start = start_time + timedelta(hours=i * config["delay_between_topics"])

            result = self.run_complete_pipeline(
                topic=topic,
                target_audience=config["target_audience"],
                platforms=config["platforms"],
                animation_style=config["animation_style"],
                story_template=config["story_template"],
                schedule_start=schedule_start,
                auto_approve=config["auto_approve"]
            )

            results.append(result)

            if not config["auto_approve"] and i < len(topics_list) - 1:
                proceed = input(f"\n✅ Topic {i+1} complete. Continue to next topic? (y/n): ").strip().lower()
                if proceed != 'y':
                    print("🛑 Batch pipeline stopped by user.")
                    break

        return results

def main():
    """CLI entrypoint for the master pipeline.

    Examples:
      # Single topic headless run
      python master_automation_pipeline.py --topic "AI for creators" --platforms youtube,tiktok --auto-approve

      # Batch run from file (one topic per line)
      python master_automation_pipeline.py --batch-file topics.txt --auto-approve
    """
    parser = argparse.ArgumentParser(description='Master Automation Pipeline')
    parser.add_argument('--topic', help='Single topic to run the pipeline for')
    parser.add_argument('--batch-file', help='Path to a file with topics (one per line)')
    parser.add_argument('--platforms', help="Comma-separated platforms (default: youtube,tiktok,instagram)")
    parser.add_argument('--style', default='realistic', help='Animation style')
    parser.add_argument('--template', default='problem_solution', help='Story template')
    parser.add_argument('--auto-approve', action='store_true', help='Auto-approve all steps for non-interactive runs')
    parser.add_argument('--delay', type=int, default=1, help='Hours between batch topic runs')
    args = parser.parse_args()

    pipeline = MasterAutomationPipeline()

    if args.topic:
        platforms = args.platforms.split(',') if args.platforms else ["youtube", "tiktok", "instagram"]
        result = pipeline.run_complete_pipeline(
            topic=args.topic,
            target_audience='general',
            platforms=platforms,
            animation_style=args.style,
            story_template=args.template,
            schedule_start=None,
            auto_approve=args.auto_approve
        )
        print(f"\n📊 Pipeline Result: {result.get('status')}")
        return

    if args.batch_file:
        if not os.path.exists(args.batch_file):
            print(f"❌ Batch file not found: {args.batch_file}")
            return
        with open(args.batch_file, 'r', encoding='utf-8') as f:
            topics = [line.strip() for line in f if line.strip()]

        config = {
            'target_audience': 'general',
            'platforms': args.platforms.split(',') if args.platforms else ["youtube", "tiktok", "instagram"],
            'animation_style': args.style,
            'story_template': args.template,
            'auto_approve': args.auto_approve,
            'delay_between_topics': args.delay
        }
        results = pipeline.run_batch_pipeline(topics, config)
        successful = len([r for r in results if r.get('status') == 'completed'])
        print(f"\n📊 Batch Complete: {successful}/{len(topics)} successful")
        return

    # If no args passed, fall back to compact interactive mode
    print("🚀 MASTER AUTOMATION PIPELINE (interactive)")
    print("=" * 50)
    topic = input("📋 Enter your content topic: ").strip()
    if not topic:
        print("❌ No topic provided.")
        return
    platforms = input("📱 Enter platforms (comma-separated or 'all', default 'youtube,tiktok,instagram'): ").strip()
    if platforms.lower() == 'all':
        platforms = ["youtube", "tiktok", "instagram", "twitter", "facebook", "linkedin"]
    else:
        platforms = [p.strip() for p in (platforms or 'youtube,tiktok,instagram').split(',')]
    style = input("🎨 Animation style (default 'realistic'): ").strip() or 'realistic'
    template = input("📖 Story template (default 'problem_solution'): ").strip() or 'problem_solution'
    auto_approve = input("\n🤖 Auto-approve all steps? (y/n): ").strip().lower() == 'y'

    result = pipeline.run_complete_pipeline(
        topic=topic,
        target_audience='general',
        platforms=platforms,
        animation_style=style,
        story_template=template,
        auto_approve=auto_approve
    )
    print(f"\n📊 Pipeline Result: {result.get('status')}")


if __name__ == '__main__':
    main()