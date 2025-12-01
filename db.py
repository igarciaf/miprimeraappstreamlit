# db.py — Módulo de base de datos para ConectaServicios
# (EN PRESENTACIÓN) Aquí se manejan TODOS los datos de la app: usuarios, servicios,
# chats, trabajos, evaluaciones y notificaciones.

from typing import Optional, List, Dict
import sqlite3
import os
from datetime import datetime

# Ruta del archivo SQLite
DB_FILENAME = os.path.join(os.path.dirname(__file__), "conecta.db")

# -----------------------------
# CONEXIÓN A BASE DE DATOS
# -----------------------------
def get_conn():
    """Devuelve una conexión a SQLite con filas accesibles como diccionarios."""
    conn = sqlite3.connect(DB_FILENAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREACIÓN DE TABLAS
# -----------------------------
def init_db():
    """
    (EN PRESENTACIÓN) Esta función se ejecuta una sola vez.
    Crea todas las tablas necesarias para que la app funcione.
    """
    conn = get_conn()
    cur = conn.cursor()

    # Tabla de usuarios
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

    # Tabla de servicios
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

    # Tabla de mensajes del chat
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

    # Tabla de notificaciones
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

    # Tabla de trabajos (solicitudes entre usuarios)
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

    # Tabla de evaluaciones
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

    conn.commit()
    conn.close()


# ================================================================
# USUARIOS
# ================================================================
def create_user(nombre: str, email: str, password_hash: str,
                bio: Optional[str] = None, comuna: Optional[str] = None) -> int:
    """Registra un nuevo usuario."""
    conn = get_conn()
    cur = conn.cursor()
    created = datetime.utcnow().isoformat()

    try:
        cur.execute("""
            INSERT INTO users (nombre, email, password_hash, bio, comuna, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, email, password_hash, bio, comuna, created))
        conn.commit()
        uid = cur.lastrowid
    except sqlite3.IntegrityError:
        uid = 0

    conn.close()
    return uid


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


def update_user_profile(user_id: int, nombre: str=None,
                        bio: str=None, comuna: str=None):
    """Actualiza información del perfil del usuario."""
    conn = get_conn()
    cur = conn.cursor()
    if nombre:
        cur.execute("UPDATE users SET nombre = ? WHERE id = ?", (nombre, user_id))
    if bio:
        cur.execute("UPDATE users SET bio = ? WHERE id = ?", (bio, user_id))
    if comuna:
        cur.execute("UPDATE users SET comuna = ? WHERE id = ?", (comuna, user_id))
    conn.commit()
    conn.close()


# ================================================================
# SERVICIOS
# ================================================================
def add_service(user_id: int, category: str, service: str,
                comunas: Optional[str] = None, price: Optional[float] = None) -> int:
    """Publica un nuevo servicio."""
    conn = get_conn()
    cur = conn.cursor()
    created = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO services (user_id, category, service, comunas, price, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, category, service, comunas, price, created))

    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def get_user_services(user_id: int) -> List[Dict]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services WHERE user_id = ? ORDER BY id DESC", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_services_filtered(term: str, comuna: Optional[str] = None) -> List[Dict]:
    """
    (EN PRESENTACIÓN)
    Esta consulta une tabla de servicios con la tabla de usuarios
    para mostrar nombre, bio y comuna del proveedor.
    """
    conn = get_conn()
    cur = conn.cursor()

    term_like = f"%{term}%"

    if comuna:
        comuna_like = f"%{comuna}%"
        cur.execute("""
            SELECT s.*, u.nombre AS user_nombre, u.comuna AS user_comuna,
                   u.bio AS user_bio, s.user_id AS user_id
            FROM services s
            JOIN users u ON s.user_id = u.id
            WHERE (LOWER(s.service) LIKE LOWER(?) OR LOWER(s.category) LIKE LOWER(?))
              AND (s.comunas LIKE ? OR u.comuna LIKE ?)
            ORDER BY s.id DESC
        """, (term_like, term_like, comuna_like, comuna_like))
    else:
        cur.execute("""
            SELECT s.*, u.nombre AS user_nombre, u.comuna AS user_comuna,
                   u.bio AS user_bio, s.user_id AS user_id
            FROM services s
            JOIN users u ON s.user_id = u.id
            WHERE (LOWER(s.service) LIKE LOWER(?) OR LOWER(s.category) LIKE LOWER(?))
            ORDER BY s.id DESC
        """, (term_like, term_like))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ================================================================
# MENSAJES (CHAT)
# ================================================================
def add_message(emisor_id: int, receptor_id: int, contenido: str):
    """Guarda un mensaje nuevo."""
    conn = get_conn()
    cur = conn.cursor()
    timestamp = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO messages (emisor_id, receptor_id, contenido, timestamp)
        VALUES (?, ?, ?, ?)
    """, (emisor_id, receptor_id, contenido, timestamp))

    conn.commit()
    conn.close()


def get_messages_between(user_a: int, user_b: int) -> List[Dict]:
    """Obtiene el historial entre dos usuarios."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM messages
        WHERE (emisor_id = ? AND receptor_id = ?)
           OR (emisor_id = ? AND receptor_id = ?)
        ORDER BY id ASC
    """, (user_a, user_b, user_b, user_a))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recent_chats(user_id: int) -> List[Dict]:
    """
    (EN PRESENTACIÓN)
    Devuelve una lista de conversaciones recientes,
    cada una con:
      - nombre del otro usuario
      - último mensaje
      - hora
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, emisor_id, receptor_id, contenido, timestamp
        FROM messages
        WHERE emisor_id = ? OR receptor_id = ?
        ORDER BY timestamp DESC
    """, (user_id, user_id))

    messages = cur.fetchall()

    chats = {}
    for msg in messages:
        msg = dict(msg)
        other = msg["receptor_id"] if msg["emisor_id"] == user_id else msg["emisor_id"]

        if other not in chats:
            chats[other] = {
                "other_user_id": other,
                "last_message": msg["contenido"],
                "last_timestamp": msg["timestamp"]
            }

    result = []
    for oid, chat in chats.items():
        cur.execute("SELECT nombre FROM users WHERE id = ?", (oid,))
        name = cur.fetchone()
        if name:
            chat["other_user_name"] = name["nombre"]
            result.append(chat)

    conn.close()
    return result


