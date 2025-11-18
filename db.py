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
        return user_id
    
    except Exception as e:
        print("Error al crear usuario:", e)
        return -1
    
    finally:
        conn.close()
        
# ============ TRABAJOS ============

def create_trabajo(service_id: int, cliente_id: int, trabajador_id: int, 
                   fecha_solicitada: str, hora_solicitada: str, direccion: str, 
                   descripcion: str, precio_propuesto: Optional[float] = None) -> int:
    """Crear nueva solicitud de trabajo"""
    conn = get_conn()
    cur = conn.cursor()
    fecha_creacion = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO trabajos (service_id, cliente_id, trabajador_id, estado, 
                             fecha_solicitada, hora_solicitada, direccion, descripcion, 
                             precio_propuesto, fecha_creacion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (service_id, cliente_id, trabajador_id, "pendiente", 
          fecha_solicitada, hora_solicitada, direccion, descripcion, 
          precio_propuesto, fecha_creacion))
    conn.commit()
    trabajo_id = cur.lastrowid
    conn.close()
    return trabajo_id

def get_trabajo_by_id(trabajo_id: int) -> Optional[Dict]:
    """Obtener trabajo por ID"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.*, 
               s.service as servicio_nombre,
               s.category as servicio_categoria,
               c.nombre as cliente_nombre,
               c.email as cliente_email,
               tr.nombre as trabajador_nombre,
               tr.email as trabajador_email
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
    """Obtener trabajos solicitados por un cliente"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.*, 
               s.service as servicio_nombre,
               tr.nombre as trabajador_nombre
        FROM trabajos t
        JOIN services s ON t.service_id = s.id
        JOIN users tr ON t.trabajador_id = tr.id
        WHERE t.cliente_id = ?
        ORDER BY t.fecha_creacion DESC
    """, (cliente_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_trabajos_trabajador(trabajador_id: int) -> List[Dict]:
    """Obtener trabajos recibidos por un trabajador"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.*, 
               s.service as servicio_nombre,
               c.nombre as cliente_nombre
        FROM trabajos t
        JOIN services s ON t.service_id = s.id
        JOIN users c ON t.cliente_id = c.id
        WHERE t.trabajador_id = ?
        ORDER BY t.fecha_creacion DESC
    """, (trabajador_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_trabajo_estado(trabajo_id: int, nuevo_estado: str, 
                          precio_final: Optional[float] = None,
                          comentario_trabajador: Optional[str] = None):
    """Actualizar estado del trabajo"""
    conn = get_conn()
    cur = conn.cursor()
    
    if nuevo_estado == "aceptado":
        fecha_aceptacion = datetime.utcnow().isoformat()
        cur.execute("UPDATE trabajos SET estado = ?, fecha_aceptacion = ? WHERE id = ?",
                   (nuevo_estado, fecha_aceptacion, trabajo_id))
    elif nuevo_estado == "completado":
        fecha_completado = datetime.utcnow().isoformat()
        if precio_final is not None:
            cur.execute("""UPDATE trabajos SET estado = ?, fecha_completado = ?, 
                          precio_final = ?, comentario_trabajador = ? WHERE id = ?""",
                       (nuevo_estado, fecha_completado, precio_final, comentario_trabajador, trabajo_id))
        else:
            cur.execute("""UPDATE trabajos SET estado = ?, fecha_completado = ?, 
                          comentario_trabajador = ? WHERE id = ?""",
                       (nuevo_estado, fecha_completado, comentario_trabajador, trabajo_id))
    else:
        cur.execute("UPDATE trabajos SET estado = ? WHERE id = ?", (nuevo_estado, trabajo_id))
    
    conn.commit()
    conn.close()

# ============ EVALUACIONES ============

def create_evaluacion(trabajo_id: int, cliente_id: int, trabajador_id: int,
                     calificacion: int, comentario: str,
                     puntualidad: int, calidad: int, comunicacion: int,
                     recomendaria: int) -> int:
    """Crear evaluación de un trabajo"""
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    cur.execute("""
        INSERT INTO evaluaciones (trabajo_id, cliente_id, trabajador_id, calificacion,
                                 comentario, puntualidad, calidad, comunicacion,
                                 recomendaria, fecha)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (trabajo_id, cliente_id, trabajador_id, calificacion, comentario,
          puntualidad, calidad, comunicacion, recomendaria, fecha))
    conn.commit()
    eval_id = cur.lastrowid
    
    # Actualizar estado del trabajo a "evaluado"
    cur.execute("UPDATE trabajos SET estado = ? WHERE id = ?", ("evaluado", trabajo_id))
    conn.commit()
    conn.close()
    return eval_id

