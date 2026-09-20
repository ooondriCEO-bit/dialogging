TEXTS = {
    "ru": {
        "choose_language": "Выберите язык / Choose language:",
        "welcome": (
            "Привет! 👋 Это бот поддержки <b>Dialoging</b>.\n\n"
            "Здесь можно:\n"
            "• задать вопрос в поддержку\n"
            "• посмотреть частые вопросы (FAQ)\n"
            "• оформить или продлить подписку"
        ),
        "menu_support": "💬 Поддержка",
        "menu_faq": "ℹ️ FAQ",
        "menu_subscription": "💳 Подписка",
        "menu_status": "👤 Мой статус",
        "faq_text": (
            "<b>Частые вопросы</b>\n\n"
            "❓ <b>Что такое Dialoging?</b>\n"
            "Приложение для поиска новых друзей и правильного круга общения — "
            "формат похож на свайпы, но цель не пара, а дружба.\n\n"
            "❓ <b>Как отменить подписку?</b>\n"
            "Напишите нам в поддержку — отменим и ответим на вопросы по возврату.\n\n"
            "❓ <b>Не приходит письмо/доступ после оплаты?</b>\n"
            "Обычно это занимает до 1 минуты. Если дольше — напишите в поддержку, "
            "приложите скриншот оплаты."
        ),
        "support_prompt": (
            "Опишите свой вопрос одним сообщением — я передам его команде, "
            "и вам ответят прямо здесь, в этом чате."
        ),
        "support_sent": "Спасибо! Ваше сообщение передано команде поддержки. Обычно отвечаем в течение дня.",
        "support_reply_prefix": "💬 <b>Ответ поддержки:</b>\n\n",
        "subscription_title": "Выберите тариф подписки:",
        "subscription_status_active": "✅ Подписка активна до {date}",
        "subscription_status_none": "У вас пока нет активной подписки.",
        "plan_button": "{title} — {price}₽",
        "payment_created": (
            "Счёт создан на сумму {price}₽ ({title}).\n\n"
            "1️⃣ Оплатите по ссылке ниже\n"
            "2️⃣ После оплаты нажмите «Проверить оплату»\n\n"
            "Ссылка: {url}"
        ),
        "check_payment_button": "🔄 Проверить оплату",
        "payment_not_found": "Пока не вижу оплату. Если вы уже оплатили — подождите немного и нажмите ещё раз.",
        "payment_success": "✅ Оплата получена! Подписка активна до {date}. Спасибо!",
        "back_button": "⬅️ Назад",
    },
    "en": {
        "choose_language": "Choose language / Выберите язык:",
        "welcome": (
            "Hi! 👋 This is the <b>Dialoging</b> support bot.\n\n"
            "Here you can:\n"
            "• ask a support question\n"
            "• check the FAQ\n"
            "• subscribe or renew your subscription"
        ),
        "menu_support": "💬 Support",
        "menu_faq": "ℹ️ FAQ",
        "menu_subscription": "💳 Subscription",
        "menu_status": "👤 My status",
        "faq_text": (
            "<b>Frequently Asked Questions</b>\n\n"
            "❓ <b>What is Dialoging?</b>\n"
            "An app for finding new friends and the right social circle — "
            "swipe-style, but the goal is friendship, not dating.\n\n"
            "❓ <b>How do I cancel my subscription?</b>\n"
            "Message our support — we'll cancel it and help with refund questions.\n\n"
            "❓ <b>No access after payment?</b>\n"
            "It usually takes up to 1 minute. If longer, contact support with a payment screenshot."
        ),
        "support_prompt": (
            "Describe your question in one message — I'll forward it to the team, "
            "and you'll get a reply right here in this chat."
        ),
        "support_sent": "Thanks! Your message was sent to our support team. We usually reply within a day.",
        "support_reply_prefix": "💬 <b>Support reply:</b>\n\n",
        "subscription_title": "Choose a subscription plan:",
        "subscription_status_active": "✅ Subscription active until {date}",
        "subscription_status_none": "You don't have an active subscription yet.",
        "plan_button": "{title} — {price} RUB",
        "payment_created": (
            "Invoice created for {price} RUB ({title}).\n\n"
            "1️⃣ Pay via the link below\n"
            "2️⃣ After paying, tap “Check payment”\n\n"
            "Link: {url}"
        ),
        "check_payment_button": "🔄 Check payment",
        "payment_not_found": "Payment not found yet. If you already paid, wait a bit and try again.",
        "payment_success": "✅ Payment received! Subscription active until {date}. Thank you!",
        "back_button": "⬅️ Back",
    },
}


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text
