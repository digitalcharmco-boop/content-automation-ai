
from script_generator import ScriptGenerator
from enhanced_video_producer import EnhancedVideoProducer
from datetime import datetime
import json
import os

def main():
    print("🎬 CUSTOM VIDEO PIPELINE (Script Agent + Video Producer)")
    print("=" * 60)
    
    topic = "How to Learn Anything Fast"
    custom_outline = """
    1. Hook: promise a result.
    2. Step 1 (Fast Step).
    3. Step 2 (Fast Step).
    4. Step 3 (Fast Step).
    5. Quick recap or CTA.
    """
    
    print(f"\n📝 Topic: {topic}")
    print(f"📋 Outline: {custom_outline}")
    
    # 1. Generate Script
    print("\ngenerating script with Script Agent...")
    generator = ScriptGenerator()
    
    # Use the generator to create a draft based on the custom outline
    script_content = generator.generate(
        topic=topic,
        # We need to hack this a bit because generate() uses default outline.
        # But wait, generate() calls generate_script_draft(topic, default_outline, ...)
        # So we should call generate_script_draft DIRECTLY to use our outline.
    )
    
    # Actually, let's call generate_script_draft directly
    print("Calling Script Agent with custom outline...")
    draft = generator.generate_script_draft(topic, custom_outline, target_duration=60)
    
    # Handle the result
    if isinstance(draft, dict) and "script" in draft:
        script_text = draft["script"]
        print("\n✅ Script Generated!")
        print("-" * 20)
        print(script_text[:300] + "...")
        print("-" * 20)
        
        # Save it as an approved script for the producer
        script_data = {
            "topic": topic,
            "script": script_text,
            "approved": True,
            "created_at": datetime.now().isoformat()
        }
        
        filename = f"script_custom_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2)
        print(f"\nSaved approved script to: {filename}")
        
        # 2. Produce Video
        print("\n🎥 Producing Video...")
        producer = EnhancedVideoProducer()
        
        result = producer.produce_enhanced_video(
            script_file=filename,
            style="anime",
            template="how_to_guide", # Use our new template
            rare_facts_mode=False
        )
        
        print("\n" + "=" * 60)
        print("🎉 SUCCESS! Video Created")
        print(f"Video: {result['video_file']}")
        print(f"Thumbnail: {result['thumbnail_file']}")
        
    else:
        print("❌ Script generation failed or returned unexpected format")
        print(draft)

if __name__ == "__main__":
    main()
