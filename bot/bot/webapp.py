import hashlib
import hmac
import json
from pathlib import Path
from urllib.parse import parse_qsl

from aiohttp import web

from . import database as db
from .config import BOT_TOKEN, ADMIN_CHAT_ID, ADMIN_IDS

STATIC_DIR = Path(__file__).parent / "webapp_static"


def _validate_init_data(init_data: str):
    """Проверяет подпись initData, которую передаёт Telegram WebApp.
    Возвращает dict с распарсенными полями (включая 'user' как dict) либо None, если подпись неверна."""
    if not init_data:
        return None
    try:
        parsed = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return None
    received_hash = parsed.pop("hash", None)
    if not received_hash or not BOT_TOKEN:
        return None
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    computed_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(computed_hash, received_hash):
        return None
    if "user" in parsed:
        try:
            parsed["user"] = json.loads(parsed["user"])
        except (ValueError, TypeError):
            parsed["user"] = None
    return parsed


async def handle_index(request):
    return web.FileResponse(STATIC_DIR / "index.html")


async def handle_get_news(request):
    return web.json_response(db.get_news())


async def handle_whoami(request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        body = {}
    data = _validate_init_data(body.get("init_data", ""))
    user = data.get("user") if data else None
    if not user:
        return web.json_response({"is_admin": False})
    return web.json_response({"is_admin": user.get("id") in ADMIN_IDS})


async def handle_post_news(request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"ok": False, "error": "bad_request"}, status=400)

    data = _validate_init_data(body.get("init_data", ""))
    user = data.get("user") if data else None
    if not user or user.get("id") not in ADMIN_IDS:
        return web.json_response({"ok": False, "error": "forbidden"}, status=403)

    text = (body.get("text") or "").strip()
    if not text:
        return web.json_response({"ok": False, "error": "empty"}, status=400)

    db.add_news(text)
    return web.json_response({"ok": True})


async def handle_post_support(request):
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"ok": False, "error": "bad_request"}, status=400)

    text = (body.get("text") or "").strip()
    if not text:
        return web.json_response({"ok": False, "error": "empty"}, status=400)

    data = _validate_init_data(body.get("init_data", ""))
    user = data.get("user") if data else None
    if not user or not user.get("id"):
        return web.json_response({"ok": False, "error": "no_user"}, status=400)

    user_id = user["id"]
    username = user.get("username")
    first_name = user.get("first_name") or "Пользователь"

    db.get_or_create_user(user_id, username)
    lang = db.get_language(user_id)

    bot = request.app["bot"]
    header = f"📩 Вопрос от @{username or user_id} ({first_name}, id: {user_id}, lang: {lang}) — из мини-аппа:\n\n"
    sent = await bot.send_message(ADMIN_CHAT_ID, header + text)
    db.link_support_message(sent.message_id, user_id)

    return web.json_response({"ok": True})


def create_app(bot) -> web.Application:
    app = web.Application()
    app["bot"] = bot
    app.router.add_get("/", handle_index)
    app.router.add_get("/api/news", handle_get_news)
    app.router.add_post("/api/news", handle_post_news)
    app.router.add_post("/api/support", handle_post_support)
    app.router.add_post("/api/whoami", handle_whoami)
    return app