# ================================================================
# NOTIFICACIONES
# ================================================================
def add_notification(usuario_id: int, tipo: str, mensaje: str):
    """Crea una notificación para un usuario."""
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO notifications (usuario_id, tipo, mensaje, fecha, leido)
        VALUES (?, ?, ?, ?, 0)
    """, (usuario_id, tipo, mensaje, fecha))

    conn.commit()
    conn.close()


def get_notifications(usuario_id: int, only_unread=False):
    """Obtiene notificaciones de un usuario."""
    conn = get_conn()
    cur = conn.cursor()

    if only_unread:
        cur.execute("""
            SELECT * FROM notifications
            WHERE usuario_id = ? AND leido = 0
            ORDER BY id DESC
        """, (usuario_id,))
    else:
        cur.execute("""
            SELECT * FROM notifications
            WHERE usuario_id = ?
            ORDER BY id DESC
        """, (usuario_id,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_notification_read(notification_id: int):
    """Marca una notificación como leída."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE notifications SET leido = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()


# ================================================================
# TRABAJOS (SOLICITUDES)
# ================================================================
def create_trabajo(service_id: int, cliente_id: int, trabajador_id: int,
                   fecha_solicitada: str, hora_solicitada: str,
                   direccion: str, descripcion: str,
                   precio_propuesto: Optional[float]) -> int:
    """Crea un nuevo trabajo pendiente."""
    conn = get_conn()
    cur = conn.cursor()
    created = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO trabajos (
            service_id, cliente_id, trabajador_id, estado,
            fecha_solicitada, hora_solicitada, direccion, descripcion,
            precio_propuesto, fecha_creacion
        )
        VALUES (?, ?, ?, 'pendiente', ?, ?, ?, ?, ?, ?)
    """, (service_id, cliente_id, trabajador_id,
          fecha_solicitada, hora_solicitada, direccion, descripcion,
          precio_propuesto, created))

    conn.commit()
    tid = cur.lastrowid
    conn.close()
    return tid


def get_trabajo_by_id(trabajo_id: int):
    """Obtiene información completa de un trabajo."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.*,
               s.service AS servicio_nombre,
               c.nombre AS cliente_nombre,
               tr.nombre AS trabajador_nombre
        FROM trabajos t
        JOIN services s ON t.service_id = s.id
        JOIN users c ON t.cliente_id = c.id
        JOIN users tr ON t.trabajador_id = tr.id
        WHERE t.id = ?
    """, (trabajo_id,))

    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_trabajos_cliente(cliente_id: int) -> List[Dict]:
    """Muestra los trabajos solicitados por un cliente."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.*, s.service AS servicio_nombre, u.nombre AS trabajador_nombre
        FROM trabajos t
        JOIN services s ON t.service_id = s.id
        JOIN users u ON t.trabajador_id = u.id
        WHERE t.cliente_id = ?
        ORDER BY fecha_creacion DESC
    """, (cliente_id,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_trabajos_trabajador(trabajador_id: int) -> List[Dict]:
    """Muestra los trabajos que recibió el trabajador."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT t.*, s.service AS servicio_nombre, u.nombre AS cliente_nombre
        FROM trabajos t
        JOIN services s ON t.service_id = s.id
        JOIN users u ON t.cliente_id = u.id
        WHERE t.trabajador_id = ?
        ORDER BY fecha_creacion DESC
    """, (trabajador_id,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_trabajo_estado(trabajo_id: int, nuevo_estado: str,
                          precio_final: Optional[float] = None,
                          comentario_trabajador: Optional[str] = None):
    """Actualiza el estado del trabajo (aceptado, completado, etc)."""
    conn = get_conn()
    cur = conn.cursor()

    if nuevo_estado == "aceptado":
        cur.execute("""
            UPDATE trabajos
            SET estado = ?, fecha_aceptacion = ?
            WHERE id = ?
        """, (nuevo_estado, datetime.utcnow().isoformat(), trabajo_id))

    elif nuevo_estado == "completado":
        cur.execute("""
            UPDATE trabajos
            SET estado = ?, fecha_completado = ?, precio_final = ?, comentario_trabajador = ?
            WHERE id = ?
        """, (nuevo_estado, datetime.utcnow().isoformat(),
              precio_final, comentario_trabajador, trabajo_id))

    else:
        cur.execute("UPDATE trabajos SET estado = ? WHERE id = ?", (nuevo_estado, trabajo_id))

    conn.commit()
    conn.close()


# ================================================================
# EVALUACIONES
# ================================================================
def create_evaluacion(trabajo_id: int, cliente_id: int, trabajador_id: int,
                      calificacion: int, comentario: str,
                      puntualidad: int, calidad: int,
                      comunicacion: int, recomendaria: int):
    """Guarda la evaluación de un trabajo."""
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()

    cur.execute("""
        INSERT INTO evaluaciones (
            trabajo_id, cliente_id, trabajador_id, calificacion,
            comentario, puntualidad, calidad, comunicacion,
            recomendaria, fecha
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (trabajo_id, cliente_id, trabajador_id, calificacion,
          comentario, puntualidad, calidad, comunicacion,
          recomendaria, fecha))

    # Cambiar estado del trabajo
    cur.execute("UPDATE trabajos SET estado = 'evaluado' WHERE id = ?", (trabajo_id,))

    conn.commit()
    conn.close()


