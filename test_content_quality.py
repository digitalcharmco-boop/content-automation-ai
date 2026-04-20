#!/usr/bin/env python3
"""
ContentFlow AI — Live Quality Test
Runs the viral optimizer + script generator on a real topic and prints
everything so you can judge output quality before going live.

Usage:
  python test_content_quality.py
  python test_content_quality.py --topic "how to make money with AI content" --audience "content creators" --platform tiktok
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

from viral_content_optimizer import ViralContentOptimizer
from script_generator import ScriptGenerator

SEP = "=" * 70
THIN = "-" * 70


def print_section(title, content):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)
    if isinstance(content, list):
        for i, item in enumerate(content, 1):
            print(f"\n  {i}. {item}")
    else:
        print(content)


def run_test(topic, audience, platform):
    print(f"\n{SEP}")
    print(f"  CONTENTFLOW AI — CONTENT QUALITY TEST")
    print(f"  Topic    : {topic}")
    print(f"  Audience : {audience}")
    print(f"  Platform : {platform}")
    print(SEP)

    # ── 1. HOOKS ────────────────────────────────────────────────────
    print("\n[1/4] Generating viral hooks...")
    optimizer = ViralContentOptimizer()
    hooks_data = optimizer.generate_viral_hooks(topic, audience)

    if "error" in hooks_data:
        print(f"  ERROR: {hooks_data['error']}")
        sys.exit(1)

    hooks = hooks_data.get("hooks", [])
    print_section("VIRAL HOOKS (10 variations)", hooks)

    # ── 2. TITLES ───────────────────────────────────────────────────
    print(f"\n[2/4] Generating titles...")
    titles_data = optimizer.generate_viral_titles(topic, niche=audience)
    titles = titles_data.get("titles", [])
    print_section("VIDEO TITLES (8 variations)", titles)

    # ── 3. CAPTIONS ─────────────────────────────────────────────────
    print(f"\n[3/4] Generating captions for {platform.upper()}...")
    captions_data = optimizer.generate_viral_captions(topic, platform=platform)
    captions = captions_data.get("captions", [])

    print(f"\n{SEP}")
    print(f"  PLATFORM CAPTIONS — {platform.upper()} (5 variations)")
    print(SEP)
    for i, cap in enumerate(captions, 1):
        print(f"\n  [{i}] {cap}")
        print(THIN)

    # ── 4. SCRIPT ───────────────────────────────────────────────────
    print(f"\n[4/4] Generating full video script...")
    generator = ScriptGenerator()

    best_hook = hooks[0] if hooks else topic
    outline = f"""
    Hook: {best_hook}
    Problem: Why most people fail at {topic}
    Solution: The actual approach that works
    Proof: Specific example / result
    CTA: Engagement question + next step
    """

    script_data = generator.generate_script_draft(topic, outline, target_duration=90)

    if "error" in script_data:
        print(f"  ERROR: {script_data['error']}")
    else:
        print(f"\n{SEP}")
        print(f"  FULL VIDEO SCRIPT (90-second optimized)")
        print(SEP)
        print(f"\n  Word count : {script_data.get('word_count', '?')}")
        print(f"\n{script_data.get('script', '')}")

    # ── ENGAGEMENT QUESTIONS ────────────────────────────────────────
    print(f"\n[+] Generating engagement questions...")
    eq_data = optimizer.generate_engagement_questions(topic)
    questions = eq_data.get("questions", [])
    print_section("ENGAGEMENT QUESTIONS (comment drivers)", questions)

    # ── SUMMARY ─────────────────────────────────────────────────────
    print(f"\n{SEP}")
    print(f"  TEST COMPLETE")
    print(SEP)
    print(f"""
  Generated:
    {len(hooks)} hooks
    {len(titles)} titles
    {len(captions)} captions ({platform})
    {len(questions)} engagement questions
    1 full video script

  Best hook to use:
    "{hooks[0] if hooks else 'N/A'}"

  Best title to use:
    "{titles[0] if titles else 'N/A'}"
""")


def main():
    parser = argparse.ArgumentParser(description='ContentFlow AI quality test')
    parser.add_argument('--topic', default='how to make $500 this week with AI content',
                        help='Content topic to test')
    parser.add_argument('--audience', default='content creators and side hustlers',
                        help='Target audience description')
    parser.add_argument('--platform', default='tiktok',
                        choices=['youtube', 'tiktok', 'instagram', 'twitter'],
                        help='Target platform for captions')
    args = parser.parse_args()

    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY not set in .env")
        sys.exit(1)

    run_test(args.topic, args.audience, args.platform)


if __name__ == '__main__':
    main()
