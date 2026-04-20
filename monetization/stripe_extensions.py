#!/usr/bin/env python3
"""
Stripe extensions — subscription management, webhook handling, automated refunds.
Import and register these routes onto the existing checkout_server Flask app.
"""

import os
import json
import stripe
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(__file__).parent.parent / ".env")

stripe.api_key     = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET     = os.getenv("STRIPE_WEBHOOK_SECRET", "")
REFUND_WINDOW_DAYS = int(os.getenv("REFUND_WINDOW_DAYS", "30"))

bp = Blueprint("stripe_ext", __name__)

# Price IDs — set these in .env or replace with your actual Stripe price IDs
PRICE_IDS = {
    "starter": os.getenv("STRIPE_PRICE_STARTER"),
    "pro":     os.getenv("STRIPE_PRICE_PRO"),
    "agency":  os.getenv("STRIPE_PRICE_AGENCY"),
}


# ── SUBSCRIPTIONS ────────────────────────────────────────────────────────────

@bp.route("/api/create-subscription", methods=["POST"])
def create_subscription():
    data     = request.get_json(silent=True) or {}
    tier     = data.get("tier", "pro").lower()
    email    = data.get("email", "").strip()
    price_id = PRICE_IDS.get(tier)

    if not email:
        return jsonify({"error": "email required"}), 400
    if not price_id:
        return jsonify({"error": f"No price ID configured for tier '{tier}'. Set STRIPE_PRICE_{tier.upper()} in .env"}), 400

    try:
        customer = _get_or_create_customer(email)
        sub = stripe.Subscription.create(
            customer=customer.id,
            items=[{"price": price_id}],
            payment_behavior="default_incomplete",
            payment_settings={"save_default_payment_method": "on_subscription"},
            expand=["latest_invoice.payment_intent"],
            metadata={"tier": tier, "product": "ContentFlow AI"},
        )
        intent = sub.latest_invoice.payment_intent
        return jsonify({
            "subscriptionId": sub.id,
            "clientSecret":   intent.client_secret,
            "status":         sub.status,
        })
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/api/cancel-subscription", methods=["POST"])
def cancel_subscription():
    data = request.get_json(silent=True) or {}
    sub_id = data.get("subscriptionId")
    if not sub_id:
        return jsonify({"error": "subscriptionId required"}), 400

    try:
        sub = stripe.Subscription.cancel(sub_id)
        return jsonify({"status": sub.status, "canceledAt": sub.canceled_at})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400


@bp.route("/api/subscription-status", methods=["GET"])
def subscription_status():
    email = request.args.get("email", "").strip()
    if not email:
        return jsonify({"error": "email required"}), 400

    customers = stripe.Customer.list(email=email, limit=1).data
    if not customers:
        return jsonify({"active": False, "subscriptions": []})

    subs = stripe.Subscription.list(customer=customers[0].id, status="active").data
    return jsonify({
        "active": len(subs) > 0,
        "subscriptions": [{"id": s.id, "tier": s.metadata.get("tier"), "status": s.status} for s in subs],
    })


# ── REFUNDS ──────────────────────────────────────────────────────────────────

@bp.route("/api/refund", methods=["POST"])
def create_refund():
    data       = request.get_json(silent=True) or {}
    payment_id = data.get("paymentIntentId")
    reason     = data.get("reason", "requested_by_customer")

    if not payment_id:
        return jsonify({"error": "paymentIntentId required"}), 400

    valid_reasons = {"duplicate", "fraudulent", "requested_by_customer"}
    if reason not in valid_reasons:
        reason = "requested_by_customer"

    try:
        intent = stripe.PaymentIntent.retrieve(payment_id)
        charge_id = intent.latest_charge

        if not charge_id:
            return jsonify({"error": "No charge found for this payment intent"}), 400

        refund = stripe.Refund.create(charge=charge_id, reason=reason)
        return jsonify({"refundId": refund.id, "status": refund.status, "amount": refund.amount})
    except stripe.error.StripeError as e:
        return jsonify({"error": str(e)}), 400


# ── WEBHOOKS ─────────────────────────────────────────────────────────────────

@bp.route("/api/webhook/v2", methods=["POST"])
def webhook_v2():
    payload    = request.data
    sig_header = request.headers.get("Stripe-Signature", "")

    if not WEBHOOK_SECRET:
        return jsonify({"error": "STRIPE_WEBHOOK_SECRET not set — cannot verify webhook"}), 500

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError:
        return jsonify({"error": "invalid payload"}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({"error": "invalid signature"}), 400

    etype = event["type"]
    obj   = event["data"]["object"]

    handlers = {
        "payment_intent.succeeded":           _on_payment_succeeded,
        "customer.subscription.created":      _on_subscription_created,
        "customer.subscription.deleted":      _on_subscription_cancelled,
        "invoice.payment_failed":             _on_payment_failed,
        "charge.dispute.created":             _on_dispute_created,
    }

    handler = handlers.get(etype)
    if handler:
        handler(obj)

    return jsonify({"received": True, "type": etype})


# ── EVENT HANDLERS ───────────────────────────────────────────────────────────

def _on_payment_succeeded(intent):
    tier  = intent.get("metadata", {}).get("tier", "unknown")
    email = _email_from_intent(intent)
    print(f"[PAYMENT] tier={tier} email={email} id={intent['id']}")
    _trigger_delivery(email, tier, intent["id"])


def _on_subscription_created(sub):
    tier     = sub.get("metadata", {}).get("tier", "unknown")
    customer = stripe.Customer.retrieve(sub["customer"])
    email    = customer.get("email", "")
    print(f"[SUB CREATED] tier={tier} email={email} sub={sub['id']}")


def _on_subscription_cancelled(sub):
    customer = stripe.Customer.retrieve(sub["customer"])
    email    = customer.get("email", "")
    print(f"[SUB CANCELLED] email={email} sub={sub['id']}")


def _on_payment_failed(invoice):
    customer = stripe.Customer.retrieve(invoice["customer"])
    email    = customer.get("email", "")
    print(f"[PAYMENT FAILED] email={email} invoice={invoice['id']} — consider retry logic")


def _on_dispute_created(charge):
    print(f"[DISPUTE] charge={charge['id']} amount={charge.get('amount')} — review required")


# ── HELPERS ──────────────────────────────────────────────────────────────────

def _get_or_create_customer(email: str):
    existing = stripe.Customer.list(email=email, limit=1).data
    if existing:
        return existing[0]
    return stripe.Customer.create(email=email)


def _email_from_intent(intent) -> str:
    email = intent.get("receipt_email", "")
    if not email:
        try:
            charges = intent.get("charges", {}).get("data", [])
            if charges:
                email = charges[0].get("billing_details", {}).get("email", "")
        except Exception:
            pass
    return email or ""


def _trigger_delivery(email: str, tier: str, payment_id: str):
    if not email:
        return
    try:
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from monetization.agents.convertkit_sender import ConvertKitSender
        ck     = ConvertKitSender()
        seq_id = os.getenv("CONVERTKIT_SEQUENCE_ID", "")
        if seq_id:
            ck.subscribe_to_sequence(email, email.split("@")[0], seq_id)
    except Exception as e:
        print(f"[DELIVERY] ConvertKit error: {e}")
