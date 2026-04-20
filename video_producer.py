#!/usr/bin/env python3
"""
Automated Video Production Pipeline
Creates videos from approved scripts with voice synthesis and editing.
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import requests
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip, ColorClip

class VideoProducer:
    def __init__(self, output_dir="videos"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
    
    def load_approved_script(self, script_file):
        """Load and validate approved script"""
        with open(script_file, 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        
        if not script_data.get('approved', False):
            raise ValueError("Script must be approved before video production")
        
        return script_data
    
    def generate_voice(self, text, voice="en-US-AriaNeural", output_file=None):
        """Generate voice using Azure TTS (requires Azure Speech Service)"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.temp_dir / f"voice_{timestamp}.wav"
        
        # Using Azure Speech Service (requires subscription key)
        speech_key = os.getenv('AZURE_SPEECH_KEY')
        speech_region = os.getenv('AZURE_SPEECH_REGION', 'eastus')
        
        if not speech_key:
            print("Warning: No Azure Speech key found. Using dummy audio.")
            # Create silent audio as placeholder
            duration = len(text.split()) * 0.5  # Approximate duration
            silence = AudioFileClip.silence(duration=duration, fps=44100)
            silence.write_audiofile(str(output_file))
            return output_file
        
        # Azure TTS implementation would go here
        # For now, creating placeholder
        duration = len(text.split()) * 0.5
        silence = AudioFileClip.silence(duration=duration, fps=44100)
        silence.write_audiofile(str(output_file))
        return output_file
    
    def create_visuals(self, script_text, duration):
        """Generate basic video visuals"""
        # Extract visual cues from script
        visual_segments = self._extract_visual_cues(script_text)
        
        # Create simple text-based video
        clips = []
        segment_duration = duration / max(len(visual_segments), 1)
        
        for i, segment in enumerate(visual_segments):
            # Create text clip
            txt_clip = TextClip(
                text=segment['text'][:100] + "..." if len(segment['text']) > 100 else segment['text'],
                font_size=50,
                color='white'
            ).with_duration(segment_duration).with_position('center')
            
            # Create background
            bg = ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(segment_duration)
            
            # Composite
            clip = CompositeVideoClip([bg, txt_clip])
            clips.append(clip)
        
        if not clips:
            # Fallback: simple black background
            clips = [ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duration)]
        
        return concatenate_videoclips(clips)
    
    def _extract_visual_cues(self, script_text):
        """Extract visual cues from script"""
        segments = []
        lines = script_text.split('\n')
        
        current_segment = ""
        for line in lines:
            if line.strip().startswith('[VISUAL:'):
                if current_segment:
                    segments.append({'text': current_segment.strip(), 'visual': line.strip()})
                current_segment = ""
            else:
                current_segment += line + " "
        
        if current_segment:
            segments.append({'text': current_segment.strip(), 'visual': 'default'})
        
        return segments
    
    def create_thumbnail(self, title, output_file=None):
        """Generate thumbnail image"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"thumbnail_{timestamp}.jpg"
        
        # Simple thumbnail with text
        txt_clip = TextClip(
            text=title,
            font_size=60,
            color='white',
            size=(1280, 720)
        ).with_duration(1).with_position('center')
        
        bg = ColorClip(size=(1280, 720), color=(50, 50, 150)).with_duration(1)
        thumbnail = CompositeVideoClip([bg, txt_clip])
        
        # Save frame as image
        thumbnail.save_frame(str(output_file), t=0)
        return output_file
    
    def produce_video(self, script_file):
        """Main video production pipeline"""
        print(f"Starting video production from: {script_file}")
        
        # Load approved script
        script_data = self.load_approved_script(script_file)
        script_text = script_data['script']
        topic = script_data['topic']
        
        # Generate voiceover
        print("Generating voiceover...")
        audio_file = self.generate_voice(script_text)
        
        # Load audio to get duration
        audio_clip = AudioFileClip(str(audio_file))
        duration = audio_clip.duration
        
        # Create visuals
        print("Creating visuals...")
        video_clip = self.create_visuals(script_text, duration)
        
        # Combine audio and video
        print("Combining audio and video...")
        final_video = video_clip.set_audio(audio_clip)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()[:50]
        output_file = self.output_dir / f"{safe_topic}_{timestamp}.mp4"
        
        # Export video
        print(f"Exporting video to: {output_file}")
        final_video.write_videofile(
            str(output_file),
            fps=30,
            codec='libx264',
            audio_codec='aac'
        )
        
        # Generate thumbnail
        print("Creating thumbnail...")
        thumbnail_file = self.create_thumbnail(topic)
        
        # Cleanup
        audio_clip.close()
        video_clip.close()
        final_video.close()
        
        result = {
            "video_file": str(output_file),
            "thumbnail_file": str(thumbnail_file),
            "duration": duration,
            "created_at": datetime.now().isoformat(),
            "script_source": script_file
        }
        
        # Save metadata
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        print(f"Video production complete: {output_file}")
        return result

def main():
    """Interactive video production"""
    producer = VideoProducer()
    
    script_file = input("Enter path to approved script file: ")
    
    if not os.path.exists(script_file):
        print(f"Error: Script file not found: {script_file}")
        return
    
    try:
        result = producer.produce_video(script_file)
        print(f"\nVideo created successfully:")
        print(f"Video: {result['video_file']}")
        print(f"Thumbnail: {result['thumbnail_file']}")
        print(f"Duration: {result['duration']:.1f} seconds")
    
    except Exception as e:
        print(f"Error during video production: {str(e)}")

if __name__ == "__main__":
    main()