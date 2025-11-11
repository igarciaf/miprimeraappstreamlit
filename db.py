# db.py
from typing import Optional
import sqlite3

# Nombre de la base de datos local
DB_NAME = "usuarios.db"


def init_db():
    """Inicializa la base de datos si no existe"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            bio TEXT,
            comuna TEXT
        )
    """)
    conn.commit()
    conn.close()


def create_user(nombre: str, email: str, password_hash: str, bio: Optional[str] = None, comuna: Optional[str] = None) -> int:
    """Crea un nuevo usuario en la base de datos"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, password_hash, bio, comuna)
        VALUES (?, ?, ?, ?, ?)
    """, (nombre, email, password_hash, bio, comuna))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email: str):
    """Obtiene un usuario por su correo electrónico"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user