def get_evaluaciones_trabajador(trabajador_id: int) -> List[Dict]:
    """Obtener todas las evaluaciones de un trabajador"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT e.*, c.nombre as cliente_nombre, t.servicio_nombre
        FROM evaluaciones e
        JOIN users c ON e.cliente_id = c.id
        JOIN (
            SELECT tr.id, s.service as servicio_nombre
            FROM trabajos tr
            JOIN services s ON tr.service_id = s.id
        ) t ON e.trabajo_id = t.id
        WHERE e.trabajador_id = ?
        ORDER BY e.fecha DESC
    """, (trabajador_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_promedio_calificacion(trabajador_id: int) -> float:
    """Obtener promedio de calificaciones de un trabajador"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT AVG(calificacion) as promedio
        FROM evaluaciones
        WHERE trabajador_id = ?
    """, (trabajador_id,))
    row = cur.fetchone()
    conn.close()
    return round(row['promedio'], 1) if row and row['promedio'] else 0.0

def get_estadisticas_trabajador(trabajador_id: int) -> Dict:
    """Obtener estadísticas del trabajador"""
    conn = get_conn()
    cur = conn.cursor()
    
    # Total trabajos completados
    cur.execute("SELECT COUNT(*) as total FROM trabajos WHERE trabajador_id = ? AND estado IN ('completado', 'evaluado')",
               (trabajador_id,))
    completados = cur.fetchone()['total']
    
    # Total evaluaciones
    cur.execute("SELECT COUNT(*) as total FROM evaluaciones WHERE trabajador_id = ?", (trabajador_id,))
    evaluaciones = cur.fetchone()['total']
    
    # Promedio calificación
    promedio = get_promedio_calificacion(trabajador_id)
    
    # Promedio puntualidad, calidad, comunicación
    cur.execute("""
        SELECT AVG(puntualidad) as puntualidad,
               AVG(calidad) as calidad,
               AVG(comunicacion) as comunicacion,
               SUM(recomendaria) as recomendaciones
        FROM evaluaciones
        WHERE trabajador_id = ?
    """, (trabajador_id,))
    promedios = cur.fetchone()
    
    conn.close()
    
    return {
        'trabajos_completados': completados,
        'total_evaluaciones': evaluaciones,
        'promedio_general': promedio,
        'puntualidad': round(promedios['puntualidad'], 1) if promedios['puntualidad'] else 0,
        'calidad': round(promedios['calidad'], 1) if promedios['calidad'] else 0,
        'comunicacion': round(promedios['comunicacion'], 1) if promedios['comunicacion'] else 0,
        'recomendaciones': promedios['recomendaciones'] or 0
    }

# ============ FOTOS DE TRABAJOS ============

def add_foto_trabajo(trabajo_id: int, foto_base64: str, descripcion: Optional[str] = None):
    """Agregar foto a un trabajo"""
    conn = get_conn()
    cur = conn.cursor()
    fecha = datetime.utcnow().isoformat()
    cur.execute("INSERT INTO fotos_trabajos (trabajo_id, foto_base64, descripcion, fecha) VALUES (?, ?, ?, ?)",
               (trabajo_id, foto_base64, descripcion, fecha))
    conn.commit()
    conn.close()

def get_fotos_trabajo(trabajo_id: int) -> List[Dict]:
    """Obtener fotos de un trabajo"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM fotos_trabajos WHERE trabajo_id = ? ORDER BY fecha", (trabajo_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_fotos_trabajador(trabajador_id: int, limit: int = 10) -> List[Dict]:
    """Obtener fotos recientes de trabajos de un trabajador (para galería de perfil)"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT f.*, t.servicio_nombre
        FROM fotos_trabajos f
        JOIN (
            SELECT tr.id, s.service as servicio_nombre
            FROM trabajos tr
            JOIN services s ON tr.service_id = s.id
            WHERE tr.trabajador_id = ?
        ) t ON f.trabajo_id = t.id
        ORDER BY f.fecha DESC
        LIMIT ?
    """, (trabajador_id, limit))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]
