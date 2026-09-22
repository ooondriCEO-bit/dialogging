import uuid
from yookassa import Configuration, Payment

from .config import YOOKASSA_SHOP_ID, YOOKASSA_SECRET_KEY, RETURN_URL, PLANS

Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


def create_payment(user_id: int, plan_key: str):
    plan = PLANS[plan_key]
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": f"{plan['price']:.2f}",
            "currency": "RUB",
        },
        "confirmation": {
            "type": "redirect",
            "return_url": RETURN_URL,
        },
        "capture": True,
        "description": f"Dialoging subscription: {plan_key} (user {user_id})",
        "metadata": {
            "user_id": str(user_id),
            "plan_key": plan_key,
        },
    }, idempotence_key)
    return payment.id, payment.confirmation.confirmation_url


def get_payment_status(payment_id: str) -> str:
    payment = Payment.find_one(payment_id)
    return payment.status  # 'pending' | 'waiting_for_capture' | 'succeeded' | 'canceled'
