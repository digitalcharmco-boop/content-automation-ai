#!/usr/bin/env python3
"""
Branding substitution tool — replace all placeholders in sales page, emails, and copy.

Usage:
  python monetization/rebrand.py --interactive
  python monetization/rebrand.py --config branding_config.json

Example branding_config.json:
{
  "company_name": "My Company",
  "product_name": "AI Automation Toolkit",
  "product_price": "17",
  "product_description": "Unlock 10x faster content production with AI-powered video, social media, and email automation.",
  "checkout_url": "https://gumroad.com/l/my-product",
  "sender_email": "launches@mycompany.com",
  "sender_name": "My Company Team",
  "support_email": "support@mycompany.com",
  "website_url": "https://mycompany.com"
}
"""

import json
import os
import sys
import argparse
from pathlib import Path


# Placeholder map (key -> description for interactive prompts)
PLACEHOLDERS = {
    "{{COMPANY_NAME}}": "Your company/brand name (e.g., 'Moni Labs')",
    "{{PRODUCT_NAME}}": "Product name (e.g., 'ContentFlow AI')",
    "{{PRODUCT_PRICE}}": "Pro tier price in USD (e.g., '97')",
    "{{PRODUCT_DESCRIPTION}}": "One-line product description",
    "{{CHECKOUT_URL}}": "Primary (Pro) checkout link",
    "{{CHECKOUT_URL_STARTER}}": "Starter tier Stripe checkout link",
    "{{CHECKOUT_URL_PRO}}": "Pro tier Stripe checkout link",
    "{{CHECKOUT_URL_AGENCY}}": "Agency tier Stripe checkout link",
    "{{SENDER_EMAIL}}": "Sending email address",
    "{{SENDER_NAME}}": "Sender name used in email sign-offs",
    "{{SUPPORT_EMAIL}}": "Support/reply-to email",
    "{{WEBSITE_URL}}": "Your main website URL",
    # lowercase variants used in email bodies
    "{{sender_name}}": None,
    "{{support_email}}": None,
    "{{checkout_url}}": None,
}

FILES_TO_REBRAND = [
    "monetization/sales_page.html",
    "monetization/checkout_copy.md",
    "monetization/tripwire_page.md",
    "monetization/emails/nurture_emails.md",
    "monetization/emails/cold_outreach.md",
    "monetization/emails/cold_outreach_personalized.md",
]


def interactive_prompt():
    """Prompt user for each placeholder value."""
    config = {}
    print("\n=== Branding Configuration ===\n")
    for placeholder, description in PLACEHOLDERS.items():
        default = ""
        if "price" in description.lower():
            default = "17"
        elif "company" in description.lower():
            default = "My Company"
        elif "product_name" in description.lower():
            default = "AI Automation Toolkit"
        
        prompt_text = f"{placeholder}\n  {description}"
        if default:
            prompt_text += f" [{default}]"
        prompt_text += ": "
        
        value = input(prompt_text).strip() or default
        # Map placeholder to config key (e.g., {{COMPANY_NAME}} -> COMPANY_NAME)
        key = placeholder.strip("{}").strip()
        config[key] = value
    
    return config


def load_config(path):
    """Load branding config from JSON file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            raw_config = json.load(f)
        # Normalize keys to match placeholders
        config = {}
        for k, v in raw_config.items():
            # Allow both snake_case and UPPERCASE keys
            key_upper = k.upper().replace('-', '_')
            config[key_upper] = v
        return config
    except Exception as e:
        print(f"Error loading config from {path}: {e}")
        sys.exit(1)


def build_replacements(config):
    """Convert config dict to placeholder->value replacements."""
    replacements = {}
    for placeholder, description in PLACEHOLDERS.items():
        key = placeholder.strip("{}").strip()
        key_upper = key.upper()
        if description is None:
            # lowercase alias — resolve from uppercase counterpart
            if key_upper in config:
                replacements[placeholder] = str(config[key_upper])
        elif key_upper in config:
            replacements[placeholder] = str(config[key_upper])
    return replacements


def rebrand_file(file_path, replacements):
    """Apply replacements to a single file."""
    if not os.path.exists(file_path):
        print(f"  ⚠ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
        
        # Check if any replacements were made
        if content == original_content:
            print(f"  (no placeholders) {file_path}")
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  OK: {file_path}")
        return True
    except Exception as e:
        print(f"  ERROR rebranding {file_path}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Rebrand sales page, emails, and copy with your company details."
    )
    parser.add_argument(
        '--interactive', action='store_true',
        help='Interactive mode: prompt for each branding value'
    )
    parser.add_argument(
        '--config', type=str, default=None,
        help='Path to branding_config.json file'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='Show what would be replaced without writing'
    )
    args = parser.parse_args()

    # Load config
    if args.config:
        config = load_config(args.config)
        print(f"Loaded config from {args.config}")
    elif args.interactive:
        config = interactive_prompt()
    else:
        print("Please provide --interactive or --config <path>")
        parser.print_help()
        sys.exit(1)

    # Build replacements
    replacements = build_replacements(config)
    
    if not replacements:
        print("No branding values provided. Exiting.")
        sys.exit(1)

    print("\n=== Replacements ===\n")
    for placeholder, value in replacements.items():
        print(f"  {placeholder} -> {value}")

    if args.dry_run:
        print("\n(Dry-run mode: no files modified)")
        return

    # Apply to all files
    print("\n=== Rebranding Files ===\n")
    success_count = 0
    for file_path in FILES_TO_REBRAND:
        if rebrand_file(file_path, replacements):
            success_count += 1

    print(f"\nDone: {success_count}/{len(FILES_TO_REBRAND)} files rebranded")
    
    # Optionally save config for future reference
    config_save_path = "monetization/branding_config.json"
    try:
        # Convert keys back to snake_case for readability
        config_for_save = {}
        for k, v in config.items():
            key_snake = k.lower()
            config_for_save[key_snake] = v
        
        with open(config_save_path, 'w', encoding='utf-8') as f:
            json.dump(config_for_save, f, indent=2)
        print(f"Saved config to {config_save_path}")
    except Exception as e:
        print(f"Warning: Could not save config: {e}")


if __name__ == '__main__':
    main()
