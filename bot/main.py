import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from . import database as db
from .config import BOT_TOKEN, PAYMENT_CHECK_INTERVAL, PLANS
from .payments import get_payment_status
from .texts import t
from .handlers import start, faq, support, subscription

logging.basicConfig(level=logging.INFO)


async def payment_checker(bot: Bot):
    """Раз в PAYMENT_CHECK_INTERVAL секунд сам проверяет все неоплаченные счета в ЮKassa."""
    while True:
        await asyncio.sleep(PAYMENT_CHECK_INTERVAL)
        try:
            pending = db.get_pending_payments()
            for row in pending:
                status = get_payment_status(row["payment_id"])
                if status == "succeeded":
                    db.update_payment_status(row["payment_id"], "succeeded")
                    days = PLANS[row["plan_key"]]["days"]
                    until = db.extend_subscription(row["user_id"], days)
                    lang = db.get_language(row["user_id"])
                    await bot.send_message(
                        row["user_id"],
                        t(lang, "payment_success", date=until.strftime("%d.%m.%Y")),
                    )
                elif status == "canceled":
                    db.update_payment_status(row["payment_id"], "canceled")
        except Exception:
            logging.exception("Ошибка при фоновой проверке платежей")


async def main():
    db.init_db()

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(faq.router)
    dp.include_router(support.router)
    dp.include_router(subscription.router)

    asyncio.create_task(payment_checker(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