def get_evaluaciones_trabajador(trabajador_id: int) -> List[Dict]:
    """Devuelve todas las evaluaciones hechas a un trabajador."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT e.*, u.nombre AS cliente_nombre, s.service AS servicio_nombre
        FROM evaluaciones e
        JOIN users u ON e.cliente_id = u.id
        JOIN trabajos t ON e.trabajo_id = t.id
        JOIN services s ON t.service_id = s.id
        WHERE e.trabajador_id = ?
        ORDER BY e.fecha DESC
    """, (trabajador_id,))

    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_promedio_calificacion(trabajador_id: int) -> float:
    """Promedio general del trabajador."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT AVG(calificacion) AS promedio
        FROM evaluaciones
        WHERE trabajador_id = ?
    """, (trabajador_id,))

    row = cur.fetchone()
    conn.close()
    return round(row["promedio"], 1) if row and row["promedio"] else 0.0


def get_estadisticas_trabajador(trabajador_id: int) -> Dict:
    """Devuelve resumen estadístico del trabajador."""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM trabajos
        WHERE trabajador_id = ? AND estado IN ('completado','evaluado')
    """, (trabajador_id,))
    completados = cur.fetchone()["total"]

    cur.execute("""
        SELECT COUNT(*) AS total
        FROM evaluaciones
        WHERE trabajador_id = ?
    """, (trabajador_id,))
    evaluaciones = cur.fetchone()["total"]

    promedio = get_promedio_calificacion(trabajador_id)

    cur.execute("""
        SELECT AVG(puntualidad) AS p, AVG(calidad) AS c,
               AVG(comunicacion) AS co, SUM(recomendaria) AS r
        FROM evaluaciones
        WHERE trabajador_id = ?
    """, (trabajador_id,))

    stats = cur.fetchone()
    conn.close()

    return {
        "trabajos_completados": completados,
        "total_evaluaciones": evaluaciones,
        "promedio_general": promedio,
        "puntualidad": round(stats["p"], 1) if stats["p"] else 0,
        "calidad": round(stats["c"], 1) if stats["c"] else 0,
        "comunicacion": round(stats["co"], 1) if stats["co"] else 0,
        "recomendaciones": stats["r"] or 0
    }
