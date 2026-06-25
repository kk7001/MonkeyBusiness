"""
Paseli (e-amusement virtual currency) storage — one balance per UID.

Table schema:
    uid         INTEGER PRIMARY KEY  — user account ID
    balance     INTEGER              — current balance (default from config.paseli)
    total_spent INTEGER              — lifetime spending
"""

import config
from core_database import get_db


def _ensure_table():
    """Create paseli table if not exist. Migrate from old format if needed."""
    conn = get_db().conn

    old_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='paseli'"
    ).fetchone()

    if old_exists:
        cols = conn.execute("PRAGMA table_info('paseli')").fetchall()
        col_names = [c["name"] for c in cols]
        if "data" in col_names:
            import json
            rows = conn.execute("SELECT data FROM paseli").fetchall()
            old_data = [json.loads(r["data"]) for r in rows]
            conn.execute("DROP TABLE paseli")
            conn.commit()
        elif "cardid" in col_names:
            # Drop old cardid-based schema
            conn.execute("DROP TABLE paseli")
            conn.commit()
        else:
            return

    conn.execute(
        "CREATE TABLE IF NOT EXISTS paseli ("
        "  uid         INTEGER PRIMARY KEY,"
        "  balance     INTEGER NOT NULL DEFAULT 0,"
        "  total_spent INTEGER NOT NULL DEFAULT 0"
        ")"
    )
    conn.commit()

    if old_exists and 'data' in str(col_names):
        for doc in old_data:
            conn.execute(
                "INSERT OR IGNORE INTO paseli (uid, balance, total_spent) VALUES (?, ?, ?)",
                (doc.get("uid", doc.get("cardid", 0)), doc.get("balance", config.paseli), doc.get("total_spent", 0)),
            )
        conn.commit()


def get(uid):
    """Get paseli row as dict, or None."""
    _ensure_table()
    conn = get_db().conn
    row = conn.execute(
        "SELECT uid, balance, total_spent FROM paseli WHERE uid = ?", (uid,)
    ).fetchone()
    return dict(row) if row else None


def get_balance(uid):
    """Get balance, returning config default if not found."""
    row = get(uid)
    return row["balance"] if row else config.paseli


def set(uid, balance=None, total_spent=None):
    """Upsert paseli row."""
    _ensure_table()
    conn = get_db().conn
    existing = get(uid)
    if existing:
        new_balance = balance if balance is not None else existing["balance"]
        new_spent = total_spent if total_spent is not None else existing["total_spent"]
        conn.execute(
            "UPDATE paseli SET balance = ?, total_spent = ? WHERE uid = ?",
            (new_balance, new_spent, uid),
        )
    else:
        new_balance = balance if balance is not None else config.paseli
        new_spent = total_spent if total_spent is not None else 0
        conn.execute(
            "INSERT INTO paseli (uid, balance, total_spent) VALUES (?, ?, ?)",
            (uid, new_balance, new_spent),
        )
    conn.commit()


def add_spend(uid, amount):
    """Deduct balance and add to total_spent. Returns new balance."""
    _ensure_table()
    conn = get_db().conn
    existing = get(uid)
    if existing:
        new_balance = existing["balance"] - amount
        new_spent = existing["total_spent"] + amount
        if new_balance < 1000 or new_balance > config.paseli:
            new_balance = config.paseli
        conn.execute(
            "UPDATE paseli SET balance = ?, total_spent = ? WHERE uid = ?",
            (new_balance, new_spent, uid),
        )
    else:
        new_balance = config.paseli - amount
        if new_balance < 1000 or new_balance > config.paseli:
            new_balance = config.paseli
        conn.execute(
            "INSERT INTO paseli (uid, balance, total_spent) VALUES (?, ?, ?)",
            (uid, new_balance, amount),
        )
    conn.commit()
    return new_balance
