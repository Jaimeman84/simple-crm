import sqlite3
from typing import List, Optional
from ..models.prospect import Prospect
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path: str = "crm.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prospects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    email TEXT NOT NULL,
                    status TEXT NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP,
                    updated_at TIMESTAMP
                )
            ''')
            conn.commit()

    def add_prospect(self, prospect: Prospect) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO prospects (full_name, phone_number, email, status, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                prospect.full_name,
                prospect.phone_number,
                prospect.email,
                prospect.status,
                prospect.notes,
                datetime.now(),
                datetime.now()
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_prospects(self) -> List[Prospect]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM prospects')
            rows = cursor.fetchall()
            prospects = []
            for row in rows:
                row_dict = dict(row)
                # Convert timestamp strings to datetime objects
                row_dict['created_at'] = datetime.strptime(row_dict['created_at'], '%Y-%m-%d %H:%M:%S.%f')
                row_dict['updated_at'] = datetime.strptime(row_dict['updated_at'], '%Y-%m-%d %H:%M:%S.%f')
                prospects.append(Prospect(**row_dict))
            return prospects

    def update_prospect(self, prospect: Prospect) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE prospects 
                SET full_name=?, phone_number=?, email=?, status=?, notes=?, updated_at=?
                WHERE id=?
            ''', (
                prospect.full_name,
                prospect.phone_number,
                prospect.email,
                prospect.status,
                prospect.notes,
                datetime.now(),
                prospect.id
            ))
            conn.commit()
            return cursor.rowcount > 0

    def delete_prospect(self, prospect_id: int) -> bool:
        """Delete a prospect from the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM prospects WHERE id = ?', (prospect_id,))
            conn.commit()
            return cursor.rowcount > 0

    def check_duplicate_email(self, email: str) -> bool:
        """Check if a prospect with the given email already exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM prospects WHERE email = ?', (email,))
            count = cursor.fetchone()[0]
            return count > 0 