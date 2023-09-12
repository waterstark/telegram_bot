from yookassa import Configuration, Payment

from config import SHOP_ID, SHOP_API_TOKEN

import asyncio
import json


Configuration.account_id = SHOP_ID
Configuration.secret_key = SHOP_API_TOKEN


def payment(value, description):
    payment = Payment.create(
        {
            "amount": {"value": value, "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": "https://web.telegram.org/a/#5992743378",
            },
            "capture": True,
            "description": description,
        }
    )
    return json.loads(payment.json())


async def check_payment(payment_id):
    payment = json.loads((Payment.find_one(payment_id)).json())
    while payment["status"] == "pending":
        payment = json.loads((Payment.find_one(payment_id)).json())
        await asyncio.sleep(3)

    if payment["status"] == "succeeded":
        print("SUCCSESS RETURN")
        print(payment)
        return True
    else:
        print("BAD RETURN")
        print(payment)
        return False
