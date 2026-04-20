#!/usr/bin/env python3
"""
Universal Viral Prompt Template Generator
Creates high-engagement content prompts for any topic/niche using proven viral psychology.
"""

import os
import json
from datetime import datetime

class UniversalViralPromptGenerator:
    def __init__(self):
        self.viral_template = """
        {topic_intro} content exploring {main_angle}, {secondary_angle}, and {hook_elements} in {context_area}, designed to drive traffic and conversions by highlighting actionable insights and problem-solving.
        
        Focus on {primary_subtopics}, {engagement_triggers}, {authority_elements}, {curiosity_gaps}, {transformation_stories}, {expert_insights}, {actionable_frameworks}, {case_studies}, {problem_solutions}, {results_evidence}, {social_proof_elements}, {urgency_factors}, {value_demonstrations}, {credibility_markers}, {exclusive_insights}, {behind_the_scenes}, {contrarian_viewpoints}, {myth_busting}, {step_by_step_processes}, {tools_and_resources}.
        
        Emphasize {credibility_sources} from {authority_domains} and {proof_elements}, {implementation_value} for {target_outcome}, {delivery_mechanism} for individuals seeking {desired_result}, {success_stories} of {achievement_examples}, {cta_alignment} for {conversion_goals}. 
        
        Include specific details about {mechanism_explanation}, {real_examples} illustrating their {impact_description}, {precise_identification} for {detection_methods}, {clear_action_steps} for {implementation_process}, and {long_term_benefits} for {target_beneficiaries}.
        
        Stories should feature: {story_elements}, {social_proof_stories}, {expert_validation}, {transformation_narratives}, and {prevention_strategies}.
        
        Focus on {empowerment_angle} with {knowledge_delivery} to {navigate_challenges} and {overcome_obstacles}, providing {critical_value} that {solves_problems} and {drives_engagement} towards {solution_direction} and {resource_destination}.
        
        IT'S EXTREMELY IMPORTANT THAT THE CONTENT PROVIDES {outcome_promise} AND {clear_pathway} TO {ultimate_goal}.
        """
    
    def generate_niche_prompt(self, niche_data):
        """Generate viral content prompt for specific niche"""
        return self.viral_template.format(**niche_data)
    
    def get_dark_psychology_template(self):
        """Returns the analyzed dark psychology template structure"""
        return {
            "topic_intro": "Dark relationship psychology",
            "main_angle": "manipulative tactics, toxic dynamics",
            "secondary_angle": "covert influence strategies",
            "hook_elements": "psychological warfare techniques", 
            "context_area": "interpersonal connections",
            
            "primary_subtopics": "narcissistic abuse/covert narcissism/malignant narcissism, gaslighting techniques/reality distortion/memory manipulation, emotional blackmail/guilt-tripping/obligation induction",
            
            "engagement_triggers": "love bombing/idealize-devalue-discard cycle/hoovering, silent treatment/stonewalling/passive aggression, triangulation/divide and conquer/sowing discord",
            
            "authority_elements": "psychological research and case studies",
            "curiosity_gaps": "covert manipulation techniques most people don't recognize",
            "transformation_stories": "healing from abuse/setting boundaries/rebuilding self-worth",
            
            "credibility_sources": "credibility markers/authority signals",
            "authority_domains": "psychological research and case studies",
            "proof_elements": "case studies/proven results of understanding these dynamics",
            
            "target_outcome": "identification and defense against manipulation",
            "delivery_mechanism": "actionable insights/practical applications",
            "desired_result": "protection from toxic relationships",
            
            "outcome_promise": "ACTIONABLE SOLUTIONS",
            "clear_pathway": "CLEAR PATHWAYS TO IMPROVEMENT",
            "ultimate_goal": "ESCAPE FROM TOXIC DYNAMICS"
        }
    
    def create_custom_niche_templates(self):
        """Generate templates for various profitable niches"""
        
        templates = {
            "fitness_weight_loss": {
                "topic_intro": "Advanced fitness and weight loss science",
                "main_angle": "metabolism hacking, fat burning secrets",
                "secondary_angle": "body transformation strategies",
                "hook_elements": "hidden weight loss triggers",
                "context_area": "body composition optimization",
                "primary_subtopics": "intermittent fasting protocols/autophagy activation/insulin sensitivity, HIIT vs steady cardio/fat burning zones/exercise efficiency, macronutrient timing/protein synthesis/carb cycling",
                "engagement_triggers": "plateau breaking techniques/metabolic confusion/body adaptation, supplement stacking/natural fat burners/thermogenesis, sleep optimization/stress cortisol/hormone balance",
                "authority_elements": "peer-reviewed fitness studies and transformation case studies",
                "target_outcome": "rapid fat loss and muscle preservation",
                "outcome_promise": "PROVEN TRANSFORMATION METHODS",
                "ultimate_goal": "SUSTAINABLE BODY TRANSFORMATION"
            },
            
            "make_money_online": {
                "topic_intro": "Underground online income strategies",
                "main_angle": "passive income systems, digital wealth building",
                "secondary_angle": "financial freedom blueprints",
                "hook_elements": "income generation secrets",
                "context_area": "digital entrepreneurship",
                "primary_subtopics": "affiliate marketing funnels/high-ticket sales/commission structures, dropshipping automation/product research/supplier networks, course creation/knowledge monetization/audience building",
                "engagement_triggers": "scaling strategies/income multiplication/passive systems, traffic generation/SEO secrets/viral marketing, conversion optimization/sales psychology/buyer behavior",
                "authority_elements": "verified income reports and student success stories",
                "target_outcome": "consistent online income generation",
                "outcome_promise": "ACTIONABLE INCOME STRATEGIES",
                "ultimate_goal": "FINANCIAL INDEPENDENCE ONLINE"
            },
            
            "dating_relationships": {
                "topic_intro": "Advanced dating psychology and attraction science",
                "main_angle": "human attraction mechanics, relationship dynamics",
                "secondary_angle": "social influence mastery",
                "hook_elements": "hidden attraction triggers",
                "context_area": "modern dating landscape",
                "primary_subtopics": "attraction psychology/evolutionary triggers/subconscious signals, conversation mastery/emotional connection/rapport building, confidence building/inner game/self-worth development",
                "engagement_triggers": "dating app optimization/profile psychology/matching algorithms, text game/messaging strategies/response psychology, approach anxiety/rejection handling/resilience building",
                "authority_elements": "behavioral psychology research and dating success studies",
                "target_outcome": "authentic connection and relationship success",
                "outcome_promise": "PROVEN ATTRACTION STRATEGIES",
                "ultimate_goal": "MEANINGFUL RELATIONSHIP SUCCESS"
            },
            
            "personal_development": {
                "topic_intro": "Peak performance psychology and mindset mastery",
                "main_angle": "consciousness hacking, mental optimization",
                "secondary_angle": "elite performance strategies",
                "hook_elements": "hidden potential activation methods",
                "context_area": "human achievement and fulfillment",
                "primary_subtopics": "neuroplasticity training/brain rewiring/cognitive enhancement, habit formation/behavior change/neural pathways, mindfulness practices/meditation techniques/awareness cultivation",
                "engagement_triggers": "productivity hacking/focus optimization/flow states, goal achievement/visualization/manifestation, emotional intelligence/self-regulation/stress mastery",
                "authority_elements": "neuroscience research and high-achiever case studies",
                "target_outcome": "peak performance and life satisfaction",
                "outcome_promise": "TRANSFORMATIONAL GROWTH METHODS",
                "ultimate_goal": "UNLIMITED PERSONAL POTENTIAL"
            },
            
            "health_longevity": {
                "topic_intro": "Cutting-edge longevity science and biohacking",
                "main_angle": "cellular optimization, anti-aging protocols",
                "secondary_angle": "lifespan extension strategies",
                "hook_elements": "biological age reversal techniques",
                "context_area": "optimal human health and longevity",
                "primary_subtopics": "mitochondrial health/cellular energy/oxidative stress, telomere optimization/DNA repair/genetic expression, hormone optimization/endocrine balance/youth restoration",
                "engagement_triggers": "biohacking protocols/quantified self/biomarker tracking, supplementation strategies/nootropics/nutrient optimization, recovery optimization/sleep quality/stress reduction",
                "authority_elements": "longevity research and clinical studies",
                "target_outcome": "extended healthspan and vitality",
                "outcome_promise": "SCIENCE-BASED LONGEVITY STRATEGIES",
                "ultimate_goal": "OPTIMIZED HEALTH AND LONGEVITY"
            }
        }
        
        return templates
    
    def generate_viral_prompt_for_topic(self, topic_name, custom_elements=None):
        """Generate complete viral prompt for any topic"""
        
        templates = self.create_custom_niche_templates()
        
        if topic_name in templates:
            template_data = templates[topic_name]
        else:
            # Create basic template for unknown topics
            template_data = {
                "topic_intro": f"Advanced {topic_name} strategies",
                "main_angle": f"{topic_name} optimization techniques",
                "secondary_angle": f"expert-level {topic_name} methods",
                "hook_elements": f"hidden {topic_name} secrets",
                "context_area": f"{topic_name} mastery",
                "primary_subtopics": f"core {topic_name} principles",
                "engagement_triggers": f"advanced {topic_name} strategies",
                "authority_elements": f"{topic_name} research and case studies",
                "target_outcome": f"{topic_name} success",
                "outcome_promise": f"PROVEN {topic_name.upper()} METHODS",
                "ultimate_goal": f"{topic_name.upper()} MASTERY"
            }
        
        # Override with custom elements if provided
        if custom_elements:
            template_data.update(custom_elements)
        
        # Fill in remaining template variables with defaults
        default_values = {
            "curiosity_gaps": f"secrets most people don't know about {topic_name}",
            "transformation_stories": f"success stories and breakthrough moments",
            "expert_insights": f"insider knowledge and expert perspectives",
            "actionable_frameworks": f"step-by-step implementation guides",
            "case_studies": f"real-world examples and proof",
            "problem_solutions": f"common challenges and solutions",
            "results_evidence": f"verified results and outcomes",
            "social_proof_elements": f"testimonials and success stories",
            "urgency_factors": f"time-sensitive opportunities",
            "value_demonstrations": f"clear benefits and transformations",
            "credibility_markers": f"expert credentials and proof",
            "exclusive_insights": f"insider information and secrets",
            "behind_the_scenes": f"how it really works",
            "contrarian_viewpoints": f"unconventional approaches",
            "myth_busting": f"common misconceptions exposed",
            "step_by_step_processes": f"detailed implementation guides",
            "tools_and_resources": f"recommended tools and resources",
            "credibility_sources": f"research-backed evidence",
            "authority_domains": f"expert studies and analysis",
            "proof_elements": f"documented results and case studies",
            "implementation_value": f"practical application methods",
            "delivery_mechanism": f"actionable insights and strategies",
            "desired_result": f"{topic_name} success and mastery",
            "success_stories": f"transformation case studies",
            "achievement_examples": f"real success examples",
            "cta_alignment": f"conversion-optimized calls to action",
            "conversion_goals": f"related products and services",
            "mechanism_explanation": f"how the methods work",
            "real_examples": f"real-world applications",
            "impact_description": f"measurable results and outcomes",
            "precise_identification": f"specific techniques and methods",
            "detection_methods": f"recognition and identification",
            "clear_action_steps": f"implementation roadmap",
            "implementation_process": f"step-by-step execution",
            "long_term_benefits": f"sustained results and growth",
            "target_beneficiaries": f"ideal candidates and users",
            "story_elements": f"compelling narratives and examples",
            "social_proof_stories": f"success testimonials",
            "expert_validation": f"authority endorsements",
            "transformation_narratives": f"before and after stories",
            "prevention_strategies": f"avoiding common mistakes",
            "empowerment_angle": f"knowledge-based empowerment",
            "knowledge_delivery": f"expert information sharing",
            "navigate_challenges": f"overcome obstacles",
            "overcome_obstacles": f"solve common problems",
            "critical_value": f"essential information",
            "solves_problems": f"addresses key challenges",
            "drives_engagement": f"creates strong interest",
            "solution_direction": f"expert guidance",
            "resource_destination": f"additional resources and tools",
            "clear_pathway": f"CLEAR STEPS TO SUCCESS"
        }
        
        # Merge template data with defaults
        for key, value in default_values.items():
            if key not in template_data:
                template_data[key] = value
        
        return self.generate_niche_prompt(template_data)
    
    def save_prompt_template(self, topic_name, prompt_content):
        """Save generated prompt template to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"viral_prompt_{topic_name}_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Viral Content Prompt for {topic_name.title()}\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write(prompt_content)
        
        print(f"Viral prompt saved: {filename}")
        return filename

def main():
    """Interactive viral prompt generation"""
    generator = UniversalViralPromptGenerator()
    
    print("=== UNIVERSAL VIRAL PROMPT GENERATOR ===")
    print("\nAvailable niche templates:")
    templates = generator.create_custom_niche_templates()
    for i, niche in enumerate(templates.keys(), 1):
        print(f"{i}. {niche.replace('_', ' ').title()}")
    
    choice = input(f"\nEnter topic name (or number 1-{len(templates)}): ").strip()
    
    # Handle numeric choice
    if choice.isdigit():
        choice_num = int(choice) - 1
        if 0 <= choice_num < len(templates):
            topic_name = list(templates.keys())[choice_num]
        else:
            print("Invalid number. Using custom topic.")
            topic_name = input("Enter custom topic name: ").strip()
    else:
        topic_name = choice.lower().replace(' ', '_')
    
    # Generate viral prompt
    viral_prompt = generator.generate_viral_prompt_for_topic(topic_name)
    
    print(f"\n{'='*50}")
    print(f"VIRAL PROMPT FOR: {topic_name.replace('_', ' ').upper()}")
    print(f"{'='*50}")
    print(viral_prompt)
    
    # Save to file
    filename = generator.save_prompt_template(topic_name, viral_prompt)
    print(f"\nPrompt saved to: {filename}")

if __name__ == "__main__":
    main()