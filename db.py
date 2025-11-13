import sqlite3
from typing import Optional, List, Dict
import os
from datetime import datetime

DB_FILENAME = os.path.join(os.path.dirname(__file__), "conecta.db")

def get_conn():
    conn = sqlite3.connect(DB_FILENAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        bio TEXT,
        comuna TEXT,
        servicios TEXT,
        created_at TEXT
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emisor_id INTEGER NOT NULL,
        receptor_id INTEGER NOT NULL,
        contenido TEXT NOT NULL,
        timestamp TEXT,
        FOREIGN KEY (emisor_id) REFERENCES users(id),
        FOREIGN KEY (receptor_id) REFERENCES users(id)
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        tipo TEXT,
        mensaje TEXT,
        fecha TEXT,
        leido INTEGER DEFAULT 0,
        FOREIGN KEY (usuario_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

def create_user(nombre: str, email: str, password_hash: str, bio: Optional[str]=None, comuna: Optional[str]=None, servicios: Optional[str]=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cur.execute(
            "INSERT INTO users (nombre, email, password_hash, bio, comuna, servicios, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (nombre, email, password_hash, bio, comuna, servicios, created_at)
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        user_id = 0
    conn.close()
    return user_id

def get_user_by_email(email: str) -> Optional[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_profile(user_id: int, nombre: str=None, bio: str=None, comuna: str=None, servicios: str=None):
    conn = get_conn()
    cur = conn.cursor()
    if nombre is not None:
        cur.execute("UPDATE users SET nombre = ? WHERE id = ?", (nombre, user_id))
    if bio is not None:
        cur.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, user_id))
    if comuna is not None:
        cur.execute("UPDATE users SET comuna = ? WHERE id = ?", (comuna, user_id))
    if servicios is not None:
        cur.execute("UPDATE users SET servicios = ? WHERE id = ?", (servicios, user_id))
    conn.commit()
    conn.close()

def search_users_by_service(service_query: str) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    like_query = f"%{service_query.lower()}%"
    cur.execute("SELECT * FROM users WHERE LOWER(servicios) LIKE ?", (like_query,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
