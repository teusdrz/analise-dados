

import sqlite3
from typing import Optional

from .database import get_connection
from .models import Task, TaskStatus
from .config import DB_PATH

 
class TaskRepository:
   

    def __init__(self, db_path=DB_PATH) -> None:
        self.db_path = db_path


    def create(self, task: Task) -> Task:
    
        sql = """
            INSERT INTO tasks (title, description, status, created_at, user_id)
            VALUES (?, ?, ?, ?, ?)
        """
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(sql, (
                task.title,
                task.description,
                task.status.value,          
                task.created_at.isoformat(),
                task.user_id,
            ))
            task.id = cursor.lastrowid    
        return task

   
    def find_all(self) -> list[Task]:
      
        sql = "SELECT * FROM tasks ORDER BY created_at DESC"
        with get_connection(self.db_path) as conn:
            rows = conn.execute(sql).fetchall()

        return [self._row_to_task(row) for row in rows]

 
    def find_by_id(self, task_id: int) -> Optional[Task]:
        
        sql = "SELECT * FROM tasks WHERE id = ?"
        with get_connection(self.db_path) as conn:
            row = conn.execute(sql, (task_id,)).fetchone()
       
        return self._row_to_task(row) if row else None

  
    def find_by_status(self, status: TaskStatus) -> list[Task]:
   
        sql = "SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC"
        with get_connection(self.db_path) as conn:
            rows = conn.execute(sql, (status.value,)).fetchall()
        return [self._row_to_task(row) for row in rows]

   
    def update(self, task: Task) -> bool:
   
        sql = """
            UPDATE tasks
            SET title = ?, description = ?, status = ?
            WHERE id = ?
        """
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(sql, (
                task.title,
                task.description,
                task.status.value,
                task.id,
            ))
        return cursor.rowcount > 0  

    
    def delete(self, task_id: int) -> bool:

        sql = "DELETE FROM tasks WHERE id = ?"
        with get_connection(self.db_path) as conn:
            cursor = conn.execute(sql, (task_id,))
        return cursor.rowcount > 0

   
    def count(self) -> int:
        
        sql = "SELECT COUNT(*) FROM tasks"
        with get_connection(self.db_path) as conn:
        
            result = conn.execute(sql).fetchone()
        return result[0] if result else 0

    def count_by_status(self) -> dict[str, int]:
    
        sql = "SELECT status, COUNT(*) as total FROM tasks GROUP BY status"
        with get_connection(self.db_path) as conn:
            rows = conn.execute(sql).fetchall()

        return {row["status"]: row["total"] for row in rows}


    def _row_to_task(self, row: sqlite3.Row) -> Task:

        from datetime import datetime
        return Task(
           id          = row["id"],
        title       = row["title"],
        description = row["description"],
        status      = TaskStatus(row["status"]),
        created_at  = datetime.fromisoformat(row["created_at"]),
        user_id     = row["user_id"],
        )
