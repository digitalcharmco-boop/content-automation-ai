#!/usr/bin/env python3
"""Dry-run utility: prints rendered emails without sending."""

import argparse
from send_sequence import load_templates, split_templates
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True)
    args = parser.parse_args()

    raw = load_templates(args.template)
    templates = split_templates(raw)

    for i, t in enumerate(templates, start=1):
        subj = t['subject']
        body = t['body'].replace('{{first_name}}', os.getenv('DRY_NAME', 'Friend'))
        print(f"\n=== Email {i}: {subj} ===\n{body}\n")


if __name__ == '__main__':
    main()
