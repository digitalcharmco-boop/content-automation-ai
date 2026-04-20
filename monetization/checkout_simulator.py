#!/usr/bin/env python3
"""Simulate a checkout and record orders to `monetization/orders.json`.

This is a local-only simulator for testing the revenue flow. It does not
process payments or communicate with external gateways.
"""

import os
import json
import uuid
import datetime

ORDERS_FILE = os.path.join(os.path.dirname(__file__), 'orders.json')


def simulate_purchase(buyer_email='buyer@example.com', product='AI Content Cash Kit', price=17.0):
    os.makedirs(os.path.dirname(ORDERS_FILE), exist_ok=True)
    order = {
        'id': str(uuid.uuid4()),
        'email': buyer_email,
        'product': product,
        'price': float(price),
        'time': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    with open(ORDERS_FILE, 'a', encoding='utf-8') as f:
        f.write(json.dumps(order) + '\n')
    print('Simulated purchase:', json.dumps(order))
    return order


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--email', default='buyer@example.com')
    parser.add_argument('--price', type=float, default=17.0)
    args = parser.parse_args()
    simulate_purchase(args.email, price=args.price)
