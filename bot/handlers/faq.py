from aiogram import Router, F
from aiogram.types import Message

from .. import database as db
from ..texts import TEXTS, t

router = Router()


def _lang(user_id: int) -> str:
    return db.get_language(user_id)


@router.message(F.text.in_([TEXTS["ru"]["menu_faq"], TEXTS["en"]["menu_faq"]]))
async def show_faq(message: Message):
    lang = _lang(message.from_user.id)
    await message.answer(t(lang, "faq_text"))


@router.message(F.text.in_([TEXTS["ru"]["menu_status"], TEXTS["en"]["menu_status"]]))
async def show_status(message: Message):
    lang = _lang(message.from_user.id)
    until = db.get_subscription_until(message.from_user.id)
    if until and db.is_subscribed(message.from_user.id):
        await message.answer(t(lang, "subscription_status_active", date=until.strftime("%d.%m.%Y")))
    else:
        await message.answer(t(lang, "subscription_status_none"))
