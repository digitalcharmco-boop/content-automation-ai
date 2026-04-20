#!/usr/bin/env python3
"""
YouTube OAuth test — validates the full auth flow before building anything on top.
Uses a local Flask callback server on 127.0.0.1 (never localhost, never input()).

Usage:
  1. Add to .env:  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET
  2. In Google Cloud Console, add authorized redirect URI: http://127.0.0.1:8766/callback
  3. Run: python auth_test_youtube.py
  4. Browser opens -> authorize -> token printed -> one API call verified
"""

import os
import json
import secrets
import threading
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

import requests
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

CLIENT_ID     = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
REDIRECT_URI  = "http://127.0.0.1:8766/callback"
SCOPES        = " ".join([
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
])
TOKEN_FILE    = Path(__file__).parent / "config" / "youtube_tokens.json"

_token_result = {}
_shutdown     = threading.Event()

app = Flask(__name__)


@app.route("/callback")
def callback():
    code  = request.args.get("code")
    error = request.args.get("error")

    if error:
        _token_result["error"] = error
        _shutdown.set()
        return f"<h2>Auth failed: {error}</h2>", 400

    if not code:
        _token_result["error"] = "no code received"
        _shutdown.set()
        return "<h2>No code received.</h2>", 400

    resp = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code":          code,
            "client_id":     CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "redirect_uri":  REDIRECT_URI,
            "grant_type":    "authorization_code",
        },
        timeout=15,
    )
    data = resp.json()

    if "access_token" not in data:
        _token_result["error"] = data
        _shutdown.set()
        return f"<h2>Token exchange failed</h2><pre>{json.dumps(data, indent=2)}</pre>", 400

    _token_result["tokens"] = data
    _shutdown.set()
    return "<h2>Authorization successful!</h2><p>You can close this tab.</p>"


def _run_server():
    import logging
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app.run(host="127.0.0.1", port=8766, debug=False, use_reloader=False)


def verify_api_call(access_token: str) -> bool:
    resp = requests.get(
        "https://www.googleapis.com/youtube/v3/channels",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"part": "snippet", "mine": "true"},
        timeout=15,
    )
    data = resp.json()
    if resp.status_code == 200 and data.get("items"):
        channel = data["items"][0]["snippet"]
        print(f"  Verified API call — channel: {channel.get('title', '(unknown)')}")
        return True
    print(f"  API call failed: {data}")
    return False


def save_tokens(data: dict):
    TOKEN_FILE.parent.mkdir(exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  Tokens saved to {TOKEN_FILE}")


def main():
    if not CLIENT_ID or not CLIENT_SECRET:
        raise SystemExit("ERROR: Set YOUTUBE_CLIENT_ID and YOUTUBE_CLIENT_SECRET in .env")

    state  = secrets.token_hex(16)
    params = {
        "client_id":     CLIENT_ID,
        "redirect_uri":  REDIRECT_URI,
        "response_type": "code",
        "scope":         SCOPES,
        "access_type":   "offline",
        "prompt":        "consent",
        "state":         state,
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)

    server_thread = threading.Thread(target=_run_server, daemon=True)
    server_thread.start()

    print("\nYouTube OAuth Test")
    print(f"  Redirect URI : {REDIRECT_URI}")
    print(f"  Opening browser...\n")
    webbrowser.open(auth_url)

    _shutdown.wait(timeout=120)

    if "error" in _token_result:
        raise SystemExit(f"Auth failed: {_token_result['error']}")

    if "tokens" not in _token_result:
        raise SystemExit("Timed out waiting for callback.")

    tokens = _token_result["tokens"]
    access_token  = tokens["access_token"]
    refresh_token = tokens.get("refresh_token", "")
    print(f"  Access token  : {access_token[:12]}...")
    print(f"  Refresh token : {refresh_token[:12]}..." if refresh_token else "  Refresh token : (none — re-auth needed)")
    print(f"  Expires in    : {tokens.get('expires_in')} seconds")

    print("\nVerifying API call...")
    ok = verify_api_call(access_token)

    if ok:
        save_tokens(tokens)
        print("\nYouTube auth test PASSED. Safe to build on top of this flow.")
    else:
        raise SystemExit("API verification failed — do not build on top of this token.")


if __name__ == "__main__":
    main()
