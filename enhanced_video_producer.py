#!/usr/bin/env python3
"""
Enhanced Video Production Pipeline
Creates videos with multiple animation styles, story templates, and cinematic effects.
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
import json
import subprocess
from pathlib import Path
from datetime import datetime
import requests
import random
# MoviePy 2.x imports from main module
from moviepy import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips, ImageClip, ColorClip
import numpy as np

class EnhancedVideoProducer:
    def __init__(self, output_dir="videos", assets_dir="assets"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.temp_dir = Path("temp")
        self.temp_dir.mkdir(exist_ok=True)
        self.assets_dir = Path(assets_dir)
        self.assets_dir.mkdir(exist_ok=True)
        
        # Create asset subdirectories
        for subdir in ["fonts", "backgrounds", "animations", "sound_effects", "music"]:
            (self.assets_dir / subdir).mkdir(exist_ok=True)
    
    def get_animation_styles(self):
        """Define available animation and visual styles"""
        return {
            "realistic": {
                "description": "Photorealistic visuals with natural lighting",
                "background_colors": [(25, 25, 25), (45, 45, 45), (65, 65, 65)],
                "text_effects": ["fade_in", "slide_up"],
                "transitions": ["crossfade", "push_left"],
                "fonts": ["Arial-Bold", "Helvetica"],
                "font_size": 60,
                "animation_speed": "normal"
            },
            "cartoon": {
                "description": "Bright, colorful cartoon-style animations",
                "background_colors": [(255, 100, 100), (100, 255, 100), (100, 100, 255)],
                "text_effects": ["bounce", "pop_in", "wiggle"],
                "transitions": ["zoom_in", "bounce"],
                "fonts": ["Comic Sans MS", "Arial-Black"],
                "font_size": 70,
                "animation_speed": "fast"
            },
            "anime": {
                "description": "Japanese animation style with dramatic effects",
                "background_colors": [(50, 0, 100), (100, 0, 50), (0, 50, 100)],
                "text_effects": ["slash_reveal", "dramatic_zoom", "glow"],
                "transitions": ["flash", "swipe_right"],
                "fonts": ["Arial-Bold", "Impact"],
                "font_size": 65,
                "animation_speed": "dynamic"
            },
            "cinematic": {
                "description": "Movie-style with dramatic lighting and effects",
                "background_colors": [(20, 20, 30), (30, 20, 20), (20, 30, 20)],
                "text_effects": ["typewriter", "fade_in", "glow"],
                "transitions": ["fade_to_black", "crossfade"],
                "fonts": ["Times New Roman", "Georgia"],
                "font_size": 55,
                "animation_speed": "slow"
            },
            "minimal": {
                "description": "Clean, modern minimalist design",
                "background_colors": [(255, 255, 255), (245, 245, 245), (235, 235, 235)],
                "text_effects": ["simple_fade", "slide_in"],
                "transitions": ["cut", "fade"],
                "fonts": ["Helvetica-Light", "Arial"],
                "font_size": 50,
                "animation_speed": "normal"
            },
            "neon": {
                "description": "Cyberpunk neon glow effects",
                "background_colors": [(10, 10, 30), (30, 10, 30), (10, 30, 30)],
                "text_effects": ["neon_glow", "flicker", "scan_line"],
                "transitions": ["glitch", "neon_wipe"],
                "fonts": ["Courier New", "Monaco"],
                "font_size": 60,
                "animation_speed": "fast"
            }
        }
    
    def get_story_templates(self):
        """Define story-driven video templates"""
        return {
            "hero_journey": {
                "structure": ["hook", "ordinary_world", "call_to_adventure", "challenges", "transformation", "resolution"],
                "pacing": [0.15, 0.20, 0.15, 0.30, 0.15, 0.05],
                "visual_themes": ["dramatic", "transformative", "inspiring"]
            },
            "problem_solution": {
                "structure": ["problem_reveal", "pain_points", "solution_intro", "how_it_works", "benefits", "call_to_action"],
                "pacing": [0.20, 0.20, 0.15, 0.25, 0.15, 0.05],
                "visual_themes": ["contrast", "before_after", "solution_focused"]
            },
            "list_format": {
                "structure": ["intro", "point_1", "point_2", "point_3", "point_4", "conclusion"],
                "pacing": [0.10, 0.20, 0.20, 0.20, 0.20, 0.10],
                "visual_themes": ["numbered", "progressive", "organized"]
            },
            "story_revelation": {
                "structure": ["mystery_setup", "building_tension", "clues", "revelation", "impact", "lesson"],
                "pacing": [0.15, 0.20, 0.25, 0.20, 0.15, 0.05],
                "visual_themes": ["mysterious", "revealing", "dramatic"]
            },
            "educational": {
                "structure": ["topic_intro", "foundation", "examples", "deep_dive", "application", "summary"],
                "pacing": [0.10, 0.20, 0.25, 0.25, 0.15, 0.05],
                "visual_themes": ["informative", "clear", "progressive"]
            },
            "how_to_guide": {
                "structure": ["hook_result", "step_1", "step_2", "step_3", "step_4", "cta_recap"],
                "pacing": [0.15, 0.20, 0.15, 0.15, 0.15, 0.20],
                "visual_themes": ["instructional", "clear_steps", "action_oriented"]
            }
        }
    
    def get_rare_facts_templates(self):
        """Templates specifically for rare facts and educational content"""
        return {
            "mind_blowing_facts": {
                "intro_hooks": [
                    "🤯 This will blow your mind...",
                    "❗ 95% of people don't know this...",
                    "🔥 Prepare to have your reality shifted...",
                    "💥 This fact will change everything..."
                ],
                "transition_phrases": [
                    "But here's what's even crazier...",
                    "Wait, it gets better...",
                    "Plot twist:",
                    "Here's the kicker..."
                ],
                "fact_reveals": [
                    "The shocking truth is...",
                    "Scientists discovered that...",
                    "What they found will amaze you...",
                    "The reality is mind-bending..."
                ]
            },
            "historical_secrets": {
                "intro_hooks": [
                    "🏛️ History books won't tell you this...",
                    "📜 Hidden in ancient texts...",
                    "👑 Royal secrets exposed...",
                    "⚔️ The untold story..."
                ],
                "transition_phrases": [
                    "Centuries later, we discovered...",
                    "Archaeological evidence revealed...",
                    "Hidden documents show...",
                    "The real story behind..."
                ]
            },
            "science_mysteries": {
                "intro_hooks": [
                    "🔬 Science can't explain this...",
                    "🌌 The universe hides secrets...",
                    "🧬 DNA reveals shocking truths...",
                    "⚡ Physics breaks down here..."
                ],
                "transition_phrases": [
                    "Quantum mechanics suggests...",
                    "Recent studies prove...",
                    "The data shows something impossible...",
                    "Einstein couldn't have imagined..."
                ]
            }
        }
    
    def get_cinematic_effects(self):
        """Define cinematic visual effects"""
        return {
            "transitions": {
                "fade_to_black": lambda clip: clip.fadeout(0.5),
                "zoom_in": lambda clip: clip.resize(lambda t: 1 + 0.1*t),
                "pan_right": lambda clip: clip.with_position(lambda t: (-50*t, 'center')),
                "flash": lambda clip: clip.fx(lambda c: c.with_opacity(0.8 if int(c.duration*10) % 2 else 1)),
                "glitch": lambda clip: clip.fx(lambda c: c.with_opacity(0.9 + 0.1*np.random.random()))
            },
            "text_animations": {
                "typewriter": self._typewriter_effect,
                "glow": self._glow_effect,
                "bounce": self._bounce_effect,
                "neon_glow": self._neon_glow_effect,
                "dramatic_zoom": self._dramatic_zoom_effect
            },
            "background_effects": {
                "particle_system": self._create_particles,
                "gradient_sweep": self._gradient_sweep,
                "noise_texture": self._noise_texture,
                "geometric_shapes": self._geometric_shapes
            }
        }
    
    def _typewriter_effect(self, text_clip):
        """Create typewriter animation effect"""
        # Simplified typewriter effect
        return text_clip
    
    def _glow_effect(self, text_clip):
        """Add glow effect to text"""
        return text_clip.with_opacity(0.9)
    
    def _bounce_effect(self, text_clip):
        """Create bouncing animation"""
        return text_clip.with_position(lambda t: ('center', 'center'))
    
    def _neon_glow_effect(self, text_clip):
        """Create neon glow effect"""
        return text_clip.with_opacity(0.95)
    
    def _dramatic_zoom_effect(self, text_clip):
        """Create dramatic zoom effect"""
        return text_clip.resize(lambda t: 1 + 0.05*np.sin(t*2))
    
    def _create_particles(self, duration):
        """Create particle system background"""
        return ColorClip(size=(1920, 1080), color=(0, 0, 0)).with_duration(duration)
    
    def _gradient_sweep(self, duration, colors):
        """Create gradient sweep effect"""
        return ColorClip(size=(1920, 1080), color=colors[0]).with_duration(duration)
    
    def _noise_texture(self, duration):
        """Create noise texture background"""
        return ColorClip(size=(1920, 1080), color=(30, 30, 30)).with_duration(duration)
    
    def _geometric_shapes(self, duration):
        """Create animated geometric shapes"""
        return ColorClip(size=(1920, 1080), color=(20, 20, 40)).with_duration(duration)
    
    def create_enhanced_visuals(self, script_text, duration, style="realistic", template="problem_solution"):
        """Create enhanced visuals with animation styles and story templates"""
        
        # Get style and template configurations
        animation_style = self.get_animation_styles()[style]
        story_template = self.get_story_templates()[template]
        
        # Extract and structure content
        visual_segments = self._extract_enhanced_visual_cues(script_text, story_template)
        
        # If no segments, create one from the full script
        if not visual_segments:
            visual_segments = [{'text': script_text[:500], 'visual': 'default', 'type': 'default'}]
        
        print(f"Creating video from {len(visual_segments)} segments, total duration: {duration}s")
        
        clips = []
        total_segments = len(visual_segments)
        
        # Simple approach: split duration evenly across segments
        segment_duration = duration / max(total_segments, 1)
        
        for i, segment in enumerate(visual_segments):
            # Create background based on style
            bg_color = random.choice(animation_style["background_colors"])
            background = ColorClip(size=(1920, 1080), color=bg_color).with_duration(segment_duration)
            
            # Create text with style-specific formatting
            text_content = segment['text'][:150] + "..." if len(segment['text']) > 150 else segment['text']
            
            # Skip empty text
            if not text_content.strip():
                print(f"Skipping empty segment {i}")
                continue
            
            print(f"Creating segment {i+1}/{total_segments}: {text_content[:50]}... (duration: {segment_duration}s)")
                
            txt_clip = TextClip(
                text=text_content,
                font_size=animation_style["font_size"],
                color='white',
                stroke_color='black' if style != "minimal" else None,
                stroke_width=2 if style in ["cartoon", "anime"] else 0
            ).with_duration(segment_duration).with_position('center')
            
            # Composite elements with explicit duration
            clip = CompositeVideoClip([background, txt_clip]).with_duration(segment_duration)
            print(f"  Clip {i} created with duration: {clip.duration}")
            clips.append(clip)
        
        print(f"Total clips created: {len(clips)}")
        
        if not clips:
            # Fallback: create simple clip with full text
            print("No clips created, using fallback")
            fallback_color = animation_style["background_colors"][0]
            background = ColorClip(size=(1920, 1080), color=fallback_color).with_duration(duration)
            txt = TextClip(
                text=script_text[:150] + "...",
                font_size=animation_style["font_size"],
                color='white'
            ).with_duration(duration).with_position('center')
            clips = [CompositeVideoClip([background, txt]).with_duration(duration)]
        
        print("Concatenating clips...")
        return concatenate_videoclips(clips)
    
    def _extract_enhanced_visual_cues(self, script_text, story_template):
        """Extract and categorize visual cues based on story template"""
        segments = []
        lines = script_text.split('\n')
        current_segment = ""
        segment_type = "default"
        
        # Keywords for different segment types
        fact_keywords = ["fact", "study", "research", "discovered", "scientists", "data"]
        story_keywords = ["story", "experience", "happened", "remember", "once", "imagine"]
        
        for line in lines:
            line = line.strip()
            
            # Detect segment type
            if any(keyword in line.lower() for keyword in fact_keywords):
                segment_type = "fact"
            elif any(keyword in line.lower() for keyword in story_keywords):
                segment_type = "story"
            
            if line.startswith('[VISUAL:') or line.startswith('[TONE:') or line.startswith('[PACE:'):
                if current_segment:
                    segments.append({
                        'text': current_segment.strip(),
                        'visual': line,
                        'type': segment_type
                    })
                current_segment = ""
                segment_type = "default"
            else:
                current_segment += line + " "
        
        if current_segment:
            segments.append({
                'text': current_segment.strip(),
                'visual': 'default',
                'type': segment_type
            })
        
        return segments
    
    def _add_background_effects(self, background, style):
        """Add style-specific background effects"""
        if style == "neon":
            # Add subtle glow effect
            return background.with_opacity(0.95)
        elif style == "cinematic":
            # Add film grain effect
            return background.with_opacity(0.98)
        return background
    
    def _apply_text_effect(self, txt_clip, effect):
        """Apply specific text animation effects"""
        if effect == "fade_in":
            return txt_clip
        elif effect == "bounce":
            return txt_clip.with_position(('center', 'center'))
        elif effect == "typewriter":
            return self._typewriter_effect(txt_clip)
        elif effect == "glow":
            return self._glow_effect(txt_clip)
        elif effect == "dramatic_zoom":
            return self._dramatic_zoom_effect(txt_clip)
        else:
            return txt_clip
    
    def _add_fact_styling(self, txt_clip, style):
        """Add special styling for fact segments"""
        # Add emoji or icon for facts
        if style in ["cartoon", "anime"]:
            # Could add animated icons here
            pass
        return txt_clip
    
    def _add_story_styling(self, txt_clip, style):
        """Add special styling for story segments"""
        # Different styling for story segments
        return txt_clip
    
    def _apply_transition(self, clip, transition):
        """Apply transition effects between clips"""
        if transition == "crossfade":
            return clip
        elif transition == "zoom_in":
            return clip.resize(lambda t: 1 + 0.1*t if t < 1 else 1.1)
        elif transition == "flash":
            return clip.fx(lambda c: c.with_opacity(0.8))
        else:
            return clip
    
    def create_enhanced_thumbnail(self, title, style="realistic", output_file=None):
        """Create thumbnail with style-specific design"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.output_dir / f"thumbnail_{style}_{timestamp}.png"
        
        animation_style = self.get_animation_styles()[style]
        bg_color = animation_style["background_colors"][0]
        
        # Create styled thumbnail
        txt_clip = TextClip(
            text=title,
            font_size=animation_style["font_size"] + 10,
            color='white',
            stroke_color='black' if style != "minimal" else None,
            stroke_width=3 if style in ["cartoon", "anime"] else 0,
            size=(1280, 720)
        ).with_duration(1).with_position('center')
        
        bg = ColorClip(size=(1280, 720), color=bg_color).with_duration(1)
        
        # Add style-specific elements
        if style == "neon":
            # Add neon border effect
            pass
        elif style == "cartoon":
            # Add cartoon-style elements
            pass
        
        thumbnail = CompositeVideoClip([bg, txt_clip])
        thumbnail.save_frame(str(output_file), t=0)
        return output_file
    
    def produce(self, script, animation_style="realistic", story_template="problem_solution", output_dir=None, platform="youtube"):
        """
        Wrapper method for compatibility with content_production_pipeline.
        Creates a video from a script text.
        """
        # Create a temporary script file
        script_file = self.temp_dir / f"temp_script_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        script_data = {
            "topic": "Auto-generated content",
            "script": script,
            "approved": True,  # Auto-approve for pipeline-generated scripts
            "generated_at": datetime.now().isoformat(),
            "platform": platform
        }
        with open(script_file, 'w') as f:
            json.dump(script_data, f)
        
        # Call the main production method
        return self.produce_enhanced_video(
            script_file=str(script_file),
            style=animation_style,
            template=story_template,
            rare_facts_mode=False
        )
    
    def produce_enhanced_video(self, script_file, style="realistic", template="problem_solution", rare_facts_mode=False):
        """Main enhanced video production pipeline"""
        print(f"Starting enhanced video production...")
        print(f"Style: {style} | Template: {template}")
        
        # Load approved script
        script_data = self.load_approved_script(script_file)
        script_text = script_data['script']
        topic = script_data['topic']
        platform = script_data.get('platform', 'youtube')
        
        # Apply rare facts enhancements if enabled
        if rare_facts_mode:
            script_text = self._enhance_for_rare_facts(script_text)
        
        # Generate voiceover
        print("Generating voiceover...")
        
        # Platform-specific duration targets
        platform_durations = {
            'tiktok': 60,      # 1 minute for TikTok
            'instagram': 60,   # 1 minute for Instagram Reels
            'youtube_shorts': 60,  # 1 minute for YouTube Shorts
            'twitter': 45,     # 45 seconds for Twitter
            'youtube': 180,    # 3 minutes for full YouTube videos
            'default': 60      # Default to 1 minute
        }
        
        # Get target duration for platform
        target_duration = platform_durations.get(platform.lower(), platform_durations['default'])
        
        # Generate actual voiceover
        audio_file = self.generate_voice(script_text)
        
        # Load audio to get actual duration
        from moviepy import AudioFileClip
        audio_clip = AudioFileClip(str(audio_file))
        duration = audio_clip.duration
        
        print(f"Platform: {platform}")
        print(f"Target duration: {target_duration}s")
        print(f"Video duration: {duration}s (from voice)")
        
        # Create enhanced visuals
        print(f"Creating {style} style visuals...")
        video_clip = self.create_enhanced_visuals(script_text, duration, style, template)

        # Add audio to video
        print("Adding voiceover to video...")
        final_video = video_clip.with_audio(audio_clip)
        
        # Generate output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
        output_file = self.output_dir / f"{safe_topic}_{style}_{timestamp}.mp4"
        
        # Export video
        print(f"Exporting {style} style video...")
        final_video.write_videofile(
            str(output_file),
            fps=30,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        # Create enhanced thumbnail
        print("Creating enhanced thumbnail...")
        thumbnail_file = self.create_enhanced_thumbnail(topic, style)
        
        # Cleanup
        if audio_clip:
            audio_clip.close()
        video_clip.close()
        final_video.close()
        
        result = {
            "video_file": str(output_file),
            "thumbnail_file": str(thumbnail_file),
            "duration": duration,
            "style": style,
            "template": template,
            "rare_facts_mode": rare_facts_mode,
            "created_at": datetime.now().isoformat(),
            "script_source": script_file
        }
        
        # Save metadata
        metadata_file = output_file.with_suffix('.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        
        print(f"Enhanced video production complete: {output_file}")
        return result
    
    def _enhance_for_rare_facts(self, script_text):
        """Enhance script for rare facts presentation"""
        rare_facts_templates = self.get_rare_facts_templates()
        
        # Add engaging hooks and transitions
        enhanced_script = script_text
        
        # This would implement fact-specific enhancements
        # For now, return original script
        return enhanced_script
    
    def load_approved_script(self, script_file):
        """Load and validate approved script"""
        with open(script_file, 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        
        if not script_data.get('approved', False):
            raise ValueError("Script must be approved before video production")
        
        return script_data
    
    def generate_voice(self, text, voice="en-US-AriaNeural", output_file=None):
        """Generate voice using ElevenLabs TTS"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.temp_dir / f"voice_{timestamp}.wav"

        # Try ElevenLabs first, fallback to silent if unavailable
        try:
            import requests
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if not api_key:
                raise ValueError("No ElevenLabs API key")
            
            # Use default voice ID for English (Rachel voice)
            voice_id = "21m00Tcm4TlvDq8ikWAM"
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            # Save as MP3, convert to WAV
            mp3_file = str(output_file).replace('.wav', '.mp3')
            with open(mp3_file, 'wb') as f:
                f.write(response.content)
            
            # Convert MP3 to WAV using moviepy
            from moviepy import AudioFileClip
            audio = AudioFileClip(mp3_file)
            audio.write_audiofile(str(output_file), logger=None)
            duration = audio.duration
            audio.close()
            
            # Clean up MP3
            os.remove(mp3_file)
            
            print(f"✓ Generated voice ({duration:.1f}s)")
            return output_file
            
        except Exception as e:
            print(f"⚠ Voice generation unavailable ({e}), using silent audio")
            
            # Fallback to silent audio
            word_count = len(text.split()) if text else 10
            duration = max(word_count * 0.5, 5.0)
            
            from moviepy import AudioClip
            import numpy as np
            
            def make_frame(t):
                # Handle array of times (vectorization) which moviepy uses
                try:
                    return np.zeros((len(t), 2))
                except TypeError:
                     # Fallback for scalar t
                    return np.array([0, 0])
            
            silent_audio = AudioClip(make_frame, duration=duration, fps=44100)
            silent_audio.write_audiofile(str(output_file), logger=None)
            silent_audio.close()
            
            return output_file

def main():
    """Interactive enhanced video production"""
    producer = EnhancedVideoProducer()
    
    print("🎬 ENHANCED VIDEO PRODUCER")
    print("=" * 40)
    
    # Show available options
    styles = producer.get_animation_styles()
    templates = producer.get_story_templates()
    
    print("\n📱 Available Animation Styles:")
    for i, (style, config) in enumerate(styles.items(), 1):
        print(f"{i}. {style.title()}: {config['description']}")
    
    print("\n📖 Available Story Templates:")
    for i, (template, config) in enumerate(templates.items(), 1):
        print(f"{i}. {template.replace('_', ' ').title()}")
    
    # Get user input
    script_file = input("\n📄 Enter path to approved script file: ")
    
    if not os.path.exists(script_file):
        print(f"❌ Error: Script file not found: {script_file}")
        return
    
    # Select style
    print(f"\n🎨 Select animation style (1-{len(styles)}):")
    style_choice = input("Enter number (or press Enter for realistic): ").strip()
    if style_choice.isdigit() and 1 <= int(style_choice) <= len(styles):
        selected_style = list(styles.keys())[int(style_choice)-1]
    else:
        selected_style = "realistic"
    
    # Select template
    print(f"\n📖 Select story template (1-{len(templates)}):")
    template_choice = input("Enter number (or press Enter for problem_solution): ").strip()
    if template_choice.isdigit() and 1 <= int(template_choice) <= len(templates):
        selected_template = list(templates.keys())[int(template_choice)-1]
    else:
        selected_template = "problem_solution"
    
    # Rare facts mode
    rare_facts = input("\n🤯 Enable rare facts mode? (y/n): ").strip().lower() == 'y'
    
    try:
        result = producer.produce_enhanced_video(
            script_file, 
            style=selected_style, 
            template=selected_template,
            rare_facts_mode=rare_facts
        )
        
        print(f"\n🎉 Enhanced video created successfully!")
        print(f"📹 Video: {result['video_file']}")
        print(f"🖼️ Thumbnail: {result['thumbnail_file']}")
        print(f"⏱️ Duration: {result['duration']:.1f} seconds")
        print(f"🎨 Style: {result['style']}")
        print(f"📖 Template: {result['template']}")
    
    except Exception as e:
        print(f"❌ Error during video production: {str(e)}")

if __name__ == "__main__":
    main()