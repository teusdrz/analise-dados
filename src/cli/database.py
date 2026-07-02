

import sqlite3
from contextlib import contextmanager
from typing import Generator

from config import DB_PATH

SQL_CREATE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT    NOT NULL,
        email      TEXT    NOT NULL UNIQUE
    );
"""
SQL_CREATE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
      id          INTEGER PRIMARY KEY AUTOINCREMENT,
      title       TEXT NOT NULL,
      description TEXT NOT NULL DEFAULT '',
      status      TEXT NOT NULL DEFAULT 'todo',
      created_at  TEXT NOT NULL,
      user_id     INTEGER NOT NULL,
      FOREIGN KEY (user_id) REFERENCES users (id)
    );
"""

@contextmanager
def get_connection(db_path=DB_PATH) -> Generator[sqlite3.Connection, None, None]:

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  
    conn.execute("PRAGMA foreign_keys = ON")  
    try:
        yield conn        
        conn.commit()      
    except Exception:
        conn.rollback()     
        raise              
    finally:
        conn.close()        


def create_tables(db_path=DB_PATH) -> None:

    with get_connection(db_path) as conn:
        conn.execute(SQL_CREATE_USERS)
        conn.execute(SQL_CREATE_TASKS)
