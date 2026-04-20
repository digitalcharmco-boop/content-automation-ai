#!/usr/bin/env python3
"""
Script Drafting Assistant with Human Review
Generates initial script drafts that require human approval before proceeding.
"""

import os
import json
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ScriptGenerator:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None
    
    def generate(self, topic, target_audience="general", retention_focus=True, target_duration=300):
        """Wrapper method for pipeline compatibility - generates script with default outline"""
        default_outline = f"""
        1. Hook - Attention grabbing opening
        2. Problem - Identify the challenge
        3. Solution - Provide the answer
        4. Proof - Share results/evidence
        5. CTA - Call to action
        """
        
        # Try AI generation first, fallback to template if no API key
        if self.client:
            result = self.generate_script_draft(topic, default_outline, target_duration)
            # Return just the script text for pipeline compatibility
            if isinstance(result, dict):
                return result.get('script', self._generate_fallback_script(topic, target_duration))
            return str(result)
        else:
            # Use fallback template when no API key available
            return self._generate_fallback_script(topic, target_duration)
    
    def _generate_fallback_script(self, topic, target_duration=300):
        """Generate a basic script template when AI is not available"""
        # Calculate approximate segments based on duration (150 words per minute speaking pace)
        words_per_minute = 150
        total_words = int((target_duration / 60) * words_per_minute)
        
        # Create engaging script segments
        segments = []
        
        # Hook (10% of script)
        hook_words = int(total_words * 0.10)
        segments.append(f"Have you ever wondered about {topic}? Today I'm revealing the secrets that most people don't know.")
        
        # Problem (20% of script)
        problem_words = int(total_words * 0.20)
        segments.append(f"The biggest challenge with {topic} is that most people approach it all wrong. They make common mistakes that hold them back from real results.")
        
        # Solution (40% of script - main content)
        solution_words = int(total_words * 0.40)
        segments.append(f"Let me share the proven approach to {topic}. First, you need to understand the fundamentals. Second, implement the right strategy. Third, avoid the pitfalls that trip up beginners.")
        segments.append(f"Here's what actually works with {topic}: focus on consistency over perfection. Start small, build momentum, and watch the compound effects multiply over time.")
        
        # Proof (20% of script)
        proof_words = int(total_words * 0.20)
        segments.append(f"This approach to {topic} has been proven time and time again. Countless people have achieved remarkable results by following these exact principles.")
        
        # CTA (10% of script)
        cta_words = int(total_words * 0.10)
        segments.append(f"Now it's your turn to take action on {topic}. Start today, stay consistent, and comment below with your progress. What's your biggest question about {topic}?")
        
        # Join segments with proper spacing
        full_script = " ".join(segments)
        
        # Ensure we hit approximate word count
        words = full_script.split()
        if len(words) < total_words:
            # Add more detail to solution section
            extra = f"When it comes to {topic}, remember that small daily actions compound into massive results. Focus on progress, not perfection. Track your journey, celebrate small wins, and keep pushing forward."
            full_script += " " + extra
        
        return full_script
    
    def generate_script_draft(self, topic, outline, target_duration=300):
        """Generate initial script draft from topic and outline"""
        
        # High-retention viral script prompt
        words_target = int((target_duration / 60) * 140)  # ~140 wpm for natural speech
        prompt = f"""You are a top-performing short-form content creator. Your videos regularly hit 500k-2M views because you give REAL, specific, actionable content — not vague motivational fluff.

Write a {target_duration}-second video script (approximately {words_target} words spoken) for:
Topic: {topic}
Outline: {outline}

SCRIPT STRUCTURE (follow this exactly):

[0-8 sec] HOOK — One sentence. Pattern interrupt or bold specific claim. Must make someone stop scrolling. No "Hey guys" or "In today's video." Start mid-thought.

[8-20 sec] PROBLEM — Name the exact frustration or mistake in 2-3 sentences. Be specific. Use "you" language. Make the viewer feel seen.

[20-{int(target_duration * 0.6)} sec] MEAT — The actual content. Give REAL, specific steps, facts, or methods. If you say "step 1", actually explain it. Include:
  - At least one specific number, example, or real detail
  - One "most people do X, but actually Y" inversion
  - One mini-curiosity loop ("I'll show you why in a second...")
  - Speak as if talking to one specific person

[{int(target_duration * 0.6)}-{int(target_duration * 0.85)} sec] PROOF/PAYOFF — One concrete example, result, or demonstration. Specific > general. "This got me 47k views" beats "this went viral."

[{int(target_duration * 0.85)}-{target_duration} sec] CTA + ENGAGEMENT — One natural ask. End with a question that creates debate or invites personal stories — NOT "like and subscribe."

RULES:
- Write ONLY the spoken words — no stage directions, no [VISUAL] tags, no tone markers
- Every sentence must earn its place. Cut anything vague.
- No phrases like: "In today's video", "Don't forget to like", "As you can see", "Essentially", "Let me explain"
- No fake energy — sound like a real person sharing something they actually know
- Specific details make content go viral. Vague content gets skipped.
- Do NOT name specific third-party tools or apps (they date poorly and feel like ads). Describe the capability instead.
- The proof/result section must include a specific number, timeframe, or outcome. No "it worked great" — say exactly what happened.
- The CTA question must invite a genuine debate or personal story, not a yes/no answer.

Write the script now. Spoken words only."""
        
        try:
            if not self.client:
                raise Exception("OpenAI API key not configured")
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            script = response.choices[0].message.content
            return self._format_script(script, topic)
            
        except Exception as e:
            return {"error": f"Failed to generate script: {str(e)}"}
    
    def _format_script(self, script, topic):
        """Format script with metadata"""
        return {
            "topic": topic,
            "generated_at": datetime.now().isoformat(),
            "script": script,
            "status": "draft",
            "word_count": len(script.split()),
            "approved": False
        }
    
    def save_draft(self, script_data, filename=None):
        """Save script draft for human review"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"script_draft_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        print(f"Script draft saved to: {filename}")
        print("HUMAN REVIEW REQUIRED: Please review and approve before proceeding")
        return filename
    
    def approve_script(self, filename):
        """Mark script as approved after human review"""
        with open(filename, 'r', encoding='utf-8') as f:
            script_data = json.load(f)
        
        script_data['approved'] = True
        script_data['approved_at'] = datetime.now().isoformat()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)
        
        print(f"Script approved: {filename}")
        return script_data

def main():
    """Interactive script generation with human review checkpoint"""
    generator = ScriptGenerator()
    
    # Get input from user
    topic = input("Enter video topic: ")
    outline = input("Enter outline/key points: ")
    duration = int(input("Target duration (seconds, default 300): ") or 300)
    
    # Generate draft
    print("\nGenerating script draft...")
    script_data = generator.generate_script_draft(topic, outline, duration)
    
    if "error" in script_data:
        print(f"Error: {script_data['error']}")
        return
    
    # Save for review
    filename = generator.save_draft(script_data)
    
    # Wait for human approval
    print(f"\nPlease review the script in: {filename}")
    print("Edit the script as needed, then run:")
    print(f"python -c \"from script_generator import ScriptGenerator; ScriptGenerator().approve_script('{filename}')\"")

if __name__ == "__main__":
    main()