#!/usr/bin/env python3
"""Simple dashboard that summarizes simulated orders and sent logs."""

import json
import os
from pathlib import Path

BASE = Path(__file__).parent
ORDERS_FILE = BASE / 'orders.json'
SENT_LOG = BASE / 'sent_log.json'


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


def load_json(path):
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def main():
    orders = load_json_lines(ORDERS_FILE)
    sent = load_json(SENT_LOG)

    total_orders = len(orders)
    total_revenue = sum(o.get('price', 0) for o in orders)

    delivered = [s for s in sent if s.get('status') == 'delivered_simulated']

    print('--- Monetization Dashboard (Local Simulation) ---')
    print(f'Total simulated orders: {total_orders}')
    print(f'Total simulated revenue: ${total_revenue:.2f}')
    print(f'Total simulated deliveries: {len(delivered)}')
    print('\nRecent orders:')
    for o in orders[-5:]:
        print(f"- {o.get('email')} | {o.get('product')} | ${o.get('price')} | {o.get('time')}")

    print('\nRecent sends:')
    for s in sent[-5:]:
        print(f"- {s.get('to')} | {s.get('subject')} | {s.get('time')} | {s.get('status')}")


if __name__ == '__main__':
    main()
