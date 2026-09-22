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
