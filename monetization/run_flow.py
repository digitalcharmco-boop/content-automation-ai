#!/usr/bin/env python3
"""Full monetization flow: build → preview emails → simulate purchase → deliver → dashboard.

Usage:
  # Dry-run (no emails sent, simulated purchase only)
  python monetization/run_flow.py

  # Live mode (sends real emails via SMTP or SendGrid)
  python monetization/run_flow.py --live --to buyer@example.com --provider smtp

  # Simulate N purchases then deliver
  python monetization/run_flow.py --simulate 3

Run from the project root directory.
"""

import subprocess
import sys
import os
import json
import argparse
from pathlib import Path

BASE = Path(__file__).parent
PROJECT_ROOT = BASE.parent


def run_cmd(args, **kwargs):
    result = subprocess.run([sys.executable] + args, **kwargs)
    result.check_returncode()
    return result


def load_orders():
    orders_file = BASE / 'orders.json'
    orders = []
    if orders_file.exists():
        with open(orders_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        orders.append(json.loads(line))
                    except Exception:
                        pass
    return orders


def main():
    parser = argparse.ArgumentParser(description='Run the full monetization flow')
    parser.add_argument('--live', action='store_true', help='Send real emails (default: dry-run)')
    parser.add_argument('--to', default=None, help='Recipient email for live sends')
    parser.add_argument('--provider', choices=['smtp', 'sendgrid'], default='smtp')
    parser.add_argument('--simulate', type=int, default=1, metavar='N',
                        help='Number of purchases to simulate (default: 1)')
    parser.add_argument('--skip-build', action='store_true', help='Skip rebuilding the payload ZIP')
    parser.add_argument('--skip-deliver', action='store_true', help='Skip delivery step')
    args = parser.parse_args()

    print('=' * 60)
    print('  MONETIZATION FLOW')
    print('=' * 60)

    # Step 1: Build payload ZIP
    if not args.skip_build:
        print('\n[1/5] Building payload ZIP...')
        run_cmd([str(BASE / 'build_payload.py')])
    else:
        print('\n[1/5] Skipping payload build (--skip-build)')

    # Step 2: Preview / send nurture emails
    template = str(BASE / 'emails' / 'nurture_emails.md')
    if args.live:
        print(f'\n[2/5] Sending nurture emails to {args.to} via {args.provider}...')
        cmd = [str(BASE / 'agents' / 'send_sequence.py'),
               '--template', template,
               '--provider', args.provider]
        if args.to:
            cmd += ['--to', args.to]
        run_cmd(cmd)
    else:
        print('\n[2/5] Previewing nurture emails (dry-run)...')
        result = subprocess.run(
            [sys.executable, str(BASE / 'agents' / 'send_sequence.py'),
             '--template', template, '--dry-run'],
            capture_output=True, text=True
        )
        print(result.stdout[:2000])

    # Step 3: Simulate purchases
    print(f'\n[3/5] Simulating {args.simulate} purchase(s)...')
    for i in range(args.simulate):
        email = args.to or f'testbuyer{i+1}@example.com'
        result = subprocess.run(
            [sys.executable, str(BASE / 'checkout_simulator.py'),
             '--email', email, '--price', '17.0'],
            capture_output=True, text=True
        )
        print(result.stdout.strip())

    # Step 4: Deliver payload to all unfulfilled orders
    if not args.skip_deliver:
        print('\n[4/5] Delivering payload to new orders...')
        run_cmd([str(BASE / 'deliver_payload.py')])
    else:
        print('\n[4/5] Skipping delivery (--skip-deliver)')

    # Step 5: Dashboard summary
    print('\n[5/5] Dashboard summary...')
    run_cmd([str(BASE / 'dashboard.py')])

    # Final guidance
    orders = load_orders()
    print('\n' + '=' * 60)
    print('  NEXT STEPS TO GO LIVE AND MAKE REAL MONEY')
    print('=' * 60)
    print("""
1. REBRAND your sales page and emails:
   python monetization/rebrand.py --interactive
   (Or: python monetization/rebrand.py --config monetization/branding_config.json)

2. HOST your sales page:
   Upload monetization/sales_page.html to a free host:
   - Carrd.co (drag-and-drop, free)
   - Netlify Drop (drop the HTML file, instant URL)
   - Or paste the HTML into your Gumroad product description

3. CREATE your checkout:
   - Go to gumroad.com -> New Product -> Digital
   - Set price: $17
   - Upload: monetization_payload.zip (built in step 1)
   - Set success message to send buyer to download + first email
   - Copy your Gumroad URL -> paste into branding_config.json as checkout_url

4. SEND cold outreach:
   Edit monetization/outreach_list_50.csv with real leads
   python monetization/agents/send_sequence.py \
       --template monetization/emails/cold_outreach.md \
       --provider smtp --to lead@example.com

5. SET UP real email (SMTP or SendGrid):
   set SMTP_HOST=smtp.gmail.com
   set SMTP_PORT=587
   set SMTP_USER=you@gmail.com
   set SMTP_PASS=your-app-password
   set SENDER_EMAIL=you@gmail.com

   Then rerun with --live:
   python monetization/run_flow.py --live --to firstlead@example.com
""")


if __name__ == '__main__':
    main()
