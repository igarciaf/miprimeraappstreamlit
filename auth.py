# auth.py
import bcrypt
import db

def init():
    db.init_db()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    except Exception:
        return False

def register_user(nombre: str, email: str, password: str, bio: str = "", comuna: str = "") -> int:
    # Validar si ya existe
    if db.get_user_by_email(email):
        return 0  # usuario ya existe
    pwd_hash = hash_password(password)
    user_id = db.create_user(nombre, email, pwd_hash, bio, comuna)
    return user_id

def login_user(email: str, password: str) -> int:
    user = db.get_user_by_email(email)
    if not user:
        return 0
    if verify_password(password, user["password_hash"]):
        return user["id"]
    return 0
