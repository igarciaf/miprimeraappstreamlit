# db.py
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
    # users: id autoincrement, nombre, email unico, password_hash, bio, comuna, created_at
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
    # messages: id, emisor_id, receptor_id, contenido, timestamp
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
    # notifications: id, usuario_id, tipo, mensaje, fecha, leido(0/1)
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

# --- Users helpers ---
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

# --- Messages helpers ---
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

# --- Notifications helpers ---
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
