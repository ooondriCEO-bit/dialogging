from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from .. import database as db
from ..config import ADMIN_CHAT_ID
from ..texts import TEXTS, t

router = Router()


class SupportStates(StatesGroup):
    waiting_message = State()


def _lang(user_id: int) -> str:
    return db.get_language(user_id)


@router.message(F.text.in_([TEXTS["ru"]["menu_support"], TEXTS["en"]["menu_support"]]))
async def start_support(message: Message, state: FSMContext):
    lang = _lang(message.from_user.id)
    await message.answer(t(lang, "support_prompt"))
    await state.set_state(SupportStates.waiting_message)


@router.message(SupportStates.waiting_message)
async def forward_to_admin(message: Message, state: FSMContext, bot: Bot):
    lang = _lang(message.from_user.id)
    user = message.from_user
    header = f"📩 Вопрос от @{user.username or user.id} (id: {user.id}, lang: {lang}):\n\n"
    sent = await bot.send_message(ADMIN_CHAT_ID, header + message.text)
    db.link_support_message(sent.message_id, user.id)
    await message.answer(t(lang, "support_sent"))
    await state.clear()


# Админ отвечает: делает Reply на пересланное сообщение в админ-чате
@router.message(F.chat.id == ADMIN_CHAT_ID, F.reply_to_message)
async def admin_reply(message: Message, bot: Bot):
    user_id = db.get_support_user(message.reply_to_message.message_id)
    if user_id is None:
        return  # это не ответ на тикет поддержки — игнорируем
    lang = _lang(user_id)
    await bot.send_message(user_id, t(lang, "support_reply_prefix") + message.text)
    await message.reply("✅ Отправлено пользователю")
