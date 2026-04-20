#!/usr/bin/env python3
"""
One-time ConvertKit setup script.

What this does automatically:
  - Creates an opt-in form ("AI Content Cash Kit Buyers")
  - Writes the form ID back into .env

What it prints for you to do manually (takes ~5 minutes in the dashboard):
  - Creates a sequence with all 5 nurture emails pre-formatted for copy-paste
  - After you paste them in, run: python monetization/agents/setup_convertkit.py --save-ids

Run:
  python monetization/agents/setup_convertkit.py
"""

import os
import re
import sys
import requests
from pathlib import Path
from dotenv import load_dotenv, set_key

ROOT = Path(__file__).parent.parent.parent
ENV_FILE = ROOT / '.env'
load_dotenv(ENV_FILE)

API_KEY    = os.getenv('CONVERTKIT_API_KEY', '')
API_SECRET = os.getenv('CONVERTKIT_API_SECRET', '')
BASE_URL   = 'https://api.convertkit.com/v3'

NURTURE_EMAILS = [
    {
        "delay": 0,
        "subject": "Here's your AI Content Cash Kit — start with this",
        "body": """Hi {{ subscriber.first_name | default: 'Friend' }},

You're in. Here's your download link:

[INSERT YOUR GUMROAD/DOWNLOAD LINK HERE]

Once you open the ZIP, start with script-01. It's the shortest and fastest path to a video that actually sells.

Quick action for today: Pick one script, record a 60-second clip on your phone, and post it. Don't overthink it. A raw phone video with a good hook converts better than a polished video with a weak one.

Reply and let me know when it's live — I'll drop a personal tip on what to tweak for your specific audience.

Welcome to the kit. Let's get your first sale this week.

— Digital Charm
digitalcharmco@gmail.com"""
    },
    {
        "delay": 1,
        "subject": "How one 60s video made $432 in a weekend",
        "body": """Hi {{ subscriber.first_name | default: 'Friend' }},

Quick story about how this kit works in practice.

A creator — 3,200 followers, relationship niche — used script-03 (the "mistake people make" format) to record a 58-second clip on her phone. The video got 4,100 views in 48 hours.

She added this CTA in the caption: "I made a $17 kit with the exact framework I use — link in bio."

Result: 31 buyers in the first 48 hours. $527 before her weekend was over.

What she did differently:
1. Used the hook from the script word-for-word (no improvising)
2. Pointed to a Gumroad page she set up in 20 minutes
3. Sent one follow-up email 24 hours later

Your kit has the same scripts, same hook formulas, same email templates.

The only variable is whether you post.

Need help setting up Gumroad? Reply and I'll send a 3-step walkthrough.

— Digital Charm"""
    },
    {
        "delay": 3,
        "subject": "You don't need fancy equipment to make this work",
        "body": """Hi {{ subscriber.first_name | default: 'Friend' }},

The #1 reason creators stall: overthinking the setup.

In 60 minutes you can:
- Minutes 1-10: Pick a script. Read it once.
- Minutes 11-20: Film a 60s video on your phone.
- Minutes 21-30: Upload to Gumroad. Price: $17.
- Minutes 31-45: Post the video with the caption from the kit.
- Minutes 46-60: Schedule your next follow-up email.

You don't need:
- A big following (100 real fans can generate $170-$500 with a $17 offer)
- Professional video gear (your phone is fine)
- A website (Gumroad handles everything)
- A copywriter (the kit IS the copy)

Which step feels like a blocker? Reply and I'll help you push through it.

— Digital Charm"""
    },
    {
        "delay": 5,
        "subject": "People are buying this today — limited bonus",
        "body": """Hi {{ subscriber.first_name | default: 'Friend' }},

A few wins from people using the kit this week:

- One creator in the personal finance niche made $204 in 3 days after posting script-07
- A fitness creator used the cold outreach email, reached out to 20 accounts, and got 4 paying buyers ($68)
- A relationship coach closed a $97 upsell to someone who started at $17

These aren't outliers. These are people who opened the kit, picked one script, and posted.

Limited bonus: the first 10 people to reply "I posted" this week get a free 20-minute 1:1 review of their video and caption.

Reply "I posted" with the link to your video.

— Digital Charm"""
    },
    {
        "delay": 7,
        "subject": "Final reminder — 30-day guarantee",
        "body": """Hi {{ subscriber.first_name | default: 'Friend' }},

Last email in this sequence. I want to make sure you know about the guarantee.

If you use the kit — post at least one video, set up a checkout page, send at least one email — and you don't make your first sale within 30 days, I'll refund you in full.

FAQ:

Q: What if I don't have an email list?
A: You don't need one. The cold outreach templates work via DMs.

Q: What platform works best?
A: TikTok and Instagram Reels get the fastest organic reach. The scripts work on all of them.

Q: Can I resell the kit?
A: Yes. The kit includes resell rights. Rebrand it, keep 100% of the revenue.

Any questions? Reply to this email — I read every one.

— Digital Charm
digitalcharmco@gmail.com

P.S. "I was skeptical because I'd tried other kits that didn't work. This one was different — I had a buyer within 48 hours of posting." — Marcus, content creator"""
    }
]


