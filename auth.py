# auth.py — Manejo de registro e inicio de sesión
# (EN PRESENTACIÓN) Este archivo controla todo lo relacionado con:
#   - Crear usuarios nuevos
#   - Verificar credenciales al iniciar sesión
#   - Encriptar las contraseñas

import hashlib
import db
from typing import Optional, Dict


# -----------------------------
# ENCRIPTAR CONTRASEÑAS
# -----------------------------
def hash_password(password: str) -> str:
    """
    (EN PRESENTACIÓN)
    Las contraseñas NO se almacenan en texto plano.
    Aquí se encriptan con SHA-256 antes de guardarlas.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# -----------------------------
# REGISTRO DE USUARIO
# -----------------------------
def register_user(nombre: str, email: str, password: str,
                  bio: str = "", comuna: str = "") -> int:
    """
    Crea un usuario nuevo si:
      - Faltan datos → rechaza
      - Ya existe el email → rechaza
      - Si todo está ok, crea en DB usando db.create_user()
    """
    if not nombre or not email or not password:
        return 0

    # Verificar si el correo ya existe
    if db.get_user_by_email(email):
        return 0

    pwd_hash = hash_password(password)

    # Guardar usuario en la base de datos
    user_id = db.create_user(nombre, email, pwd_hash, bio, comuna)
    return user_id


# -----------------------------
# LOGIN
# -----------------------------
def login_user(email: str, password: str) -> Optional[Dict]:
    """
    Verifica si el usuario existe y si la contraseña coincide.
    Devuelve el usuario completo si el login es correcto.
    """
    user = db.get_user_by_email(email)

    if not user:
        return None

    # Comparar hash de contraseñas
    if hash_password(password) == user["password_hash"]:
        return user

    return None
