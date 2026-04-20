#!/usr/bin/env python3
"""
Demo Video Generator - Creates a test video using the enhanced video producer
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from datetime import datetime
from enhanced_video_producer import EnhancedVideoProducer

def create_demo_video():
    """Create a demo video without requiring a pre-approved script"""

    print("=" * 60)
    print("DEMO VIDEO GENERATOR")
    print("=" * 60)
    print()

    # Initialize producer
    print("[1/5] Initializing video producer...")
    producer = EnhancedVideoProducer()

    # Create a demo script
    print("[2/5] Creating demo script...")
    demo_script = """
    [VISUAL: Hook - Attention grabber]
    Why do 70% of relationships fail in the first year?

    [VISUAL: Problem reveal]
    Most people make one critical mistake when dating.
    They forget that communication is the foundation.

    [VISUAL: Solution]
    Here's what successful couples do differently.
    They practice active listening every single day.

    [VISUAL: Call to action]
    Start improving your relationship today!
    """

    script_data = {
        "topic": "Relationship Psychology Demo",
        "script": demo_script,
        "approved": True,
        "generated_at": datetime.now().isoformat()
    }

    # Save temporary script
    temp_script_file = Path("temp") / "demo_script.json"
    temp_script_file.parent.mkdir(exist_ok=True)

    import json
    with open(temp_script_file, 'w', encoding='utf-8') as f:
        json.dump(script_data, f, indent=2)

    print(f"   Script saved: {temp_script_file}")

    # Generate video
    print("[3/5] Generating video visuals...")
    print("   Style: realistic")
    print("   Template: problem_solution")
    print("   This may take 1-2 minutes...")
    print()

    try:
        result = producer.produce_enhanced_video(
            script_file=str(temp_script_file),
            style="realistic",
            template="problem_solution",
            rare_facts_mode=False
        )

        print()
        print("=" * 60)
        print("SUCCESS - VIDEO CREATED!")
        print("=" * 60)
        print()
        print(f"Video File:     {result['video_file']}")
        print(f"Thumbnail:      {result['thumbnail_file']}")
        print(f"Duration:       {result['duration']:.1f} seconds")
        print(f"Style:          {result['style']}")
        print(f"Template:       {result['template']}")
        print()

        # Check file size
        video_path = Path(result['video_file'])
        if video_path.exists():
            size_mb = video_path.stat().st_size / (1024 * 1024)
            print(f"File Size:      {size_mb:.2f} MB")
            print(f"Full Path:      {video_path.absolute()}")

        print()
        print("=" * 60)
        print("You can now open the video file to preview your content!")
        print("=" * 60)

        return result

    except Exception as e:
        print()
        print("=" * 60)
        print("ERROR DURING VIDEO GENERATION")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print()
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    create_demo_video()
