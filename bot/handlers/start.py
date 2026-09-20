from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

from .. import database as db
from ..keyboards import language_keyboard, main_menu_keyboard
from ..texts import t

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    db.get_or_create_user(message.from_user.id, message.from_user.username)
    await message.answer(t("ru", "choose_language"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def on_language_chosen(callback: CallbackQuery):
    lang = callback.data.split(":")[1]
    db.set_language(callback.from_user.id, lang)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(t(lang, "welcome"), reply_markup=main_menu_keyboard(lang))
    await callback.answer()
