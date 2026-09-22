import sqlite3
import datetime
import threading

from .config import DB_PATH

_lock = threading.Lock()


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _lock, _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT DEFAULT 'ru',
                subscription_until TEXT,
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                payment_id TEXT PRIMARY KEY,
                user_id INTEGER,
                plan_key TEXT,
                amount REAL,
                status TEXT DEFAULT 'pending',
                created_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS support_map (
                admin_message_id INTEGER PRIMARY KEY,
                user_id INTEGER
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                created_at TEXT
            )
        """)
        conn.commit()


# ---------- users ----------

def get_or_create_user(user_id: int, username: str | None):
    with _lock, _connect() as conn:
        row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
                (user_id, username, datetime.datetime.utcnow().isoformat()),
            )
            conn.commit()
            row = conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()
        return row


def set_language(user_id: int, lang: str):
    with _lock, _connect() as conn:
        conn.execute("UPDATE users SET language=? WHERE user_id=?", (lang, user_id))
        conn.commit()


def get_language(user_id: int) -> str:
    with _lock, _connect() as conn:
        row = conn.execute("SELECT language FROM users WHERE user_id=?", (user_id,)).fetchone()
        return row["language"] if row else "ru"


def get_subscription_until(user_id: int):
    with _lock, _connect() as conn:
        row = conn.execute("SELECT subscription_until FROM users WHERE user_id=?", (user_id,)).fetchone()
        if row and row["subscription_until"]:
            return datetime.datetime.fromisoformat(row["subscription_until"])
        return None


def is_subscribed(user_id: int) -> bool:
    until = get_subscription_until(user_id)
    return bool(until and until > datetime.datetime.utcnow())


def extend_subscription(user_id: int, days: int):
    current = get_subscription_until(user_id)
    now = datetime.datetime.utcnow()
    base = current if (current and current > now) else now
    new_until = base + datetime.timedelta(days=days)
    with _lock, _connect() as conn:
        conn.execute(
            "UPDATE users SET subscription_until=? WHERE user_id=?",
            (new_until.isoformat(), user_id),
        )
        conn.commit()
    return new_until


# ---------- payments ----------

def add_payment(payment_id: str, user_id: int, plan_key: str, amount: float):
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT INTO payments (payment_id, user_id, plan_key, amount, created_at) VALUES (?, ?, ?, ?, ?)",
            (payment_id, user_id, plan_key, amount, datetime.datetime.utcnow().isoformat()),
        )
        conn.commit()


def update_payment_status(payment_id: str, status: str):
    with _lock, _connect() as conn:
        conn.execute("UPDATE payments SET status=? WHERE payment_id=?", (status, payment_id))
        conn.commit()


def get_pending_payments():
    with _lock, _connect() as conn:
        return conn.execute("SELECT * FROM payments WHERE status='pending'").fetchall()


# ---------- support ----------

def link_support_message(admin_message_id: int, user_id: int):
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO support_map (admin_message_id, user_id) VALUES (?, ?)",
            (admin_message_id, user_id),
        )
        conn.commit()


def get_support_user(admin_message_id: int):
    with _lock, _connect() as conn:
        row = conn.execute(
            "SELECT user_id FROM support_map WHERE admin_message_id=?", (admin_message_id,)
        ).fetchone()
        return row["user_id"] if row else None


# ---------- broadcast ----------

def get_all_user_ids():
    with _lock, _connect() as conn:
        rows = conn.execute("SELECT user_id FROM users").fetchall()
        return [r["user_id"] for r in rows]


# ---------- news ----------

def add_news(text: str):
    with _lock, _connect() as conn:
        conn.execute(
            "INSERT INTO news (text, created_at) VALUES (?, ?)",
            (text, datetime.datetime.utcnow().isoformat()),
        )
        conn.commit()


def get_news(limit: int = 30):
    with _lock, _connect() as conn:
        rows = conn.execute(
            "SELECT id, text, created_at FROM news ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