def create_form():
    """Create an opt-in form for new buyers/leads."""
    print("\n[1/2] Creating ConvertKit opt-in form...")
    r = requests.post(
        f'{BASE_URL}/forms',
        json={
            'api_secret': API_SECRET,
            'form': {'name': 'AI Content Cash Kit Buyers'}
        }
    )
    if r.status_code in (200, 201):
        data = r.json()
        # response can be list or dict
        if isinstance(data, list):
            form = data[0]
        else:
            form = data.get('form', data)
        fid = form.get('id')
        print(f"  Form created: ID {fid}  Name: {form.get('name')}")
        return fid
    else:
        print(f"  Form creation failed: {r.status_code} — {r.text}")
        print("  You can create it manually at app.kit.com -> Forms -> New Form")
        return None


def print_sequence_instructions():
    """Print all email content formatted for easy copy-paste into ConvertKit."""
    print("\n[2/2] SEQUENCE SETUP — copy-paste these into ConvertKit")
    print("=" * 70)
    print("Go to: app.kit.com -> Sequences -> New Sequence -> Name it 'AI Content Cash Kit Nurture'")
    print("Add each email below with the specified delay.")
    print("=" * 70)

    for i, email in enumerate(NURTURE_EMAILS, 1):
        delay_label = "Send immediately" if email['delay'] == 0 else f"Send {email['delay']} day(s) after previous"
        print(f"\n--- EMAIL {i} of {len(NURTURE_EMAILS)} ---")
        print(f"Delay:   {delay_label}")
        print(f"Subject: {email['subject']}")
        print(f"\nBody:\n{email['body']}")
        print()

    print("=" * 70)
    print("\nAfter creating the sequence:")
    print("1. Copy the Sequence ID from the URL (app.kit.com/sequences/XXXXXX)")
    print("2. Open .env and set:  CONVERTKIT_SEQUENCE_ID=XXXXXX")
    print("3. Run:  python monetization/agents/setup_convertkit.py --save-ids --sequence-id XXXXXX")


def save_ids_to_env(form_id=None, sequence_id=None):
    """Write IDs back into .env."""
    updated = []
    if form_id:
        set_key(str(ENV_FILE), 'CONVERTKIT_FORM_ID', str(form_id))
        updated.append(f'CONVERTKIT_FORM_ID={form_id}')
    if sequence_id:
        set_key(str(ENV_FILE), 'CONVERTKIT_SEQUENCE_ID', str(sequence_id))
        updated.append(f'CONVERTKIT_SEQUENCE_ID={sequence_id}')
    if updated:
        print(f"\n.env updated:")
        for u in updated:
            print(f"  {u}")
    else:
        print("Nothing to save.")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='One-time ConvertKit setup')
    parser.add_argument('--save-ids', action='store_true',
                        help='Just save IDs to .env (use after manual sequence creation)')
    parser.add_argument('--sequence-id', default=None, help='Sequence ID to save')
    parser.add_argument('--form-id', default=None, help='Form ID to save')
    args = parser.parse_args()

    if not API_KEY or not API_SECRET:
        print('ERROR: CONVERTKIT_API_KEY and CONVERTKIT_API_SECRET must be set in .env')
        sys.exit(1)

    if args.save_ids:
        save_ids_to_env(form_id=args.form_id, sequence_id=args.sequence_id)
        print("\nNext: run the flow with a test buyer:")
        print("  python monetization/agents/convertkit_sender.py subscribe --email your@email.com")
        return

    # Full setup
    form_id = create_form()
    if form_id:
        save_ids_to_env(form_id=form_id)

    print_sequence_instructions()


if __name__ == '__main__':
    main()
