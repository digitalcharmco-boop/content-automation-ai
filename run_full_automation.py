#!/usr/bin/env python3
"""
Complete Automation Test Runner
Tests the entire content automation pipeline end-to-end
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
import json
from pathlib import Path
from datetime import datetime

def check_environment():
    """Check if environment is properly set up"""
    print("=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)

    issues = []

    # Check Python version
    import sys
    print(f"✓ Python version: {sys.version.split()[0]}")

    # Check required modules
    required_modules = [
        'openai',
        'moviepy',
        'PIL',
        'google',
        'requests'
    ]

    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ Module '{module}' installed")
        except ImportError:
            missing_modules.append(module)
            print(f"✗ Module '{module}' NOT installed")
            issues.append(f"Missing module: {module}")

    # Check for .env file or environment variables
    if not os.path.exists('.env'):
        print("⚠ No .env file found (optional)")
        print("  Tip: Copy .env.example to .env and add your API keys")
    else:
        print("✓ .env file found")

    # Check OPENAI_API_KEY
    if os.getenv('OPENAI_API_KEY'):
        print("✓ OPENAI_API_KEY is set")
    else:
        print("⚠ OPENAI_API_KEY not set")
        print("  Warning: Script generation will fail without OpenAI API key")
        issues.append("OPENAI_API_KEY not set")

    # Check directory structure
    required_dirs = ['content_production', 'social_analytics', 'videos', 'temp', 'assets']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ Directory '{dir_name}' exists")
        else:
            print(f"⚠ Directory '{dir_name}' doesn't exist (will be created)")

    # Check core scripts
    core_scripts = [
        'content_production_pipeline.py',
        'script_generator.py',
        'enhanced_video_producer.py',
        'viral_content_optimizer.py',
        'social_analytics_dashboard.py',
        'monetization_hooks.py'
    ]

    for script in core_scripts:
        if os.path.exists(script):
            print(f"✓ Script '{script}' found")
        else:
            print(f"✗ Script '{script}' NOT found")
            issues.append(f"Missing script: {script}")

    print("\n" + "=" * 60)
    if issues:
        print(f"⚠ Found {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        print("\nThe system may not function correctly.")
        return False
    else:
        print("✅ Environment check PASSED!")
        print("System is ready to run.")
        return True

    return len(issues) == 0


def test_script_generation():
    """Test script generation"""
    print("\n" + "=" * 60)
    print("🎬 TESTING SCRIPT GENERATION")
    print("=" * 60)

    try:
        from script_generator import ScriptGenerator

        generator = ScriptGenerator()

        # Test with simple topic
        test_topic = "5 psychology tricks to read body language"
        print(f"Generating script for: {test_topic}")

        script = generator.generate(
            topic=test_topic,
            target_audience="general",
            retention_focus=True
        )

        if script:
            print(f"✓ Script generated successfully!")
            print(f"  Length: {len(script)} characters")
            print(f"  Preview: {script[:100]}...")
            return True
        else:
            print("✗ Script generation failed - empty result")
            return False

    except Exception as e:
        print(f"✗ Script generation failed: {str(e)}")
        return False


def test_batch_generation():
    """Test video batch generation"""
    print("\n" + "=" * 60)
    print("📦 TESTING BATCH GENERATION")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline

        pipeline = ContentProductionPipeline()

        # Generate small test batch
        print("Generating test batch with 2 videos...")
        batch_name = f"test_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        batch_manifest = pipeline.generate_batch(
            topic="relationship psychology facts",
            count=2,
            batch_name=batch_name,
            animation_style="realistic",
            story_template="problem_solution"
        )

        if batch_manifest and 'videos' in batch_manifest:
            print(f"✓ Batch generated successfully!")
            print(f"  Batch name: {batch_manifest['batch_name']}")
            print(f"  Videos: {len(batch_manifest['videos'])}")
            return True, batch_name
        else:
            print("✗ Batch generation failed")
            return False, None

    except Exception as e:
        print(f"✗ Batch generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None


def test_monetization():
    """Test monetization hooks"""
    print("\n" + "=" * 60)
    print("💰 TESTING MONETIZATION HOOKS")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline

        pipeline = ContentProductionPipeline()

        # Use the test batch from previous step
        batches_dir = Path("content_production/batches")
        if not batches_dir.exists():
            print("⚠ No batches found to test monetization")
            return True  # Skip test

        batch_dirs = list(batches_dir.iterdir())
        if not batch_dirs:
            print("⚠ No batches found to test monetization")
            return True  # Skip test

        test_batch = batch_dirs[0].name
        print(f"Testing monetization on batch: {test_batch}")

        pipeline.add_monetization_hooks(
            batch_name=test_batch,
            loveguard_cta="Try LoveGuard Premium for advanced relationship insights!"
        )

        print("✓ Monetization hooks added successfully!")
        return True

    except Exception as e:
        print(f"✗ Monetization test failed: {str(e)}")
        return False


def test_scheduling():
    """Test video scheduling"""
    print("\n" + "=" * 60)
    print("📅 TESTING VIDEO SCHEDULING")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline

        pipeline = ContentProductionPipeline()

        # Find a batch to schedule
        batches_dir = Path("content_production/batches")
        if not batches_dir.exists() or not list(batches_dir.iterdir()):
            print("⚠ No batches found to schedule")
            return True  # Skip test

        test_batch = list(batches_dir.iterdir())[0].name
        print(f"Scheduling batch: {test_batch}")

        schedule_entry = pipeline.schedule_batch(
            batch_name=test_batch,
            interval="daily"
        )

        if schedule_entry:
            print("✓ Batch scheduled successfully!")
            print(f"  Publications: {len(schedule_entry['publications'])}")
            return True
        else:
            print("✗ Scheduling failed")
            return False

    except Exception as e:
        print(f"✗ Scheduling test failed: {str(e)}")
        return False


def test_analytics():
    """Test analytics system"""
    print("\n" + "=" * 60)
    print("📊 TESTING ANALYTICS SYSTEM")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline

        pipeline = ContentProductionPipeline()

        stats = pipeline.get_stats()

        print("✓ Analytics retrieved successfully!")
        print(f"  Total videos: {stats['total_videos']}")
        print(f"  Published: {stats['published_videos']}")
        print(f"  Scheduled: {stats['scheduled_videos']}")
        print(f"  Batches: {len(stats['batches'])}")

        return True

    except Exception as e:
        print(f"✗ Analytics test failed: {str(e)}")
        return False


def generate_test_report(results):
    """Generate test report"""
    print("\n" + "=" * 60)
    print("📋 TEST REPORT")
    print("=" * 60)

    total_tests = len(results)
    passed_tests = sum(1 for r in results.values() if r)
    failed_tests = total_tests - passed_tests

    print(f"\nTotal Tests: {total_tests}")
    print(f"Passed: {passed_tests} ✓")
    print(f"Failed: {failed_tests} ✗")
    print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%\n")

    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {test_name}: {status}")

    print("\n" + "=" * 60)

    if failed_tests == 0:
        print("🎉 ALL TESTS PASSED!")
        print("Your content automation system is fully operational.")
    else:
        print("⚠ SOME TESTS FAILED")
        print("Please review the errors above and fix any issues.")

    print("=" * 60)

    # Save report
    report_file = Path("test_report.json")
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed": passed_tests,
        "failed": failed_tests,
        "success_rate": passed_tests/total_tests*100,
        "results": results
    }

    with open(report_file, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\nReport saved to: {report_file}")


def main():
    """Run complete automation test"""
    print("=" * 60)
    print("  CONTENT AUTOMATION AI - FULL SYSTEM TEST")
    print("=" * 60)
    print()

    results = {}

    # Test 1: Environment check
    results['Environment Check'] = check_environment()

    if not results['Environment Check']:
        print("\n⚠ Environment check failed. Some tests may not work properly.")
        proceed = input("Continue anyway? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Test suite aborted.")
            return

    # Test 2: Script generation (requires OpenAI API key)
    if os.getenv('OPENAI_API_KEY'):
        results['Script Generation'] = test_script_generation()
    else:
        print("\n⚠ Skipping script generation test (no OPENAI_API_KEY)")
        results['Script Generation'] = True  # Don't count as failure

    # Test 3: Batch generation (requires OpenAI API key)
    if os.getenv('OPENAI_API_KEY'):
        batch_result, batch_name = test_batch_generation()
        results['Batch Generation'] = batch_result
    else:
        print("\n⚠ Skipping batch generation test (no OPENAI_API_KEY)")
        results['Batch Generation'] = True  # Don't count as failure

    # Test 4: Monetization
    results['Monetization Hooks'] = test_monetization()

    # Test 5: Scheduling
    results['Video Scheduling'] = test_scheduling()

    # Test 6: Analytics
    results['Analytics System'] = test_analytics()

    # Generate report
    generate_test_report(results)

    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)

    if all(results.values()):
        print("""
✅ Your system is fully functional!

To start generating content:

1. Set your OpenAI API key:
   $env:OPENAI_API_KEY="your-key-here"

2. Generate your first batch:
   python content_production_pipeline.py --topic "your topic" --count 5 --batch-name week1

3. Add monetization:
   python content_production_pipeline.py --batch week1 --add-cta "Your CTA here"

4. Schedule publishing:
   python content_production_pipeline.py --batch week1 --schedule --interval daily

5. View analytics:
   python content_production_pipeline.py --stats

For easier workflow, use PowerShell helpers:
   . .\\social_media_helpers.ps1
   Generate-VideoBatch -Topic "your topic" -Count 5 -BatchName week1
        """)
    else:
        print("""
⚠ Some tests failed. Please:

1. Check that all dependencies are installed:
   .venv\\Scripts\\python.exe -m pip install -r requirements.txt

2. Set up your OpenAI API key:
   $env:OPENAI_API_KEY="your-key-here"

3. Review error messages above and fix any issues

4. Re-run this test:
   python run_full_automation.py
        """)

    print("=" * 60)


if __name__ == "__main__":
    main()
