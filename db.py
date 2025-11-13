# db.py
from typing import Optional, List, Dict
import sqlite3
import os
from datetime import datetime

DB_NAME = os.path.join(os.path.dirname(__file__), "usuarios.db")

def get_conn():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    # users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        bio TEXT,
        comuna TEXT,
        created_at TEXT
    )
    """)
    # messages
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
    # notifications
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
    # user_skills
    cur.execute("""
    CREATE TABLE IF NOT EXISTS user_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    conn.commit()
    conn.close()

# --- Users ---
def create_user(nombre: str, email: str, password_hash: str, bio: Optional[str]=None, comuna: Optional[str]=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cur.execute(
            "INSERT INTO users (nombre, email, password_hash, bio, comuna, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, email, password_hash, bio, comuna, created_at)
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

def update_user_profile(user_id: int, nombre: str=None, bio: str=None, comuna: str=None):
    conn = get_conn()
    cur = conn.cursor()
    if nombre is not None:
        cur.execute("UPDATE users SET nombre = ? WHERE id = ?", (nombre, user_id))
    if bio is not None:
        cur.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, user_id))
    if comuna is not None:
        cur.execute("UPDATE users SET comuna = ? WHERE id = ?", (comuna, user_id))
    conn.commit()
    conn.close()

# --- Messages ---
def add_message(emisor_id: int, receptor_id: int, contenido: str):
    conn = get_conn()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO messages (emisor_id, receptor_id, contenido, timestamp) VALUES (?, ?, ?, ?)",
                (emisor_id, receptor_id, contenido, timestamp))
    conn.commit()
    conn.close()

def get_messages_between(user_a: int, user_b: int) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM messages
        WHERE (emisor_id = ? AND receptor_id = ?) OR (emisor_id = ? AND receptor_id = ?)
        ORDER BY id ASC
    """, (user_a, user_b, user_b, user_a))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Notifications ---
def add_notification(usuario_id: int, tipo: str, mensaje: str):
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO notifications (usuario_id, tipo, mensaje, fecha, leido) VALUES (?, ?, ?, ?, ?)",
                (usuario_id, tipo, mensaje, fecha, 0))
    conn.commit()
    conn.close()

def get_notifications(usuario_id: int, only_unread: bool=False):
    conn = get_conn()
    cur = conn.cursor()
    if only_unread:
        cur.execute("SELECT * FROM notifications WHERE usuario_id = ? AND leido = 0 ORDER BY id DESC", (usuario_id,))
    else:
        cur.execute("SELECT * FROM notifications WHERE usuario_id = ? ORDER BY id DESC", (usuario_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def mark_notification_read(notification_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET leido = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()

# --- Skills ---
def add_skill(user_id: int, skill: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO user_skills (user_id, skill) VALUES (?, ?)", (user_id, skill))
    conn.commit()
    conn.close()

def get_user_skills(user_id: int) -> List[str]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT skill FROM user_skills WHERE user_id = ?", (user_id,))
    skills = [r["skill"] for r in cur.fetchall()]
    conn.close()
    return skills

def search_users_by_skill(skill: str) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT u.id, u.nombre, u.bio, u.comuna
        FROM users u
        JOIN user_skills s ON u.id = s.user_id
        WHERE LOWER(s.skill) LIKE LOWER(?)
        GROUP BY u.id
    """, (f"%{skill}%",))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
