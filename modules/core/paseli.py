"""
Paseli (e-amusement virtual currency) storage with explicit SQL columns.

Table schema:
    cardid      TEXT PRIMARY KEY  — access card ID
    balance     INTEGER           — current balance (default from config.paseli)
    total_spent INTEGER           — lifetime spending
    pin         TEXT              — unified card PIN (shared across all games)
"""

import config
from core_database import get_db


def _ensure_table():
    """Create the paseli table with explicit columns if it doesn't exist.
    Also migrates data from the old generic JSON blob format if present."""
    conn = get_db().conn

    # Check if old-format table exists (doc_id + data columns)
    old_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='paseli'"
    ).fetchone()

    if old_exists:
        # Check if it's the old format by looking for the 'data' column
        cols = conn.execute("PRAGMA table_info('paseli')").fetchall()
        col_names = [c["name"] for c in cols]
        if "data" in col_names:
            # Migrate old data
            rows = conn.execute("SELECT data FROM paseli").fetchall()
            old_data = []
            for row in rows:
                import json
                doc = json.loads(row["data"])
                old_data.append(doc)
            conn.execute("DROP TABLE paseli")
            conn.commit()
        else:
            # Already in new format
            return

    conn.execute(
        "CREATE TABLE IF NOT EXISTS paseli ("
        "  cardid   TEXT PRIMARY KEY,"
        "  balance  INTEGER NOT NULL DEFAULT 0,"
        "  total_spent INTEGER NOT NULL DEFAULT 0,"
        "  pin      TEXT"
        ")"
    )
    conn.commit()

    # Insert migrated data
    if old_exists and old_data:
        for doc in old_data:
            conn.execute(
                "INSERT OR IGNORE INTO paseli (cardid, balance, total_spent, pin) "
                "VALUES (?, ?, ?, ?)",
                (
                    doc.get("cardid", ""),
                    doc.get("balance", config.paseli),
                    doc.get("total_spent", 0),
                    doc.get("pin", None),
                ),
            )
        conn.commit()


def get(cardid):
    """Get paseli row as a dict, or None if not found."""
    _ensure_table()
    conn = get_db().conn
    row = conn.execute(
        "SELECT cardid, balance, total_spent, pin FROM paseli WHERE cardid = ?",
        (cardid,),
    ).fetchone()
    return dict(row) if row else None


def get_balance(cardid):
    """Get balance for a card, returning config default if not found."""
    row = get(cardid)
    return row["balance"] if row else config.paseli


def get_pin(cardid):
    """Get unified PIN for a card."""
    row = get(cardid)
    return row.get("pin") if row else None


def set(cardid, balance=None, total_spent=None, pin=None):
    """Upsert paseli row. Only updates fields that are not None."""
    _ensure_table()
    conn = get_db().conn

    existing = get(cardid)
    if existing:
        new_balance = balance if balance is not None else existing["balance"]
        new_spent = total_spent if total_spent is not None else existing["total_spent"]
        new_pin = pin if pin is not None else existing.get("pin")
        conn.execute(
            "UPDATE paseli SET balance = ?, total_spent = ?, pin = ? WHERE cardid = ?",
            (new_balance, new_spent, new_pin, cardid),
        )
    else:
        new_balance = balance if balance is not None else config.paseli
        new_spent = total_spent if total_spent is not None else 0
        conn.execute(
            "INSERT INTO paseli (cardid, balance, total_spent, pin) VALUES (?, ?, ?, ?)",
            (cardid, new_balance, new_spent, pin),
        )
    conn.commit()


def set_pin(cardid, pin):
    """Set PIN for a card. Creates paseli entry with default balance if new."""
    _ensure_table()
    conn = get_db().conn

    existing = get(cardid)
    if existing:
        conn.execute(
            "UPDATE paseli SET pin = ? WHERE cardid = ?",
            (pin, cardid),
        )
    else:
        conn.execute(
            "INSERT INTO paseli (cardid, balance, total_spent, pin) VALUES (?, ?, ?, ?)",
            (cardid, config.paseli, 0, pin),
        )
    conn.commit()


def add_spend(cardid, amount):
    """Deduct balance and add to total_spent. Returns new balance.
    Creates entry with default balance if card not found."""
    _ensure_table()
    conn = get_db().conn

    existing = get(cardid)
    if existing:
        new_balance = existing["balance"] - amount
        new_spent = existing["total_spent"] + amount
        if new_balance < 1000 or new_balance > config.paseli:
            new_balance = config.paseli
        conn.execute(
            "UPDATE paseli SET balance = ?, total_spent = ? WHERE cardid = ?",
            (new_balance, new_spent, cardid),
        )
    else:
        new_balance = config.paseli - amount
        if new_balance < 1000 or new_balance > config.paseli:
            new_balance = config.paseli
        conn.execute(
            "INSERT INTO paseli (cardid, balance, total_spent) VALUES (?, ?, ?)",
            (cardid, new_balance, amount),
        )
    conn.commit()
    return new_balance
