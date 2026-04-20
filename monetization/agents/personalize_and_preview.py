#!/usr/bin/env python3
"""Personalize cold outreach templates using a CSV and print a preview or write to JSON.

Usage:
  python monetize_agents\personalize_and_preview.py --csv monetization/outreach_list_template.csv --template monetization/emails/cold_outreach_personalized.md --out previews.json

This script is intentionally safe: it only prints/writes previews and does not send emails.
"""

import csv
import json
import os
import argparse
import re


def load_template(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def split_templates(raw):
    parts = re.split(r"\n--\s+", raw)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        lines = p.splitlines()
        subj = lines[0].replace('-', '').strip()
        body = '\n'.join(lines[1:]).strip()
        m = re.search(r"Subject:\s*(.*)", body)
        subject = m.group(1).strip() if m else subj
        body = re.sub(r"Subject:.*\n", '', body, count=1).strip()
        out.append({'subject': subject, 'body': body})
    return out


def personalize(text, row):
    for k, v in row.items():
        text = text.replace('{{' + k + '}}', v)
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', required=True)
    parser.add_argument('--template', required=True)
    parser.add_argument('--out', required=False)
    args = parser.parse_args()

    raw_template = load_template(args.template)
    templates = split_templates(raw_template)

    previews = []
    with open(args.csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Normalize keys to match placeholders
            normalized = {k: v for k, v in row.items()}
            for t in templates:
                subj = personalize(t['subject'], normalized)
                body = personalize(t['body'], normalized)
                previews.append({'to': row.get('email'), 'subject': subj, 'body': body})

    # Print first 5 previews to stdout
    for i, p in enumerate(previews[:10], start=1):
        print('\n---')
        print(f"Preview {i} -> To: {p['to']} | Subject: {p['subject']}")
        print(p['body'])
        print('---')

    if args.out:
        with open(args.out, 'w', encoding='utf-8') as f:
            json.dump(previews, f, indent=2)
        print('\nWrote previews to', args.out)


if __name__ == '__main__':
    main()
