import sqlite3
import json
from pathlib import Path

DB_PATH = Path("memory.db")

class MemoryStore:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS memory (
                user_id TEXT PRIMARY KEY,
                data TEXT
            )
        """)
        self.conn.commit()

    def get(self, user_id: str) -> dict:
        cursor = self.conn.execute(
            "SELECT data FROM memory WHERE user_id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return json.loads(row[0])
        return {}

    def set(self, user_id: str, data: dict):
        self.conn.execute(
            "INSERT OR REPLACE INTO memory (user_id, data) VALUES (?, ?)",
            (user_id, json.dumps(data))
        )
        self.conn.commit()

memory_store = MemoryStore()
