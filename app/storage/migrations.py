from app.storage.db import get_conn


def _column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table});").fetchall()
    cols = {r[1] for r in rows}  # (cid, name, type, notnull, dflt_value, pk)
    return column in cols


def _add_column_if_missing(conn, table: str, column: str, ddl: str) -> None:
    if not _column_exists(conn, table, column):
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl};")


def run_migrations() -> None:
    with get_conn() as conn:
        # --- core tables ---
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY,
          interface_lang TEXT NOT NULL DEFAULT 'ru',
          target_lang TEXT DEFAULT NULL,
          level TEXT DEFAULT NULL,
          style TEXT DEFAULT NULL,
          dub_interface_for_low_levels INTEGER NOT NULL DEFAULT 0,
          input_mode TEXT NOT NULL DEFAULT 'text',          -- text|voice
          task_mode TEXT NOT NULL DEFAULT 'chat',           -- chat|translator
          translator_direction TEXT NOT NULL DEFAULT 'ui_to_target', -- ui_to_target|target_to_ui
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        """)

        # ✅ add missing translator prefs for existing DBs (safe)
        _add_column_if_missing(conn, "users", "translator_style", "translator_style TEXT NOT NULL DEFAULT 'casual'")   # casual|business
        _add_column_if_missing(conn, "users", "translator_output", "translator_output TEXT NOT NULL DEFAULT 'text'")  # text|voice

        conn.execute("""
        CREATE TABLE IF NOT EXISTS onboarding (
          user_id INTEGER PRIMARY KEY,
          stage TEXT NOT NULL DEFAULT 'interface_lang',
          completed INTEGER NOT NULL DEFAULT 0,
          started_at TEXT NOT NULL,
          completed_at TEXT DEFAULT NULL,
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS access_state (
          user_id INTEGER PRIMARY KEY,
          access_type TEXT NOT NULL DEFAULT 'free',  -- free|friend|premium|...
          valid_until TEXT DEFAULT NULL,
          allowed_languages TEXT DEFAULT NULL,        -- JSON array as TEXT
          updated_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS promo_activations (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          code TEXT NOT NULL,
          activated_at TEXT NOT NULL,
          status TEXT NOT NULL,     -- applied|denied
          reason TEXT DEFAULT NULL,
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS usage_counters (
          user_id INTEGER NOT NULL,
          date TEXT NOT NULL,      -- YYYY-MM-DD
          count INTEGER NOT NULL DEFAULT 0,
          PRIMARY KEY(user_id, date),
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          role TEXT NOT NULL,        -- user|assistant
          content TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        # ✅ NEW: separate translator history (does NOT mix with chat)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS translator_messages (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          role TEXT NOT NULL,        -- user|assistant
          content TEXT NOT NULL,
          created_at TEXT NOT NULL,
          FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
        """)

        conn.commit()
