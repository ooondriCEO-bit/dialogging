from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo,
)

from .config import PLANS, PREMIUM_WEBAPP_URL
from .texts import t


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en"),
        ]
    ])


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=t(lang, "menu_support")), KeyboardButton(text=t(lang, "menu_faq"))],
            [KeyboardButton(text=t(lang, "menu_subscription"), web_app=WebAppInfo(url=PREMIUM_WEBAPP_URL))],
        ],
        resize_keyboard=True,
    )


def plans_keyboard(lang: str) -> InlineKeyboardMarkup:
    rows = []
    for key, plan in PLANS.items():
        title = plan["title_ru"] if lang == "ru" else plan["title_en"]
        rows.append([InlineKeyboardButton(
            text=t(lang, "plan_button", title=title, price=plan["price"]),
            callback_data=f"buy:{key}",
        )])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def check_payment_keyboard(lang: str, payment_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(lang, "check_payment_button"), callback_data=f"check:{payment_id}")]
    ])
