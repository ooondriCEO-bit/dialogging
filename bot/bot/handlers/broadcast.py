import asyncio

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from .. import database as db
from ..config import ADMIN_IDS
from ..texts import t

router = Router()


class BroadcastStates(StatesGroup):
    waiting_text = State()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def _confirm_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text=t(lang, "broadcast_confirm_button"), callback_data="broadcast:confirm"),
        InlineKeyboardButton(text=t(lang, "broadcast_cancel_button"), callback_data="broadcast:cancel"),
    ]])


@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message, state: FSMContext):
    if not _is_admin(message.from_user.id):
        return  # не админ — молча игнорируем, чтобы не палить наличие команды
    lang = db.get_language(message.from_user.id)
    await message.answer(t(lang, "broadcast_prompt"))
    await state.set_state(BroadcastStates.waiting_text)


@router.message(BroadcastStates.waiting_text)
async def receive_broadcast_text(message: Message, state: FSMContext):
    lang = db.get_language(message.from_user.id)
    await state.update_data(broadcast_text=message.html_text)
    await message.answer(
        t(lang, "broadcast_preview", text=message.html_text),
        reply_markup=_confirm_keyboard(lang),
    )


@router.callback_query(F.data == "broadcast:cancel")
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    lang = db.get_language(callback.from_user.id)
    await callback.message.answer(t(lang, "broadcast_cancelled"))
    await callback.answer()


@router.callback_query(F.data == "broadcast:confirm")
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    text = data.get("broadcast_text", "")
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)
    lang = db.get_language(callback.from_user.id)

    sent, failed = 0, 0
    for user_id in db.get_all_user_ids():
        try:
            await bot.send_message(user_id, text)
            sent += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)  # не превышать лимиты Telegram API на массовую отправку

    await callback.message.answer(t(lang, "broadcast_done", sent=sent, failed=failed))
    await callback.answer()
