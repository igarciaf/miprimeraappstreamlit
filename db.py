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
        comunas TEXT,
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
    
    # ============ NUEVAS TABLAS ============
    
    # trabajos (solicitudes de servicio)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trabajos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        trabajador_id INTEGER NOT NULL,
        estado TEXT NOT NULL,
        fecha_solicitada TEXT,
        hora_solicitada TEXT,
        direccion TEXT,
        descripcion TEXT,
        precio_propuesto REAL,
        precio_final REAL,
        fecha_creacion TEXT,
        fecha_aceptacion TEXT,
        fecha_completado TEXT,
        comentario_trabajador TEXT,
        FOREIGN KEY (service_id) REFERENCES services(id),
        FOREIGN KEY (cliente_id) REFERENCES users(id),
        FOREIGN KEY (trabajador_id) REFERENCES users(id)
    )
    """)
    
    # evaluaciones
    cur.execute("""
    CREATE TABLE IF NOT EXISTS evaluaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trabajo_id INTEGER NOT NULL,
        cliente_id INTEGER NOT NULL,
        trabajador_id INTEGER NOT NULL,
        calificacion INTEGER NOT NULL,
        comentario TEXT,
        puntualidad INTEGER,
        calidad INTEGER,
        comunicacion INTEGER,
        recomendaria INTEGER,
        fecha TEXT,
        FOREIGN KEY (trabajo_id) REFERENCES trabajos(id),
        FOREIGN KEY (cliente_id) REFERENCES users(id),
        FOREIGN KEY (trabajador_id) REFERENCES users(id)
    )
    """)
    
    # fotos_trabajos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS fotos_trabajos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trabajo_id INTEGER NOT NULL,
        foto_base64 TEXT NOT NULL,
        descripcion TEXT,
        fecha TEXT,
        FOREIGN KEY (trabajo_id) REFERENCES trabajos(id)
    )
    """)
    
    conn.commit()
    conn.close()
