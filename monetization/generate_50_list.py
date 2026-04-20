#!/usr/bin/env python3
"""Generate a 50-row outreach CSV from the template for dry-run previews."""

import csv
import os

SRC = os.path.join(os.path.dirname(__file__), 'outreach_list_template.csv')
DEST = os.path.join(os.path.dirname(__file__), 'outreach_list_50.csv')


def generate(n=50):
    rows = []
    with open(SRC, newline='', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))
        if not reader:
            raise SystemExit('Template CSV is empty')

    i = 0
    while len(rows) < n:
        template = reader[i % len(reader)]
        # make small personalization differences
        idx = len(rows) + 1
        new = dict(template)
        new['first_name'] = f"{template.get('first_name', 'Friend')}{idx}"
        # make recent_post slightly vary
        new['recent_post'] = f"{template.get('recent_post','Recent post')} (idea {idx})"
        rows.append(new)
        i += 1

    # write dest
    with open(DEST, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['first_name','email','platform','recent_post'])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f'Wrote {len(rows)} rows to {DEST}')


if __name__ == '__main__':
    generate(50)
