import sqlite3
import json
import threading


# =============================================================================
# Document — dict subclass with .doc_id attribute access (TinyDB compat)
# =============================================================================

class Document(dict):
    """A dict subclass: missing keys return 0; cannot store empty strings."""

    def __missing__(self, key):
        return 0

    def __setitem__(self, key, value):
        if value == "" or value is None:
            return  # silently drop empty values
        super().__setitem__(key, value)

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(f"'Document' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'Document' object has no attribute '{name}'")


# =============================================================================
# Query API (TinyDB-compatible)
# =============================================================================

class Condition:
    """A single query condition: field OP value."""
    def __init__(self, field, op, value):
        self.field = field
        self.op = op
        self.value = value

    def __and__(self, other):
        if isinstance(other, CompoundCondition):
            return CompoundCondition([self] + other.conditions)
        elif isinstance(other, Condition):
            return CompoundCondition([self, other])
        return NotImplemented

    def __repr__(self):
        return f"Condition({self.field} {self.op} {self.value!r})"


class CompoundCondition:
    """Multiple conditions joined by AND."""
    def __init__(self, conditions):
        self.conditions = conditions

    def __and__(self, other):
        if isinstance(other, CompoundCondition):
            return CompoundCondition(self.conditions + other.conditions)
        elif isinstance(other, Condition):
            return CompoundCondition(self.conditions + [other])
        return NotImplemented

    def __repr__(self):
        return f"CompoundCondition({self.conditions!r})"


class QueryField:
    """Returned by where() or Query().field — supports comparison operators."""
    def __init__(self, field):
        self._field = field

    def __eq__(self, value):
        return Condition(self._field, "=", value)

    def __ne__(self, value):
        return Condition(self._field, "!=", value)

    def __lt__(self, value):
        return Condition(self._field, "<", value)

    def __le__(self, value):
        return Condition(self._field, "<=", value)

    def __gt__(self, value):
        return Condition(self._field, ">", value)

    def __ge__(self, value):
        return Condition(self._field, ">=", value)

    def __repr__(self):
        return f"QueryField({self._field!r})"


class Query:
    """TinyDB-compatible Query builder: Query().field == value."""
    def __getattr__(self, name):
        return QueryField(name)


def where(field):
    """TinyDB-compatible where() function: where("field") == value."""
    return QueryField(field)


# =============================================================================
# TableProxy — wraps a SQLite table
# =============================================================================

_JSON_COLUMN_TYPES = {"JSON", "JSON_LIST", "JSON_DICT"}


