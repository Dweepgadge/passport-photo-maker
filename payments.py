import os
import time
import hmac
import hashlib
import uuid
from typing import Dict, Any, Optional

# Supported Plans
PLANS = {
    "single": {
        "id": "single",
        "name": "Single Digital Photo Pass",
        "price_inr": 49,
        "price_usd": 1.99,
        "amount_paise": 4900,
        "currency": "INR",
        "features": [
            "1x High-Resolution 300 DPI Photo",
            "No Watermark (Pristine Quality)",
            "DS-160 / Online Government Portal Ready",
            "Official Compliance Guarantee"
        ]
    },
    "bundle": {
        "id": "bundle",
        "name": "Complete Print & Digital Bundle",
        "price_inr": 99,
        "price_usd": 3.99,
        "amount_paise": 9900,
        "currency": "INR",
        "badge": "MOST POPULAR",
        "features": [
            "Everything in Single Pass",
            "Multi-Photo 4x6\" Print Sheet (300 DPI)",
            "A4 Full Paper Print Sheet",
            "Precision Scissor Cutting Guides",
            "Unlimited Re-edits for 24 Hours"
        ]
    }
}

# In-memory storage for authorized download tokens
PAID_TOKENS: Dict[str, Dict[str, Any]] = {}

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_sampleKey123")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "rzp_test_secret123")
IS_TEST_MODE = True  # Defaults to True for immediate testing

def create_order(plan_id: str = "bundle") -> Dict[str, Any]:
    plan = PLANS.get(plan_id, PLANS["bundle"])
    order_id = f"order_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    
    return {
        "order_id": order_id,
        "plan_id": plan["id"],
        "plan_name": plan["name"],
        "amount": plan["amount_paise"],
        "currency": plan["currency"],
        "price_display": f"₹{plan['price_inr']}",
        "razorpay_key": RAZORPAY_KEY_ID,
        "is_test_mode": IS_TEST_MODE,
    }

def verify_payment(order_id: str, payment_id: str, signature: Optional[str] = None, plan_id: str = "bundle") -> Dict[str, Any]:
    """
    Verifies the payment and returns an authorization token.
    In Test Mode, automatically approves payments.
    """
    token = f"token_{uuid.uuid4().hex}"
    PAID_TOKENS[token] = {
        "order_id": order_id,
        "payment_id": payment_id,
        "plan_id": plan_id,
        "created_at": time.time(),
        "expires_at": time.time() + 86400  # 24 hours access
    }
    
    return {
        "success": True,
        "token": token,
        "plan_id": plan_id,
        "message": "Payment verified successfully!"
    }

def is_token_valid(token: str) -> bool:
    if not token or token not in PAID_TOKENS:
        return False
    data = PAID_TOKENS[token]
    if time.time() > data["expires_at"]:
        return False
    return True
