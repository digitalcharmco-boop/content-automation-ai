# Content Automation AI

Automated content creation pipeline with human oversight checkpoints.

## Quick Start

1. **Install Dependencies**
   ```bash
   cd content_automation_ai
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   set OPENAI_API_KEY=your_openai_key
   set AZURE_SPEECH_KEY=your_azure_key (optional)
   ```

3. **Setup YouTube API**
   - Download `credentials.json` from Google Cloud Console
   - Place in content_automation_ai folder

## Usage Workflow

### Step 0: Generate Viral Content Package (NEW!)
```bash
python viral_content_optimizer.py
```
- Generates viral hooks, titles, captions, engagement questions
- Optimized for maximum engagement and CTR
- Must review and select best options

### Step 1: Generate Viral-Optimized Script
```bash
python script_generator.py
```
- Uses advanced viral psychology prompts
- Creates retention-optimized scripts
- Includes production notes for engagement

### Step 2: Create Enhanced Video (NEW!)
```bash
python enhanced_video_producer.py
```
**6 Animation Styles:**
- Realistic (photorealistic with natural lighting)
- Cartoon (bright, colorful animations)  
- Anime (dramatic Japanese animation style)
- Cinematic (movie-style with dramatic effects)
- Minimal (clean, modern design)
- Neon (cyberpunk glow effects)

**5 Story Templates:**
- Hero Journey (transformation arc)
- Problem-Solution (pain point resolution)
- List Format (organized points)
- Story Revelation (mystery building)
- Educational (progressive learning)

**Special Features:**
- Rare Facts Mode (mind-blowing content)
- Cinematic Transitions
- Dynamic Text Effects
- Style-specific Thumbnails

### Step 3: Publish Content
```bash
python publisher.py
```
- **Prepare**: `python publisher.py` → choose "prepare"
- **Approve**: Review upload package, then approve
- **Publish**: Upload to YouTube and generate social posts

## Human Oversight Points

✅ **Script Review** - Must approve all scripts before video creation
✅ **Upload Approval** - Must approve before YouTube publishing  
✅ **Privacy Control** - Videos start as private for review

## File Structure

```
content_automation_ai/
├── script_generator.py    # AI script drafting
├── video_producer.py      # Video creation pipeline
├── publisher.py           # YouTube/social publishing
├── requirements.txt       # Dependencies
├── videos/               # Created videos
├── pending_uploads/      # Approval queue
└── temp/                # Processing files
```