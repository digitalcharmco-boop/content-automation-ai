#!/usr/bin/env python3
"""
Simple Video Creator - No ImageMagick required
Uses PIL/Pillow for text rendering instead of moviepy's TextClip
"""

import os
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from moviepy import ImageClip, AudioClip, concatenate_videoclips, CompositeVideoClip


class SimpleVideoCreator:
    def __init__(self, output_dir="videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def create_text_image(self, text, width=1920, height=1080, bg_color=(30, 30, 30), 
                         text_color=(255, 255, 255), font_size=60):
        """Create an image with text using PIL"""
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a system font
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Word wrap text
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), line_text, font=font)
            line_width = bbox[2] - bbox[0]
            
            if line_width > width - 200:  # Leave margin
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(line_text)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Calculate total text height
        total_height = len(lines) * (font_size + 10)
        y = (height - total_height) // 2
        
        # Draw each line centered
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            draw.text((x, y), line, font=font, fill=text_color)
            y += font_size + 10
        
        return np.array(img)
    
    def create_simple_video(self, topic="Relationship Advice Demo"):
        """Create a simple demo video"""
        print("🎬 Creating simple demo video...")
        
        # Define scenes
        scenes = [
            {"text": "Why do 70% of relationships fail?", "duration": 3, "bg": (20, 20, 40)},
            {"text": "Most people make one critical mistake...", "duration": 3, "bg": (40, 20, 20)},
            {"text": "They forget communication is key", "duration": 3, "bg": (20, 40, 20)},
            {"text": "Start practicing today!", "duration": 2, "bg": (30, 30, 60)}
        ]
        
        clips = []
        
        for i, scene in enumerate(scenes):
            print(f"  Creating scene {i+1}/{len(scenes)}...")
            
            # Create text image
            img_array = self.create_text_image(
                scene["text"],
                bg_color=scene["bg"],
                text_color=(255, 255, 255),
                font_size=70
            )
            
            # Create video clip from image
            clip = ImageClip(img_array).with_duration(scene["duration"])
            
            # Add fade in/out
            if i == 0:
                clip = clip
            if i == len(scenes) - 1:
                clip = clip.crossfadeout(0.5)
            
            clips.append(clip)
        
        # Concatenate all clips
        print("  Combining scenes...")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add silent audio
        print("  Adding audio...")
        duration = final_video.duration
        audio = AudioClip(lambda t: 0, duration=duration, fps=44100)
        final_video = final_video.set_audio(audio)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
        output_file = self.output_dir / f"{safe_topic}_{timestamp}.mp4"
        
        # Export video
        print(f"  Exporting to: {output_file}")
        final_video.write_videofile(
            str(output_file),
            fps=24,
            codec='libx264',
            audio_codec='aac',
            preset='medium',
            logger=None  # Suppress moviepy progress
        )
        
        # Create thumbnail
        print("  Creating thumbnail...")
        thumbnail_file = self.output_dir / f"thumbnail_{timestamp}.jpg"
        thumb_img = self.create_text_image(
            topic,
            width=1280,
            height=720,
            bg_color=(30, 30, 60),
            font_size=80
        )
        Image.fromarray(thumb_img).save(thumbnail_file, quality=95)
        
        # Cleanup
        audio.close()
        final_video.close()
        
        return {
            "video_file": str(output_file),
            "thumbnail_file": str(thumbnail_file),
            "duration": duration,
            "scenes": len(scenes)
        }


def main():
    print("\n" + "=" * 60)
    print("🎥 SIMPLE VIDEO CREATOR (No ImageMagick Required)")
    print("=" * 60)
    
    creator = SimpleVideoCreator()
    
    try:
        result = creator.create_simple_video(topic="Relationship Advice Demo")
        
        print("\n" + "=" * 60)
        print("✅ VIDEO CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📹 Video: {result['video_file']}")
        print(f"🖼️ Thumbnail: {result['thumbnail_file']}")
        print(f"⏱️ Duration: {result['duration']:.1f} seconds")
        print(f"🎬 Scenes: {result['scenes']}")
        
        # Check file size
        video_path = Path(result['video_file'])
        if video_path.exists():
            size_mb = video_path.stat().st_size / (1024 * 1024)
            print(f"📊 File Size: {size_mb:.2f} MB")
            print(f"\n📂 Location: {video_path.parent.absolute()}")
        
        print("\n🎉 Done! Open the video to preview your content.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
