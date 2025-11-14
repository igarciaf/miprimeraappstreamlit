# db.py
from typing import Optional, List, Dict
import sqlite3
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
    # services (publicaciones)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        service TEXT NOT NULL,
        comuna TEXT,
        price REAL,
        created_at TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
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
    if not user_id:
        return None
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

# --- Services ---
def add_service(user_id: int, category: str, service: str, comuna: Optional[str]=None, price: Optional[float]=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    cur.execute(
        "INSERT INTO services (user_id, category, service, comuna, price, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (user_id, category, service, comuna, price, created_at)
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid

def get_user_services(user_id: int) -> List[Dict]:
    if not user_id:
        return []
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_services_filtered(term: str, comuna: Optional[str]=None) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    term_like = f"%{term}%"
    if comuna:
        cur.execute("""
            SELECT s.*, u.nombre as user_nombre, u.comuna as user_comuna, u.bio as user_bio
            FROM services s
            JOIN users u ON s.user_id = u.id
            WHERE (LOWER(s.service) LIKE LOWER(?) OR LOWER(s.category) LIKE LOWER(?))
              AND (s.comuna = ?)
            ORDER BY s.id DESC
        """, (term_like, term_like, comuna))
    else:
        cur.execute("""
            SELECT s.*, u.nombre as user_nombre, u.comuna as user_comuna, u.bio as user_bio
            FROM services s
            JOIN users u ON s.user_id = u.id
            WHERE (LOWER(s.service) LIKE LOWER(?) OR LOWER(s.category) LIKE LOWER(?))
            ORDER BY s.id DESC
        """, (term_like, term_like))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# --- Messages ---
def add_message(emisor_id: int, receptor_id: int, contenido: str):
    if not emisor_id or not receptor_id:
        return
    conn = get_conn()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO messages (emisor_id, receptor_id, contenido, timestamp) VALUES (?, ?, ?, ?)",
                (emisor_id, receptor_id, contenido, timestamp))
    conn.commit()
    conn.close()

def get_messages_between(user_a: int, user_b: int) -> List[Dict]:
    if not user_a or not user_b:
        return []
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
    if not usuario_id:
        return
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO notifications (usuario_id, tipo, mensaje, fecha, leido) VALUES (?, ?, ?, ?, ?)",
                (usuario_id, tipo, mensaje, fecha, 0))
    conn.commit()
    conn.close()

def get_notifications(usuario_id: int, only_unread: bool=False):
    if not usuario_id:
        return []
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

def get_recent_chats(user_id: int) -> List[Dict]:
    """Obtiene lista de chats recientes con el último mensaje"""
    if not user_id:
        return []
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT
            CASE 
                WHEN m.emisor_id = ? THEN m.receptor_id
                ELSE m.emisor_id
            END as other_user_id,
            u.nombre as other_user_name,
            m.contenido as last_message,
            m.timestamp as last_timestamp,
            (SELECT COUNT(*) FROM messages m2 
             WHERE m2.receptor_id = ? 
             AND m2.emisor_id = other_user_id) as unread_count
        FROM messages m
        JOIN users u ON u.id = CASE 
            WHEN m.emisor_id = ? THEN m.receptor_id 
            ELSE m.emisor_id 
        END
        WHERE m.emisor_id = ? OR m.receptor_id = ?
        GROUP BY other_user_id
        ORDER BY m.id DESC
    """, (user_id, user_id, user_id, user_id, user_id))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
