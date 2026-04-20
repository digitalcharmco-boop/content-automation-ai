#!/usr/bin/env python3
"""
Quick Video Test - Create a simple demo video without full pipeline dependencies
"""

import os
import json
from pathlib import Path
from datetime import datetime
from enhanced_video_producer import EnhancedVideoProducer

def create_simple_test_script():
    """Create a simple test script for video production"""
    script_data = {
        "topic": "Relationship Advice Test",
        "script": """
[VISUAL: Bold text on dark background]
Why do 70% of relationships fail in the first year?

[VISUAL: Text fade in]
Most people make one critical mistake...

[VISUAL: Dramatic reveal]
They forget that communication isn't just about talking.

[PACE: Slow down]
It's about truly listening and understanding your partner's needs.

[VISUAL: Hopeful imagery]
When you master this skill, everything changes.

[TONE: Inspirational]
Your relationship transforms from struggling to thriving.

[VISUAL: Call to action]
Start practicing active listening today.
""",
        "approved": True,
        "created_at": datetime.now().isoformat()
    }
    
    # Save script
    script_dir = Path("scripts")
    script_dir.mkdir(exist_ok=True)
    
    script_file = script_dir / "test_script.json"
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(script_data, f, indent=2)
    
    print(f"✅ Created test script: {script_file}")
    return script_file

def main():
    print("🎬 QUICK VIDEO TEST")
    print("=" * 50)
    
    # Create test script
    script_file = create_simple_test_script()
    
    # Initialize video producer
    print("\n📹 Initializing video producer...")
    producer = EnhancedVideoProducer()
    
    # Available styles
    styles = list(producer.get_animation_styles().keys())
    templates = list(producer.get_story_templates().keys())
    
    print(f"\n🎨 Available styles: {', '.join(styles)}")
    print(f"📖 Available templates: {', '.join(templates)}")
    
    # Produce video with different styles
    print("\n🎥 Producing demo video...")
    print("⏳ This may take a few minutes...")
    
    try:
        result = producer.produce_enhanced_video(
            script_file=str(script_file),
            style="realistic",  # Change to: cartoon, anime, cinematic, minimal, neon
            template="problem_solution",  # Change to other templates
            rare_facts_mode=False
        )
        
        print("\n" + "=" * 50)
        print("✅ VIDEO CREATED SUCCESSFULLY!")
        print("=" * 50)
        print(f"\n📹 Video Location: {result['video_file']}")
        print(f"🖼️ Thumbnail Location: {result['thumbnail_file']}")
        print(f"⏱️ Duration: {result['duration']:.1f} seconds")
        print(f"🎨 Style: {result['style']}")
        print(f"📖 Template: {result['template']}")
        
        # Check if files exist
        video_path = Path(result['video_file'])
        thumb_path = Path(result['thumbnail_file'])
        
        if video_path.exists():
            size_mb = video_path.stat().st_size / (1024 * 1024)
            print(f"📊 Video Size: {size_mb:.2f} MB")
        
        if thumb_path.exists():
            print(f"✓ Thumbnail created successfully")
        
        print("\n🎉 Test complete! Check the videos/ directory for your output.")
        
    except Exception as e:
        print(f"\n❌ Error creating video: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
