"""
One-time migration script: convert existing TinyDB db.json to SQLite3 db.sqlite3.

Usage:
    python migrate_json_to_sqlite.py [db.json] [db.sqlite3]

If no arguments are given, defaults to "db.json" -> "db.sqlite3".
If db.json doesn't exist, the script exits cleanly.
"""

import json
import os
import sys

# Temporarily import TinyDB for reading the old database
try:
    from tinydb import TinyDB
except ImportError:
    print("ERROR: tinydb is required to read the old db.json.")
    print("Install it with: pip install tinydb")
    sys.exit(1)

from core_database import SQLiteDB


def migrate(json_path="db.json", sqlite_path="db.sqlite3"):
    if not os.path.exists(json_path):
        print(f"No {json_path} found — nothing to migrate.")
        return

    if os.path.exists(sqlite_path):
        print(f"WARNING: {sqlite_path} already exists. Remove it first to re-migrate.")
        return

    print(f"Reading {json_path} ...")
    old_db = TinyDB(json_path)

    new_db = SQLiteDB(sqlite_path)

    # TinyDB stores all tables in the JSON. We need to discover table names.
    # TinyDB's internal structure is {"_default": {...}, "table1": {...}, ...}
    # We can read the JSON directly to find table keys.
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # raw is a dict where keys are table names; "_default" is the default table
    table_names = [k for k in raw.keys() if not k.startswith("_")]

    # Also check for tables stored under numbered keys in older TinyDB versions
    for key in raw.keys():
        if isinstance(raw[key], dict):
            # It's a table
            pass

    print(f"Found tables: {table_names}")

    total_docs = 0
    for table_name in table_names:
        table = old_db.table(table_name)
        docs = table.all()
        if not docs:
            print(f"  {table_name}: empty, skipping")
            continue

        new_table = new_db.table(table_name)
        for doc in docs:
            doc.pop("doc_id", None)  # Remove old doc_id, let SQLite assign new one
            new_table.insert(doc)
            total_docs += 1

        print(f"  {table_name}: {len(docs)} documents migrated")

    old_db.close()
    new_db.close()

    json_size = os.path.getsize(json_path)
    sqlite_size = os.path.getsize(sqlite_path)

    print()
    print(f"Migration complete: {total_docs} documents across {len(table_names)} tables")
    print(f"  {json_path}: {json_size / 1024:.1f} KB")
    print(f"  {sqlite_path}: {sqlite_size / 1024:.1f} KB")
    print()
    print("You can now remove db.json (keep a backup if you like).")


if __name__ == "__main__":
    json_path = sys.argv[1] if len(sys.argv) > 1 else "db.json"
    sqlite_path = sys.argv[2] if len(sys.argv) > 2 else "db.sqlite3"
    migrate(json_path, sqlite_path)
