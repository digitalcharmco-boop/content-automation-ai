#!/usr/bin/env python3
"""
Viral Content Optimizer
Generates platform-optimized hooks, captions, titles, and engagement questions
using GPT-4o with niche-aware prompting for maximum organic reach.
"""

import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class ViralContentOptimizer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        self.model = "gpt-4o"

    def _call(self, prompt, max_tokens=1200, temperature=0.85):
        if not self.client:
            return None
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content

    def generate_viral_hooks(self, topic, target_audience="general", emotion="curiosity"):
        prompt = f"""You are a viral short-form content strategist who has grown multiple accounts past 100k.

Generate 10 viral video hooks for:
Topic: "{topic}"
Audience: {target_audience}
Core emotion to trigger: {emotion}

HOOK FRAMEWORKS — use a different one for each:
1. PATTERN INTERRUPT — "Stop scrolling if you [specific relatable thing]"
2. CURIOSITY GAP — "The one thing nobody tells you about [topic]"
3. CONTROVERSY — "Unpopular opinion: [bold specific claim about topic]"
4. STAT SHOCK — "[Specific surprising number]% of people [relevant behavior]"
5. PERSONAL STORY — "I lost/made/discovered [specific result] when I [action]"
6. QUESTION HOOK — "What if the reason you're [pain point] is actually [surprising cause]"
7. TRANSFORMATION — "I went from [specific low state] to [specific high state] in [timeframe]"
8. SECRET REVEAL — "The [industry/expert] secret behind [specific outcome]"
9. PAIN POINT — "If you're [specific struggle], you're not doing [specific thing] wrong"
10. URGENCY — "This [specific thing] changes everything after [specific trigger]"

RULES:
- Be SPECIFIC to the topic — no generic filler
- Each hook must work as a standalone first sentence for a TikTok/Reel/Short
- Use concrete specifics: numbers, timeframes, emotions, named outcomes
- Maximum 12 words per hook
- DO NOT start multiple hooks the same way

Return as a numbered list. Hook text only — no labels or explanations."""

        text = self._call(prompt)
        if not text:
            return {"error": "No API key configured"}
        return self._parse_lines(text, topic, "hooks")

    def generate_viral_captions(self, topic, video_length="short", platform="youtube"):
        platform_specs = {
            "youtube": {
                "hashtags": "3-5",
                "length": "150-220 characters before hashtags",
                "cta": "comment your answer below",
                "style": "curious, storytelling, conversational"
            },
            "tiktok": {
                "hashtags": "5-8 trending tags",
                "length": "80-120 characters before hashtags",
                "cta": "follow for part 2",
                "style": "punchy, slang-friendly, trend-aware"
            },
            "instagram": {
                "hashtags": "10-15 niche-specific tags",
                "length": "100-180 characters before hashtags",
                "cta": "save this for later",
                "style": "aspirational, personal, aesthetic"
            },
            "twitter": {
                "hashtags": "1-2 only",
                "length": "200-240 characters total",
                "cta": "repost if this hit",
                "style": "punchy, opinion-forward, thread-worthy"
            }
        }
        specs = platform_specs.get(platform, platform_specs["youtube"])

        prompt = f"""You are a top-performing {platform.upper()} creator known for captions that stop thumbs and drive real engagement.

Write 5 caption variations for a {video_length} video about: "{topic}"

Platform rules:
- {specs['hashtags']} hashtags
- Caption length: {specs['length']}
- Style: {specs['style']}
- CTA must feel natural, not forced: "{specs['cta']}"

CAPTION FRAMEWORKS — use one per variation:
1. STORY ARC: Compress a relatable mini-story into 2 sentences, then ask a question
2. BOLD CLAIM: Open with a controversial-but-true statement, back it with one fact, end with CTA
3. FOMO: "Everyone who [did X] already knows this…" — then reveal the insight
4. PERSONAL SHARE: First-person specific moment → universal truth → audience question
5. LIST TEASE: "3 things I wish I knew about [topic]: (1) … (2) … (3) watch to find out"

Each caption MUST:
- Open with a hook word or phrase in the first 3 words
- Be specific to the topic — no filler phrases
- Include relevant hashtags at the end
- End with the natural CTA

Return each as:
Caption [N] ([Framework]):
[Full caption with hashtags]"""

        text = self._call(prompt, max_tokens=1600)
        if not text:
            return {"error": "No API key configured"}
        return self._parse_captions(text, topic, platform)

    def generate_viral_titles(self, topic, niche="general"):
        prompt = f"""You are a YouTube SEO and CTR specialist. Your titles routinely hit 8-12% CTR.

Write 8 YouTube video titles for: "{topic}"
Niche: {niche}

TITLE FORMULAS — use one per title:
1. HOW-TO + SPECIFIC RESULT: "How I [specific outcome] in [timeframe] (No [common excuse])"
2. MISTAKE EXPOSE: "The [#] [topic] Mistakes Killing Your [specific outcome]"
3. SECRET REVEAL: "The [niche] Secret Behind [specific desirable result]"
4. TRANSFORMATION: "From [specific low] to [specific high] in [timeframe] — Here's How"
5. CONTROVERSIAL TRUTH: "Why [Popular Belief About Topic] Is Actually Costing You [specific thing]"
6. RANKED LIST: "[#] Things About [Topic] Nobody Talks About (But Should)"
7. URGENT WARNING: "Stop [Specific Common Action] Before You [Specific Consequence]"
8. INSIDER BREAKDOWN: "I Tried [Topic Method] for [Timeframe] — Honest Results"

RULES:
- 55-70 characters (sweet spot for desktop + mobile)
- Include at least one power word per title: secret, exposed, mistake, truth, revealed, stop, why, how
- NO clickbait — every title must deliver on its promise
- Be SPECIFIC — avoid vague words like "amazing", "great", "incredible"
- Use numbers when possible

Return as numbered list. Title text only."""

        text = self._call(prompt, max_tokens=900)
        if not text:
            return {"error": "No API key configured"}
        return self._parse_lines(text, topic, "titles")

    def generate_engagement_questions(self, topic):
        prompt = f"""You drive 500+ comments per video. Write 5 engagement questions for a video about "{topic}".

QUESTION TYPES — one of each:
1. OPINION POLL: Force a choice between two real positions people hold about {topic}
2. STORY REQUEST: Ask for a specific personal experience related to {topic}
3. DEBATE STARTER: Ask something controversial enough to create two camps
4. PREDICTION: Ask what they think will happen if they [do/don't do] something related to {topic}
5. IDENTITY: Ask which "type" they are — people love sorting themselves

RULES:
- Questions must feel like genuine curiosity, not a survey
- Use "you" language
- Include 1-2 relevant emojis
- Each question should make someone want to type a real answer, not just "yes" or "no"
- Be specific to the topic — no generic "what do you think?" filler

Return as numbered list. Question text only."""

        text = self._call(prompt, max_tokens=700)
        if not text:
            return {"error": "No API key configured"}
        return self._parse_lines(text, topic, "questions")

    def _parse_lines(self, text, topic, key):
        lines = [l.strip() for l in text.strip().split('\n') if l.strip() and l.strip()[0].isdigit()]
        return {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            key: lines,
            f"total_{key}": len(lines)
        }

    def _parse_captions(self, text, topic, platform):
        sections = []
        current = []
        for line in text.strip().split('\n'):
            if line.startswith('Caption ') and current:
                sections.append('\n'.join(current).strip())
                current = [line]
            else:
                current.append(line)
        if current:
            sections.append('\n'.join(current).strip())
        return {
            "topic": topic,
            "platform": platform,
            "generated_at": datetime.now().isoformat(),
            "captions": sections,
            "total_variations": len(sections)
        }

    def generate_complete_viral_package(self, topic, target_audience="general", platform="youtube"):
        print(f"  Generating viral package: '{topic}' | audience: {target_audience} | platform: {platform}")

        hooks = self.generate_viral_hooks(topic, target_audience)
        captions = self.generate_viral_captions(topic, platform=platform)
        titles = self.generate_viral_titles(topic, niche=target_audience)
        questions = self.generate_engagement_questions(topic)

        viral_package = {
            "topic": topic,
            "target_audience": target_audience,
            "platform": platform,
            "generated_at": datetime.now().isoformat(),
            "hooks": hooks,
            "captions": captions,
            "titles": titles,
            "engagement_questions": questions,
            "status": "pending_review"
        }

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"viral_package_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(viral_package, f, indent=2, ensure_ascii=False)

        print(f"  Saved: {filename}")
        return viral_package
