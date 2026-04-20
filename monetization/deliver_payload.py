#!/usr/bin/env python3
"""Process simulated orders and deliver the monetization payload ZIP to a local deliveries folder.

This is a local-only delivery simulator. It records deliveries to `deliveries.json`
and appends entries to `sent_log.json` as simulated send records.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from dotenv import load_dotenv

BASE = Path(__file__).parent
load_dotenv(BASE.parent / '.env')
ORDERS_FILE = BASE / 'orders.json'
DELIVERIES_FILE = BASE / 'deliveries.json'
PAYLOAD = BASE.parent / 'monetization_payload.zip'
SENT_LOG = BASE / 'sent_log.json'
DELIVERIES_DIR = BASE / 'delivered_files'


def load_json_lines(path):
    items = []
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    items.append(json.loads(line))
                except Exception:
                    continue
    return items


def append_json(path, obj):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj) + '\n')


def main():
    os.makedirs(DELIVERIES_DIR, exist_ok=True)
    delivered = []
    if DELIVERIES_FILE.exists():
        with open(DELIVERIES_FILE, 'r', encoding='utf-8') as f:
            try:
                delivered = json.load(f)
            except Exception:
                delivered = []

    orders = load_json_lines(ORDERS_FILE)
    sent_log = []
    if SENT_LOG.exists():
        try:
            with open(SENT_LOG, 'r', encoding='utf-8') as f:
                sent_log = json.load(f)
        except Exception:
            sent_log = []

    ck_api_key = os.getenv('CONVERTKIT_API_KEY', '')
    ck_sequence_id = os.getenv('CONVERTKIT_SEQUENCE_ID', '')

    new_deliveries = []
    for o in orders:
        if any(d.get('order_id') == o['id'] for d in delivered):
            continue

        # Create a copy of the payload for this order
        dest = DELIVERIES_DIR / f"payload_{o['id']}.zip"
        if PAYLOAD.exists():
            shutil.copyfile(PAYLOAD, dest)

            # Auto-subscribe buyer to ConvertKit nurture sequence
            if ck_api_key and ck_sequence_id:
                try:
                    import requests as _req
                    _req.post(
                        f'https://api.convertkit.com/v3/sequences/{ck_sequence_id}/subscribe',
                        json={
                            'api_key': ck_api_key,
                            'email': o['email'],
                            'first_name': o['email'].split('@')[0],
                        },
                        timeout=10
                    )
                    print(f"  Subscribed {o['email']} to ConvertKit sequence {ck_sequence_id}")
                except Exception as e:
                    print(f"  ConvertKit subscribe warning: {e}")
            else:
                print(f"  (Set CONVERTKIT_SEQUENCE_ID in .env to auto-enroll buyers in nurture sequence)")

            import datetime as _dt
            delivery_record = {
                'order_id': o['id'],
                'email': o['email'],
                'product': o['product'],
                'price': o['price'],
                'delivered_at': _dt.datetime.now(_dt.timezone.utc).isoformat(),
                'file': str(dest)
            }
            delivered.append(delivery_record)
            new_deliveries.append(delivery_record)

            # Simulate send log
            send_entry = {
                'to': o['email'],
                'subject': f"Your purchase: {o['product']}",
                'time': delivery_record['delivered_at'],
                'order_id': o['id'],
                'status': 'delivered_simulated'
            }
            sent_log.append(send_entry)

    # Write deliveries file
    with open(DELIVERIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(delivered, f, indent=2)

    # Write sent log
    with open(SENT_LOG, 'w', encoding='utf-8') as f:
        json.dump(sent_log, f, indent=2)

    print(f"Processed {len(new_deliveries)} new deliveries")
    for d in new_deliveries:
        print(f"Delivered {d['file']} to {d['email']}")


if __name__ == '__main__':
    main()