class TableProxy:
    """Access a SQLite table. Supports two modes:

    - schema=None (legacy): generic doc_id + data JSON blob, queried via json_extract
    - schema=dict: explicit columns defined by schema, conditions use column names directly
    """

    def __init__(self, conn, table_name, schema=None):
        self.conn = conn
        self.table_name = table_name
        self.schema = schema
        self._is_legacy = schema is None
        self._json_cols = set()
        if not self._is_legacy:
            for col, typedef in schema.items():
                if any(jt in typedef.upper() for jt in _JSON_COLUMN_TYPES):
                    self._json_cols.add(col)
        self._ensure_table()

    def _ensure_table(self):
        if self._is_legacy:
            self.conn.execute(
                f'CREATE TABLE IF NOT EXISTS "{self.table_name}" ('
                f'  doc_id INTEGER PRIMARY KEY AUTOINCREMENT,'
                f'  data TEXT NOT NULL'
                f')'
            )
            self.conn.commit()
            return

        # Check if table exists with old legacy format and migrate
        existing = self.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (self.table_name,)
        ).fetchone()

        if existing:
            cols = self.conn.execute(
                f"PRAGMA table_info('{self.table_name}')"
            ).fetchall()
            col_names = [c["name"] for c in cols]
            if "data" in col_names:
                # Migrate from legacy JSON blob to explicit columns
                rows = self.conn.execute(
                    f'SELECT * FROM "{self.table_name}"'
                ).fetchall()
                old_docs = []
                for row in rows:
                    doc = json.loads(row["data"])
                    if "doc_id" in row.keys():
                        doc["doc_id"] = row["doc_id"]
                    old_docs.append(doc)
                self.conn.execute(f'DROP TABLE "{self.table_name}"')
                self.conn.commit()
                # Create new table
                col_defs = ", ".join(
                    f'"{col}" {typedef}' for col, typedef in self.schema.items()
                )
                self.conn.execute(
                    f'CREATE TABLE "{self.table_name}" ({col_defs})'
                )
                self.conn.commit()
                # Re-insert migrated data
                for doc in old_docs:
                    serialized = self._serialize_doc(doc)
                    cols = [f'"{k}"' for k in serialized.keys()]
                    placeholders = ", ".join("?" for _ in serialized)
                    self.conn.execute(
                        f'INSERT INTO "{self.table_name}" ({", ".join(cols)}) VALUES ({placeholders})',
                        list(serialized.values())
                    )
                self.conn.commit()
                return

        # Create new table
        col_defs = ", ".join(
            f'"{col}" {typedef}' for col, typedef in self.schema.items()
        )
        self.conn.execute(
            f'CREATE TABLE IF NOT EXISTS "{self.table_name}" ({col_defs})'
        )
        self.conn.commit()

    # -- helpers ---------------------------------------------------------------

    def _row_to_doc(self, row):
        """Convert a sqlite3.Row to a Document."""
        if self._is_legacy:
            doc = json.loads(row["data"])
            doc["doc_id"] = row["doc_id"]
        else:
            doc = {}
            row_keys = set(row.keys())
            for key, typedef in self.schema.items():
                if key in row_keys:
                    val = row[key]
                else:
                    # Column not in row — use default based on type
                    tu = typedef.upper()
                    if "JSON" in tu:
                        val = {} if "LIST" not in tu else []
                    else:
                        # All non-JSON fields default to 0, avoiding '' for XML int compat
                        val = 0
                if key in self._json_cols:
                    if isinstance(val, str) and val != "":
                        try:
                            val = json.loads(val)
                        except (json.JSONDecodeError, TypeError):
                            pass
                    if val is None or val == "":
                        col_type = self.schema.get(key, "JSON").upper()
                        if "LIST" in col_type:
                            val = []
                        else:
                            val = {}
                if not isinstance(val, (list, dict)) and (val == "" or val is None):
                    val = 0
                doc[key] = val
        return Document(doc)

    def _condition_to_sql(self, condition):
        """Translate a Condition / CompoundCondition into (sql_fragment, params_list)."""
        if isinstance(condition, CompoundCondition):
            parts = []
            params = []
            for c in condition.conditions:
                sql, p = self._single_condition_to_sql(c)
                parts.append(sql)
                params.extend(p)
            return "(" + " AND ".join(parts) + ")", params
        elif isinstance(condition, Condition):
            sql, p = self._single_condition_to_sql(condition)
            return sql, p
        else:
            raise TypeError(f"Unsupported condition type: {type(condition)}")

    def _single_condition_to_sql(self, condition):
        """Translate a single Condition to SQL."""
        col = condition.field
        op = condition.op
        if self._is_legacy:
            if op == "!=":
                sql = (f"(json_extract(data, '$.{col}') IS NULL "
                       f"OR json_extract(data, '$.{col}') != ?)")
            else:
                sql = f"json_extract(data, '$.{col}') {op} ?"
        else:
            if op == "!=":
                sql = f'("{col}" != ? OR "{col}" IS NULL)'
            else:
                sql = f'"{col}" {op} ?'
        return sql, [condition.value]

    def _serialize_doc(self, doc):
        """Convert a dict to DB-ready form. Auto-adds columns for unknown keys."""
        if self._is_legacy:
            doc_copy = dict(doc)
            doc_copy.pop("doc_id", None)
            doc_copy.pop("pin", None)  # PIN belongs in paseli table
            return json.dumps(doc_copy, ensure_ascii=False)
        else:
            out = {}
            for k, v in doc.items():
                if k == "doc_id":
                    continue
                if k == "pin":
                    continue  # PIN belongs in paseli table, never in game profiles
                if k not in self.schema:
                    # Auto-add column: infer type from value
                    if isinstance(v, bool) or isinstance(v, int):
                        col_type = "INTEGER DEFAULT 0"
                    elif isinstance(v, float):
                        col_type = "REAL DEFAULT 0.0"
                    elif isinstance(v, (list, dict)):
                        col_type = "JSON"
                        self._json_cols.add(k)
                    else:
                        col_type = "INTEGER DEFAULT 0"  # default to int for safety
                    self.schema[k] = col_type
                    try:
                        self.conn.execute(
                            f'ALTER TABLE "{self.table_name}" ADD COLUMN "{k}" {col_type}'
                        )
                        self.conn.commit()
                    except Exception:
                        pass  # column might already exist
                if k in self._json_cols and not isinstance(v, str):
                    out[k] = json.dumps(v, ensure_ascii=False)
                else:
                    out[k] = v
            return out

    def _cols_for_insert(self):
        """Return the column list for INSERT statements."""
        if self._is_legacy:
            return ["data"]
        else:
            return [f'"{col}"' for col in self.schema.keys()]

    # -- iteration -------------------------------------------------------------

    def __iter__(self):
        return iter(self.all())

    def __len__(self):
        if self._is_legacy:
            row = self.conn.execute(
                f'SELECT COUNT(*) as cnt FROM "{self.table_name}"'
            ).fetchone()
        else:
            row = self.conn.execute(
                f'SELECT COUNT(*) as cnt FROM "{self.table_name}"'
            ).fetchone()
        return row["cnt"]

    # -- public API ------------------------------------------------------------

    def all(self):
        rows = self.conn.execute(
            f'SELECT * FROM "{self.table_name}" ORDER BY 1'
        ).fetchall()
        return [self._row_to_doc(r) for r in rows]

    def get(self, condition=None, doc_id=None):
        if doc_id is not None:
            col = "doc_id" if not self._is_legacy else "doc_id"
            row = self.conn.execute(
                f'SELECT * FROM "{self.table_name}" WHERE {col} = ?',
                (doc_id,)
            ).fetchone()
        elif condition is not None:
            where_sql, params = self._condition_to_sql(condition)
            row = self.conn.execute(
                f'SELECT * FROM "{self.table_name}" WHERE {where_sql} ORDER BY 1 LIMIT 1',
                params
            ).fetchone()
        else:
            return None
        return self._row_to_doc(row) if row else None

    def search(self, condition):
        where_sql, params = self._condition_to_sql(condition)
        rows = self.conn.execute(
            f'SELECT * FROM "{self.table_name}" WHERE {where_sql} ORDER BY 1',
            params
        ).fetchall()
        return [self._row_to_doc(r) for r in rows]

    def insert(self, document):
        serialized = self._serialize_doc(document)
        if self._is_legacy:
            cursor = self.conn.execute(
                f'INSERT INTO "{self.table_name}" (data) VALUES (?)',
                (serialized,)
            )
        else:
            # Don't insert explicit NULL/0 doc_id — let autoincrement handle it
            serialized.pop("doc_id", None)
            if not serialized:
                raise ValueError(f"Cannot insert empty document into '{self.table_name}'")
            cols = [f'"{k}"' for k in serialized.keys()]
            placeholders = ", ".join("?" for _ in serialized)
            cursor = self.conn.execute(
                f'INSERT INTO "{self.table_name}" ({", ".join(cols)}) VALUES ({placeholders})',
                list(serialized.values())
            )
        self.conn.commit()
        return cursor.lastrowid

    def upsert(self, document, condition):
        existing = self.get(condition)
        serialized = self._serialize_doc(document)

        if existing:
            if self._is_legacy:
                self.conn.execute(
                    f'UPDATE "{self.table_name}" SET data = ? WHERE doc_id = ?',
                    (serialized, existing["doc_id"])
                )
            else:
                set_clause = ", ".join(f'"{k}" = ?' for k in serialized.keys())
                where_sql, where_params = self._condition_to_sql(condition)
                self.conn.execute(
                    f'UPDATE "{self.table_name}" SET {set_clause} WHERE {where_sql}',
                    list(serialized.values()) + where_params
                )
        else:
            if self._is_legacy:
                self.conn.execute(
                    f'INSERT INTO "{self.table_name}" (data) VALUES (?)',
                    (serialized,)
                )
            else:
                serialized.pop("doc_id", None)
                if not serialized:
                    raise ValueError(f"Cannot upsert empty document into '{self.table_name}'")
                cols = [f'"{k}"' for k in serialized.keys()]
                placeholders = ", ".join("?" for _ in serialized)
                self.conn.execute(
                    f'INSERT INTO "{self.table_name}" ({", ".join(cols)}) VALUES ({placeholders})',
                    list(serialized.values())
                )
        self.conn.commit()

    def remove(self, condition):
        where_sql, params = self._condition_to_sql(condition)
        self.conn.execute(
            f'DELETE FROM "{self.table_name}" WHERE {where_sql}',
            params
        )
        self.conn.commit()


# =============================================================================
# SQLiteDB — top-level database handle
# =============================================================================

class SQLiteDB:
    def __init__(self, db_path="db.sqlite3"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False, timeout=10)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.conn.execute("PRAGMA wal_autocheckpoint=1000")
        self._lock = threading.Lock()

    def table(self, name, schema=None):
        """Get a TableProxy. Schema is auto-detected from modules.core.schema if not provided."""
        if schema is None:
            try:
                from modules.core.schema import get_schema
                schema = get_schema(name)
            except Exception:
                schema = None
        return TableProxy(self.conn, name, schema)

    def drop_table(self, name):
        self.conn.execute(f'DROP TABLE IF EXISTS "{name}"')
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()


# =============================================================================
# Singleton
# =============================================================================

_db_instance = None


def get_db():
    """Return the singleton SQLiteDB instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = SQLiteDB("db.sqlite3")
    return _db_instance
