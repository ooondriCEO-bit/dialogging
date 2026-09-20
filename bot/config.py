import os
from dotenv import load_dotenv

load_dotenv()

# --- Обязательные переменные (задаются в .env или в панели хостинга) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))          # куда падают обращения в поддержку
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

# Ссылка, на которую пользователь вернётся после оплаты (можно оставить как есть)
RETURN_URL = os.getenv("RETURN_URL", "https://t.me/")

DB_PATH = os.getenv("DB_PATH", "dialoging.db")

# Как часто (в секундах) бот сам проверяет статус неоплаченных платежей
PAYMENT_CHECK_INTERVAL = 60

# --- Тарифы подписки. Меняйте цены/сроки здесь, без правки остального кода ---
PLANS = {
    "1m": {"title_ru": "1 месяц",  "title_en": "1 month",  "price": 299,  "days": 30},
    "3m": {"title_ru": "3 месяца", "title_en": "3 months", "price": 699,  "days": 90},
    "12m": {"title_ru": "12 месяцев", "title_en": "12 months", "price": 1990, "days": 365},
}
