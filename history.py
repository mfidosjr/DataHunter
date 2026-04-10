# history.py
import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "datahunter_history.db")


def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con


def init_db():
    with _conn() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                title     TEXT NOT NULL,
                keywords  TEXT NOT NULL,
                fontes    TEXT NOT NULL,
                n_results INTEGER DEFAULT 0,
                chat      TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def save_search(title: str, keywords: list, fontes: dict, n_results: int, chat: list):
    with _conn() as con:
        con.execute(
            "INSERT INTO searches (title, keywords, fontes, n_results, chat, created_at) VALUES (?,?,?,?,?,?)",
            (
                title,
                json.dumps(keywords, ensure_ascii=False),
                json.dumps(fontes, ensure_ascii=False),
                n_results,
                json.dumps(chat, ensure_ascii=False),
                datetime.now().strftime("%Y-%m-%d %H:%M"),
            ),
        )


def list_searches(limit: int = 30) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM searches ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_search(search_id: int) -> dict | None:
    with _conn() as con:
        row = con.execute("SELECT * FROM searches WHERE id = ?", (search_id,)).fetchone()
    return dict(row) if row else None


def delete_search(search_id: int):
    with _conn() as con:
        con.execute("DELETE FROM searches WHERE id = ?", (search_id,))


def clear_history():
    with _conn() as con:
        con.execute("DELETE FROM searches")


init_db()
