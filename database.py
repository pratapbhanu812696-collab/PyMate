"""
database.py
Handles chat history persistence using SQLite.
Each conversation is tied to a session_id so multiple users don't mix history.
"""

import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "chat_history.db"


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Create the messages table if it doesn't already exist."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                intent TEXT,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_message(session_id: str, role: str, content: str, intent: str = None):
    """Save a single chat message to the database."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO messages (session_id, role, content, intent, timestamp) VALUES (?, ?, ?, ?, ?)",
            (session_id, role, content, intent, datetime.now().isoformat()),
        )
        conn.commit()


def get_history(session_id: str, limit: int = 50):
    """Retrieve recent chat history for a given session, oldest first."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT role, content, timestamp FROM messages "
            "WHERE session_id = ? ORDER BY id DESC LIMIT ?",
            (session_id, limit),
        )
        rows = cursor.fetchall()
        return list(reversed(rows))  # oldest first


def get_intent_stats():
    """Return count of how many times each intent was triggered — useful for an analytics view."""
    with get_connection() as conn:
        cursor = conn.execute(
            "SELECT intent, COUNT(*) as count FROM messages "
            "WHERE intent IS NOT NULL GROUP BY intent ORDER BY count DESC"
        )
        return cursor.fetchall()
