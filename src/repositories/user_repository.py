import sqlite3
from typing import Optional

from ..database import get_connection
from ..domain.models import User
from ..config import DB_PATH
class UserRepository:
    
    def __init__ (self, db_path=DB_PATH) -> None:
        self.db_path = db_path
        
    def create(self, user: User) -> User:
        sql = """
            INSERT INTO users (name, email)
            VALUES (?, ?)
        """
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(sql, (user.name, user.email))
            user.id = cursor.lastrowid
        return user
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        sql = "SELECT * FROM users WHERE id = ?"
        with get_connection(self.db_path) as conn:
            row = conn.execute(sql, (user_id,)).fetchone()
            return self._row_to_user(row) if row else None
        
    def find_by_email(self, email: str) -> Optional[User]:
        sql = "SELECT * FROM users WHERE email = ?"
        with get_connection(self.db_path) as conn:
            row = conn.execute(sql, (email,)).fetchone()
        return self._row_to_user(row) if row else None

        
    def find_all(self) -> list[User]:
            sql = "SELECT * FROM users ORDER BY id"
            with get_connection(self.db_path) as conn:
                rows = conn.execute(sql).fetchall()
                return [self._row_to_user(row) for row in rows]
     
    def _row_to_user(self, row: sqlite3.Row) -> User:
         return User(
             id=row["id"],
             name=row["name"],
             email=row["email"]
         )
        