import os
from dotenv import load_dotenv

load_dotenv()

# --- Обязательные переменные (задаются в .env или в панели хостинга) ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))          # куда падают обращения в поддержку

# ID пользователей, которым разрешена рассылка (/broadcast). Можно перечислить
# несколько через запятую: ADMIN_IDS=111111,222222
# Если не задано — по умолчанию используется ADMIN_CHAT_ID (если это личный чат, а не группа).
_admin_ids_raw = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = {int(x) for x in _admin_ids_raw.split(",") if x.strip()}
if not ADMIN_IDS and ADMIN_CHAT_ID > 0:
    ADMIN_IDS = {ADMIN_CHAT_ID}
YOOKASSA_SHOP_ID = os.getenv("YOOKASSA_SHOP_ID")
YOOKASSA_SECRET_KEY = os.getenv("YOOKASSA_SECRET_KEY")

# Если ключи ЮKassa ещё не заданы — оплата отключена, но бот всё равно работает
# (поддержка и FAQ доступны сразу). Как только добавите оба ключа и перезапустите
# бота — кнопка "Подписка" появится сама, без правки кода.
PAYMENTS_ENABLED = bool(YOOKASSA_SHOP_ID and YOOKASSA_SECRET_KEY)

# Ссылка, на которую пользователь вернётся после оплаты (можно оставить как есть)
RETURN_URL = os.getenv("RETURN_URL", "https://t.me/")

DB_PATH = os.getenv("DB_PATH", "dialoging.db")

# Как часто (в секундах) бот сам проверяет статус неоплаченных платежей
PAYMENT_CHECK_INTERVAL = 60

# Ссылка на мини-апп (открывается по кнопке "Подписка" в меню).
# Как только сгенерируете публичный домен в Railway (Settings → Networking → Generate Domain),
# Railway обычно сам подставляет его в переменную RAILWAY_PUBLIC_DOMAIN — тогда ничего вписывать не надо.
# Если нет — впишите вручную WEBAPP_URL=https://ваш-домен.up.railway.app в Variables.
_railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
PREMIUM_WEBAPP_URL = os.getenv("WEBAPP_URL") or (
    f"https://{_railway_domain}" if _railway_domain else "https://claude.ai/artifact/Rvx3YgX49BS8DJk8KacHG3"
)
PLANS = {
    "premium": {"title_ru": "Premium", "title_en": "Premium", "price": 299, "days": 30},
}
