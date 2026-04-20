#!/usr/bin/env python3
"""
ConvertKit (Kit) email integration.

Two modes:
  1. subscribe_to_sequence  — add a buyer/lead to your nurture sequence automatically
  2. broadcast              — send a one-time email to a subscriber or all subscribers

Usage examples:

  # Subscribe a new buyer to your nurture sequence (run after every purchase)
  python monetization/agents/convertkit_sender.py subscribe \
      --email buyer@example.com --first-name Jane

  # Send a broadcast to all active subscribers
  python monetization/agents/convertkit_sender.py broadcast \
      --subject "Your kit is here" --body-file monetization/emails/nurture_emails.md

  # Test connection (prints your ConvertKit account info)
  python monetization/agents/convertkit_sender.py test

Requires in .env:
  CONVERTKIT_API_KEY       — your public API key
  CONVERTKIT_API_SECRET    — your API secret (for some endpoints)
  CONVERTKIT_SEQUENCE_ID   — ID of your nurture sequence (get from ConvertKit dashboard URL)
  CONVERTKIT_FORM_ID       — ID of an opt-in form (used to subscribe buyers; optional)
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
ROOT = Path(__file__).parent.parent.parent
load_dotenv(ROOT / '.env')

API_KEY = os.getenv('CONVERTKIT_API_KEY', '')
API_SECRET = os.getenv('CONVERTKIT_API_SECRET', '')
SEQUENCE_ID = os.getenv('CONVERTKIT_SEQUENCE_ID', '')
FORM_ID = os.getenv('CONVERTKIT_FORM_ID', '')
BASE_URL = 'https://api.convertkit.com/v3'


def _check_config():
    if not API_KEY:
        print('ERROR: CONVERTKIT_API_KEY not set in .env')
        sys.exit(1)


def test_connection():
    """Verify API credentials work and print account info."""
    _check_config()
    # /account requires api_secret; fall back to api_key if secret not set
    params = {'api_secret': API_SECRET} if API_SECRET else {'api_key': API_KEY}
    r = requests.get(f'{BASE_URL}/account', params=params)
    if r.status_code == 200:
        data = r.json()
        print('ConvertKit connection OK')
        print(f"  Account: {data.get('name', 'unknown')}")
        print(f"  Primary email: {data.get('primary_email_address', 'unknown')}")
        return True
    else:
        print(f'Connection failed: {r.status_code} — {r.text}')
        return False


def list_sequences():
    """Print all sequences in the account."""
    _check_config()
    r = requests.get(f'{BASE_URL}/sequences', params={'api_secret': API_SECRET})
    r.raise_for_status()
    seqs = r.json().get('courses', [])
    if not seqs:
        print('No sequences found. Create one at app.kit.com.')
        return []
    print(f'\nSequences ({len(seqs)}):')
    for s in seqs:
        print(f"  ID: {s['id']}  Name: {s['name']}")
    return seqs


def list_forms():
    """Print all forms in the account."""
    _check_config()
    r = requests.get(f'{BASE_URL}/forms', params={'api_key': API_KEY})
    r.raise_for_status()
    forms = r.json().get('forms', [])
    if not forms:
        print('No forms found.')
        return []
    print(f'\nForms ({len(forms)}):')
    for f in forms:
        print(f"  ID: {f['id']}  Name: {f['name']}")
    return forms


def subscribe_to_sequence(email, first_name='', sequence_id=None, tags=None):
    """
    Subscribe an email address to a ConvertKit sequence.
    This is the main post-purchase hook — call this whenever someone buys.
    """
    _check_config()
    seq_id = sequence_id or SEQUENCE_ID
    if not seq_id:
        print('ERROR: CONVERTKIT_SEQUENCE_ID not set. Run list-sequences to find your ID.')
        sys.exit(1)

    payload = {
        'api_key': API_KEY,
        'email': email,
        'first_name': first_name or email.split('@')[0],
    }
    if tags:
        payload['tags'] = tags

    url = f'{BASE_URL}/sequences/{seq_id}/subscribe'
    r = requests.post(url, json=payload)

    if r.status_code in (200, 201):
        sub = r.json().get('subscription', {})
        print(f"Subscribed {email} to sequence {seq_id}")
        print(f"  Subscriber ID: {sub.get('subscriber', {}).get('id')}")
        print(f"  State: {sub.get('subscriber', {}).get('state')}")
        return sub
    else:
        print(f'Subscribe failed: {r.status_code} — {r.text}')
        return None


def subscribe_via_form(email, first_name='', form_id=None):
    """
    Alternative: subscribe via a form (public, no API secret needed).
    Use this if you want to trigger form-based automations in ConvertKit.
    """
    _check_config()
    fid = form_id or FORM_ID
    if not fid:
        print('ERROR: CONVERTKIT_FORM_ID not set. Run list-forms to find your ID.')
        sys.exit(1)

    payload = {
        'api_key': API_KEY,
        'email': email,
        'first_name': first_name or email.split('@')[0],
    }
    url = f'{BASE_URL}/forms/{fid}/subscribe'
    r = requests.post(url, json=payload)

    if r.status_code in (200, 201):
        print(f'Subscribed {email} via form {fid}')
        return r.json()
    else:
        print(f'Form subscribe failed: {r.status_code} — {r.text}')
        return None


def send_broadcast(subject, body, description='Broadcast'):
    """
    Create and send a broadcast to all active subscribers.
    Note: broadcasts go through ConvertKit's review queue for new accounts.
    """
    _check_config()
    if not API_SECRET:
        print('ERROR: CONVERTKIT_API_SECRET not set — required for broadcasts.')
        sys.exit(1)

    # Create broadcast
    payload = {
        'api_secret': API_SECRET,
        'subject': subject,
        'content': body,
        'description': description,
        'public': False,
    }
    r = requests.post(f'{BASE_URL}/broadcasts', json=payload)

    if r.status_code in (200, 201):
        broadcast = r.json().get('broadcast', {})
        bid = broadcast.get('id')
        print(f'Broadcast created: ID {bid}  Subject: {subject}')

        # Send it
        send_r = requests.post(
            f'{BASE_URL}/broadcasts/{bid}/send',
            json={'api_secret': API_SECRET}
        )
        if send_r.status_code in (200, 201):
            print(f'Broadcast {bid} queued for sending.')
        else:
            print(f'Send failed: {send_r.status_code} — {send_r.text}')
        return broadcast
    else:
        print(f'Broadcast creation failed: {r.status_code} — {r.text}')
        return None


def tag_subscriber(email, tag_name):
    """Create a tag and apply it to a subscriber."""
    _check_config()
    if not API_SECRET:
        print('ERROR: CONVERTKIT_API_SECRET not set.')
        sys.exit(1)

    # Create or find tag
    r = requests.get(f'{BASE_URL}/tags', params={'api_key': API_KEY})
    r.raise_for_status()
    tags = r.json().get('tags', [])
    tag = next((t for t in tags if t['name'].lower() == tag_name.lower()), None)

    if not tag:
        cr = requests.post(f'{BASE_URL}/tags', json={'api_secret': API_SECRET, 'tag': {'name': tag_name}})
        cr.raise_for_status()
        tag = cr.json()[0] if isinstance(cr.json(), list) else cr.json().get('tag', {})

    tag_id = tag.get('id')
    tr = requests.post(
        f'{BASE_URL}/tags/{tag_id}/subscribe',
        json={'api_key': API_KEY, 'email': email}
    )
    if tr.status_code in (200, 201):
        print(f'Tagged {email} with "{tag_name}"')
    else:
        print(f'Tagging failed: {tr.status_code} — {tr.text}')


def main():
    parser = argparse.ArgumentParser(description='ConvertKit email integration')
    sub = parser.add_subparsers(dest='command')

    # test
    sub.add_parser('test', help='Test API connection')

    # list-sequences
    sub.add_parser('list-sequences', help='List all sequences')

    # list-forms
    sub.add_parser('list-forms', help='List all forms')

    # subscribe
    p_sub = sub.add_parser('subscribe', help='Subscribe a buyer to the nurture sequence')
    p_sub.add_argument('--email', required=True)
    p_sub.add_argument('--first-name', default='')
    p_sub.add_argument('--sequence-id', default=None)
    p_sub.add_argument('--tag', default='buyer', help='Tag to apply (default: buyer)')

    # subscribe-form
    p_form = sub.add_parser('subscribe-form', help='Subscribe via a ConvertKit form')
    p_form.add_argument('--email', required=True)
    p_form.add_argument('--first-name', default='')
    p_form.add_argument('--form-id', default=None)

    # broadcast
    p_bc = sub.add_parser('broadcast', help='Send a broadcast to all subscribers')
    p_bc.add_argument('--subject', required=True)
    p_bc.add_argument('--body', default=None, help='Email body text')
    p_bc.add_argument('--body-file', default=None, help='Path to .md or .txt file with body')

    args = parser.parse_args()

    if args.command == 'test':
        test_connection()

    elif args.command == 'list-sequences':
        list_sequences()

    elif args.command == 'list-forms':
        list_forms()

    elif args.command == 'subscribe':
        subscribe_to_sequence(
            email=args.email,
            first_name=args.first_name,
            sequence_id=args.sequence_id,
        )
        if args.tag:
            tag_subscriber(args.email, args.tag)

    elif args.command == 'subscribe-form':
        subscribe_via_form(
            email=args.email,
            first_name=args.first_name,
            form_id=args.form_id,
        )

    elif args.command == 'broadcast':
        body = args.body or ''
        if args.body_file:
            with open(args.body_file, 'r', encoding='utf-8') as f:
                body = f.read()
        if not body:
            print('ERROR: provide --body or --body-file')
            sys.exit(1)
        send_broadcast(subject=args.subject, body=body)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
