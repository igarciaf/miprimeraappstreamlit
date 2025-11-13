# auth.py
import hashlib
import db
from typing import Optional, Dict

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def register_user(nombre: str, email: str, password: str, bio: str = "", comuna: str = "") -> int:
    """Devuelve id nuevo o 0 si falla (usuario existe o falta info)."""
    if not nombre or not email or not password:
        return 0
    if db.get_user_by_email(email):
        return 0
    pwd_hash = hash_password(password)
    user_id = db.create_user(nombre, email, pwd_hash, bio, comuna)
    return user_id

def login_user(email: str, password: str) -> Optional[Dict]:
    user = db.get_user_by_email(email)
    if not user:
        return None
    if hash_password(password) == user["password_hash"]:
        return user
    return None
