#!/usr/bin/env python3
"""Simple email sequence sender supporting SMTP or SendGrid (HTTP).

Usage examples (Powershell):
set SMTP_HOST=smtp.example.com
set SMTP_PORT=587
set SMTP_USER=you@example.com
set SMTP_PASS=yourpass

python monetization\agents\send_sequence.py --template monetization/emails/nurture_emails.md --dry-run

Or auto-load from GCP Secret Manager (requires monetization/secret_map.json and GOOGLE_APPLICATION_CREDENTIALS):
python monetization\agents\send_sequence.py --template monetization/emails/nurture_emails.md --dry-run --load-secrets
"""

import os
import sys
import argparse
import smtplib
from email.message import EmailMessage
import re
import json
import requests
import logging

try:
    from google.cloud import secretmanager
except Exception:
    secretmanager = None

logging.basicConfig(level=logging.INFO)


def _load_secrets_from_gcp(secret_map_path="monetization/secret_map.json"):
    """
    Load secrets from Google Secret Manager using a local secret_map.json file
    that maps ENV_VAR -> secret_id. Example:
    {
      "project": "my-gcp-project",
      "SENDGRID_API_KEY": "sendgrid-api-key",
      "SMTP_PASS": "smtp-pass",
      "SENDER_EMAIL": "sender-email"
    }
    """
    if secretmanager is None:
        logging.debug("google-cloud-secret-manager not available; skipping GCP Secret Manager load.")
        return

    if not os.path.exists(secret_map_path):
        logging.debug("No secret_map.json found at %s", secret_map_path)
        return

    try:
        with open(secret_map_path, "r", encoding="utf-8") as f:
            mapping = json.load(f)
    except Exception as e:
        logging.warning("Failed to read secret_map.json: %s", e)
        return

    # project id resolution: secret_map 'project' -> env GOOGLE_CLOUD_PROJECT / GCP_PROJECT
    project = mapping.get("project") or os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project or project == "YOUR_GCP_PROJECT_ID":
        logging.warning("GCP project not configured in secret_map.json or env; skipping secret load.")
        return

    client = secretmanager.SecretManagerServiceClient()
    for env_var, secret_id in mapping.items():
        if env_var == "project":
            continue
        # skip if env var already set
        if os.environ.get(env_var):
            continue
        name = f"projects/{project}/secrets/{secret_id}/versions/latest"
        try:
            response = client.access_secret_version(request={"name": name})
            payload = response.payload.data.decode("UTF-8")
            os.environ[env_var] = payload
            logging.info("Loaded secret for %s from GCP Secret Manager.", env_var)
        except Exception as e:
            logging.warning("Could not load secret %s (%s): %s", secret_id, env_var, e)


def _write_env_file(env_dict, output_path=".env.local"):
    """Write environment variables to a .env file for local testing."""
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            for key, val in env_dict.items():
                # simple escaping for bash/PowerShell
                val_escaped = val.replace('"', '\\"')
                f.write(f'{key}={val_escaped}\n')
        logging.info(f"Wrote environment to {output_path}")
    except Exception as e:
        logging.warning(f"Failed to write {output_path}: {e}")


def load_templates(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def split_templates(raw):
    # Split on lines that start with -- Email or -- Cold
    parts = re.split(r"\n--\s+", raw)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        lines = p.splitlines()
        subj = lines[0].replace('-', '').strip()
        body = '\n'.join(lines[1:]).strip()
        # find subject line in body if present
        m = re.search(r"Subject:\s*(.*)", body)
        subject = m.group(1).strip() if m else subj
        # remove subject line from body
        body = re.sub(r"Subject:.*\n", '', body, count=1).strip()
        out.append({'subject': subject, 'body': body})
    return out


def send_smtp(from_addr, to_addr, subject, body, smtp_config):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg.set_content(body)

    with smtplib.SMTP(smtp_config['host'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['user'], smtp_config['pass'])
        server.send_message(msg)


def send_sendgrid(from_addr, to_addr, subject, body, api_key):
    url = 'https://api.sendgrid.com/v3/mail/send'
    payload = {
        'personalizations': [{'to': [{'email': to_addr}]}],
        'from': {'email': from_addr},
        'subject': subject,
        'content': [{'type': 'text/plain', 'value': body}]
    }
    headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--template', required=True)
    parser.add_argument('--to', required=False, help='recipient email')
    parser.add_argument('--from', dest='from_addr', required=False, help='from address')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--provider', choices=['smtp', 'sendgrid'], default='smtp')
    parser.add_argument('--load-secrets', action='store_true', help='load secrets from GCP Secret Manager (requires secret_map.json)')
    parser.add_argument('--write-env', action='store_true', help='write loaded secrets to .env.local for local testing')
    args = parser.parse_args()

    # Load secrets if requested
    if args.load_secrets:
        _load_secrets_from_gcp()

    raw = load_templates(args.template)
    templates = split_templates(raw)

    to_addr = args.to or os.getenv('TEST_RECIPIENT') or 'recipient@example.com'
    from_addr = args.from_addr or os.getenv('SENDER_EMAIL') or 'you@example.com'

    if args.provider == 'smtp':
        smtp_config = {
            'host': os.getenv('SMTP_HOST', 'localhost'),
            'port': int(os.getenv('SMTP_PORT', 25)),
            'user': os.getenv('SMTP_USER', ''),
            'pass': os.getenv('SMTP_PASS', '')
        }
    else:
        smtp_config = None

    for i, t in enumerate(templates, start=1):
        sub = t['subject']
        body = t['body']
        # simple template replacement example
        body = body.replace('{{first_name}}', 'Friend')

        print(f"\n---\nEmail {i}: {sub}\nTo: {to_addr}\nFrom: {from_addr}\n\n{body[:400]}\n---\n")

        if args.dry_run:
            continue

        try:
            if args.provider == 'smtp':
                send_smtp(from_addr, to_addr, sub, body, smtp_config)
            else:
                api_key = os.getenv('SENDGRID_API_KEY')
                if not api_key:
                    raise ValueError('SENDGRID_API_KEY not set')
                send_sendgrid(from_addr, to_addr, sub, body, api_key)
            print(f"Sent email {i} to {to_addr}")
        except Exception as e:
            print(f"Failed to send email {i}: {e}")


if __name__ == '__main__':
    main()
