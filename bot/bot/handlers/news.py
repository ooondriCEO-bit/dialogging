from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .. import database as db
from ..config import ADMIN_IDS
from ..texts import t

router = Router()


class NewsStates(StatesGroup):
    waiting_text = State()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def _confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "news_confirm_button"), callback_data="news:confirm"),
        InlineKeyboardButton(text=t(lang, "news_cancel_button"), callback_data="news:cancel"),
    ]])


@router.message(Command("addnews"))
async def cmd_addnews(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return  # не админ — молча игнорируем
    lang = db.get_language(message.from_user.id)
    await message.answer(t(lang, "news_prompt"))
    await state.set_state(NewsStates.waiting_text)


@router.message(NewsStates.waiting_text)
async def receive_news_text(message: Message, state: FSMContext):
    lang = db.get_language(message.from_user.id)
    await state.update_data(news_text=message.text)
    await message.answer(
        t(lang, "news_preview", text=message.text),
        reply_markup=_confirm_keyboard(lang),
    )


@router.callback_query(F.data == "news:cancel")
async def cancel_news(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    lang = db.get_language(callback.from_user.id)
    await callback.message.answer(t(lang, "news_cancelled"))
    await callback.answer()


@router.callback_query(F.data == "news:confirm")
async def confirm_news(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text = data.get("news_text", "")
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)

    db.add_news(text)

    lang = db.get_language(callback.from_user.id)
    await callback.message.answer(t(lang, "news_done"))
    await callback.answer()
