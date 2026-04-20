#!/usr/bin/env python3
"""Google Secret Manager helper

Usage:
  # Install google auth or set GOOGLE_APPLICATION_CREDENTIALS to a service account JSON
  pip install google-cloud-secret-manager

  # Fetch single secret value and print
  python monetization\gcp_secret_manager.py --project my-gcp-project --secret SENDGRID_API_KEY --print

  # Map multiple secrets to env vars from a JSON map and write a local .env file
  python monetization\gcp_secret_manager.py --project my-gcp-project --map secret_map.json --write-dotenv .env

secret_map.json format:
  {
    "SENDGRID_API_KEY": "projects/my-gcp-project/secrets/sendgrid-api-key/versions/latest",
    "SMTP_PASS": "projects/my-gcp-project/secrets/smtp-pass/versions/latest"
  }

This script requires that the runtime has credentials with `roles/secretmanager.secretAccessor`.
Do NOT commit service account key files to source control.
"""

import os
import json
import argparse
from google.cloud import secretmanager


def get_secret(project_id, secret_id, version_id='latest'):
    """Fetch secret value from Google Secret Manager.

    secret_id can be either the simple secret name or a full resource name.
    If `secret_id` is the short name, this will build the resource path.
    """
    client = secretmanager.SecretManagerServiceClient()

    if secret_id.startswith('projects/'):
        name = secret_id
    else:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode('UTF-8')
    return payload


def load_map_and_set_env(project_id, mapping):
    """mapping: dict of ENV_VAR -> secret resource OR short secret name

    Returns dict of env_var -> value
    """
    out = {}
    for env_var, secret_ref in mapping.items():
        if secret_ref.startswith('projects/'):
            value = get_secret(project_id, secret_ref)
        else:
            # secret_ref is short name
            value = get_secret(project_id, secret_ref)
        os.environ[env_var] = value
        out[env_var] = value
    return out


def write_dotenv(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        for k, v in data.items():
            # simple escaping
            safe = v.replace('\n', '\\n')
            f.write(f"{k}={safe}\n")


def main():
    parser = argparse.ArgumentParser(description='GCP Secret Manager helper')
    parser.add_argument('--project', required=True)
    parser.add_argument('--secret', help='Single secret name or full resource')
    parser.add_argument('--version', default='latest')
    parser.add_argument('--print', action='store_true', dest='do_print')
    parser.add_argument('--map', help='Path to JSON mapping file: {ENV_VAR: secret_ref}')
    parser.add_argument('--write-dotenv', help='Write fetched secrets into a .env file')
    args = parser.parse_args()

    if args.secret:
        val = get_secret(args.project, args.secret, args.version)
        if args.do_print:
            print(val)
        else:
            print('Fetched secret length:', len(val))
        return

    if args.map:
        with open(args.map, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        data = load_map_and_set_env(args.project, mapping)
        if args.write_dotenv:
            write_dotenv(args.write_dotenv, data)
            print('Wrote dotenv:', args.write_dotenv)
        else:
            print('Loaded secrets for env vars:', list(data.keys()))
        return

    parser.print_help()


if __name__ == '__main__':
    main()
