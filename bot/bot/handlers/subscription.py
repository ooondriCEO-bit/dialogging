from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from .. import database as db
from ..config import PLANS, PAYMENTS_ENABLED
from ..keyboards import plans_keyboard, check_payment_keyboard
from ..payments import create_payment, get_payment_status
from ..texts import TEXTS, t

router = Router()


def _lang(user_id: int) -> str:
    return db.get_language(user_id)


@router.message(F.text.in_([TEXTS["ru"]["menu_subscription"], TEXTS["en"]["menu_subscription"]]))
async def show_plans(message: Message):
    lang = _lang(message.from_user.id)
    if not PAYMENTS_ENABLED:
        await message.answer(t(lang, "subscription_title"))
        await message.answer(t(lang, "subscription_coming_soon"))
        return
    await message.answer(t(lang, "subscription_title"), reply_markup=plans_keyboard(lang))


@router.callback_query(F.data.startswith("buy:"))
async def on_plan_chosen(callback: CallbackQuery):
    lang = _lang(callback.from_user.id)
    plan_key = callback.data.split(":")[1]
    plan = PLANS[plan_key]

    payment_id, url = create_payment(callback.from_user.id, plan_key)
    db.add_payment(payment_id, callback.from_user.id, plan_key, plan["price"])

    title = plan["title_ru"] if lang == "ru" else plan["title_en"]
    await callback.message.answer(
        t(lang, "payment_created", price=plan["price"], title=title, url=url),
        reply_markup=check_payment_keyboard(lang, payment_id),
        disable_web_page_preview=True,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("check:"))
async def on_check_payment(callback: CallbackQuery):
    lang = _lang(callback.from_user.id)
    payment_id = callback.data.split(":")[1]
    status = get_payment_status(payment_id)

    if status == "succeeded":
        row = db.get_pending_payments()  # чтобы найти plan_key для этого payment_id
        plan_key = None
        for r in row:
            if r["payment_id"] == payment_id:
                plan_key = r["plan_key"]
        if plan_key is None:
            # уже обработан ранее (например, фоновой проверкой)
            until = db.get_subscription_until(callback.from_user.id)
        else:
            db.update_payment_status(payment_id, "succeeded")
            days = PLANS[plan_key]["days"]
            until = db.extend_subscription(callback.from_user.id, days)
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(t(lang, "payment_success", date=until.strftime("%d.%m.%Y")))
    else:
        await callback.answer(t(lang, "payment_not_found"), show_alert=True)
