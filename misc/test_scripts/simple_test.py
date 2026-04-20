#!/usr/bin/env python3
"""
Simple Automation Test - No Unicode characters for Windows compatibility
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

def check_environment():
    """Check environment setup"""
    print("=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)

    # Check Python version
    print(f"[OK] Python version: {sys.version.split()[0]}")

    # Check required modules
    required = ['openai', 'moviepy', 'PIL', 'google', 'requests']
    missing = []

    for module in required:
        try:
            __import__(module)
            print(f"[OK] Module '{module}' installed")
        except ImportError:
            missing.append(module)
            print(f"[FAIL] Module '{module}' NOT installed")

    # Check OpenAI API key
    if os.getenv('OPENAI_API_KEY'):
        print("[OK] OPENAI_API_KEY is set")
    else:
        print("[WARN] OPENAI_API_KEY not set - some features won't work")

    # Check core scripts
    scripts = [
        'content_production_pipeline.py',
        'script_generator.py',
        'enhanced_video_producer.py'
    ]

    for script in scripts:
        if os.path.exists(script):
            print(f"[OK] Script '{script}' found")
        else:
            print(f"[FAIL] Script '{script}' NOT found")
            missing.append(script)

    print("=" * 60)

    if missing:
        print(f"RESULT: {len(missing)} issue(s) found")
        return False
    else:
        print("RESULT: All checks passed!")
        return True

def test_imports():
    """Test that all modules can be imported"""
    print("\n" + "=" * 60)
    print("TESTING MODULE IMPORTS")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline
        print("[OK] ContentProductionPipeline imported")

        from script_generator import ScriptGenerator
        print("[OK] ScriptGenerator imported")

        from enhanced_video_producer import EnhancedVideoProducer
        print("[OK] EnhancedVideoProducer imported")

        from viral_content_optimizer import ViralContentOptimizer
        print("[OK] ViralContentOptimizer imported")

        from social_analytics_dashboard import SocialAnalyticsDashboard
        print("[OK] SocialAnalyticsDashboard imported")

        print("=" * 60)
        print("RESULT: All imports successful!")
        return True

    except Exception as e:
        print(f"[FAIL] Import error: {str(e)}")
        print("=" * 60)
        return False

def test_pipeline_init():
    """Test pipeline initialization"""
    print("\n" + "=" * 60)
    print("TESTING PIPELINE INITIALIZATION")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline
        pipeline = ContentProductionPipeline()
        print("[OK] Pipeline initialized")

        # Check directories were created
        if Path("content_production").exists():
            print("[OK] content_production directory created")

        if Path("content_production/batches").exists():
            print("[OK] batches directory created")

        print("=" * 60)
        print("RESULT: Pipeline initialization successful!")
        return True

    except Exception as e:
        print(f"[FAIL] Pipeline init error: {str(e)}")
        print("=" * 60)
        return False

def test_stats():
    """Test stats retrieval"""
    print("\n" + "=" * 60)
    print("TESTING STATS SYSTEM")
    print("=" * 60)

    try:
        from content_production_pipeline import ContentProductionPipeline
        pipeline = ContentProductionPipeline()
        stats = pipeline.get_stats()

        print(f"[OK] Stats retrieved")
        print(f"  Total videos: {stats['total_videos']}")
        print(f"  Published: {stats['published_videos']}")
        print(f"  Batches: {len(stats['batches'])}")

        print("=" * 60)
        print("RESULT: Stats system working!")
        return True

    except Exception as e:
        print(f"[FAIL] Stats error: {str(e)}")
        print("=" * 60)
        return False

def main():
    """Run tests"""
    print("\n")
    print("=" * 60)
    print("CONTENT AUTOMATION AI - SYSTEM TEST")
    print("=" * 60)
    print()

    results = {}

    # Run tests
    results['Environment'] = check_environment()
    results['Imports'] = test_imports()
    results['Pipeline'] = test_pipeline_init()
    results['Stats'] = test_stats()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    total = len(results)
    passed = sum(1 for r in results.values() if r)

    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()

    for name, result in results.items():
        status = "[PASS]" if result else "[FAIL]"
        print(f"  {status} {name}")

    print("=" * 60)

    if passed == total:
        print("SUCCESS: All tests passed!")
        print("\nYour system is ready to use.")
        print("\nNext steps:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Run: python content_production_pipeline.py --help")
        print("3. Or use PowerShell helpers: . .\\social_media_helpers.ps1")
    else:
        print("WARNING: Some tests failed.")
        print("Please review errors above and fix issues.")

    print("=" * 60)

if __name__ == "__main__":
    main()
