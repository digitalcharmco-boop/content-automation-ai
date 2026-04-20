#!/usr/bin/env python3
"""
ContentFlow AI — Stripe Checkout Server
Serves the checkout page and handles PaymentIntent creation + webhook delivery.

Run:  python monetization/checkout_server.py
Open: http://localhost:4242/checkout?tier=pro
"""

import os
import sys
import json
import stripe
from pathlib import Path
from flask import Flask, request, jsonify, send_file, redirect
from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).parent.parent / ".env")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")

TIERS = {
    "starter": {"name": "ContentFlow AI — Starter", "amount": 2700,  "currency": "usd"},
    "pro":     {"name": "ContentFlow AI — Pro",     "amount": 9700,  "currency": "usd"},
    "agency":  {"name": "ContentFlow AI — Agency",  "amount": 19700, "currency": "usd"},
}

app = Flask(__name__, static_folder=str(Path(__file__).parent))

from monetization.stripe_extensions import bp as stripe_ext_bp
app.register_blueprint(stripe_ext_bp)


# ── PAGES ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_file(Path(__file__).parent / "sales_page.html")


@app.route("/checkout")
def checkout():
    return send_file(Path(__file__).parent / "checkout.html")


@app.route("/success")
def success():
    tier = request.args.get("tier", "pro")
    return f"""<!doctype html><html><head><meta charset=utf-8>
    <title>Payment Successful — ContentFlow AI</title>
    <style>body{{font-family:system-ui,sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;margin:0;background:#0a0a0a;color:#fff}}
    .box{{text-align:center;padding:48px 32px;max-width:480px}}
    h1{{font-size:32px;margin-bottom:12px;color:#4caf50}}
    p{{color:#aaa;line-height:1.6;margin-bottom:24px}}
    a{{background:#e05a00;color:#fff;padding:14px 32px;border-radius:6px;text-decoration:none;font-weight:700}}</style>
    </head><body><div class="box">
    <h1>&#10003; Payment confirmed!</h1>
    <p>Your ContentFlow AI <strong>{tier.title()}</strong> access is on the way.<br>
    Check your inbox — download link arrives within 60 seconds.</p>
    <a href="/">Back to home</a>
    </div></body></html>"""


# ── API ─────────────────────────────────────────────────────────────────────

@app.route("/api/config")
def get_config():
    """Return publishable key to the frontend."""
    return jsonify({"publishableKey": PUBLISHABLE_KEY})


@app.route("/api/create-payment-intent", methods=["POST"])
def create_payment_intent():
    data = request.get_json(silent=True) or {}
    tier_key = data.get("tier", "pro").lower()
    tier = TIERS.get(tier_key)

    if not tier:
        return jsonify({"error": f"Unknown tier: {tier_key}"}), 400

    if not stripe.api_key:
        return jsonify({"error": "Stripe not configured — add STRIPE_SECRET_KEY to .env"}), 500

    try:
        intent = stripe.PaymentIntent.create(
            amount=tier["amount"],
            currency=tier["currency"],
            description=tier["name"],
            automatic_payment_methods={"enabled": True},
            metadata={"tier": tier_key, "product": "ContentFlow AI"},
        )
        return jsonify({"clientSecret": intent.client_secret, "tier": tier_key})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature", "")

    if WEBHOOK_SECRET:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError) as e:
            return jsonify({"error": str(e)}), 400
    else:
        event = json.loads(payload)

    if event["type"] == "payment_intent.succeeded":
        intent = event["data"]["object"]
        tier = intent.get("metadata", {}).get("tier", "unknown")
        email = intent.get("receipt_email") or intent.get("charges", {}).get("data", [{}])[0].get("billing_details", {}).get("email", "")
        _handle_purchase(email, tier, intent["id"])

    return jsonify({"received": True})


def _handle_purchase(email, tier, payment_id):
    """Trigger ConvertKit subscribe + payload delivery after confirmed payment."""
    print(f"[PURCHASE] tier={tier} email={email} payment={payment_id}")
    if not email:
        return
    try:
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from monetization.agents.convertkit_sender import ConvertKitSender
        ck = ConvertKitSender()
        seq_id = os.getenv("CONVERTKIT_SEQUENCE_ID", "")
        if seq_id:
            ck.subscribe_to_sequence(email, email.split("@")[0], seq_id)
    except Exception as e:
        print(f"[WEBHOOK] ConvertKit error: {e}")


# ── ENTRY ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 4242))
    if not stripe.api_key:
        print("WARNING: STRIPE_SECRET_KEY not set — payment intents will fail")
    print(f"\nContentFlow AI checkout server")
    print(f"  Sales page : http://localhost:{port}/")
    print(f"  Checkout   : http://localhost:{port}/checkout?tier=pro")
    print(f"  Webhook    : http://localhost:{port}/api/webhook")
    print(f"  Mode       : {'LIVE' if stripe.api_key and not stripe.api_key.startswith('sk_test') else 'TEST'}\n")
    app.run(port=port, debug=False)
