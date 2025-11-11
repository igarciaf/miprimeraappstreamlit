# auth.py
import streamlit as st
import hashlib
import db


def hash_password(password: str) -> str:
    """Genera un hash SHA-256 de la contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(nombre, email, password, bio=None, comuna=None):
    """Registra un nuevo usuario si no existe"""
    if not nombre or not email or not password:
        st.error("Por favor completa todos los campos obligatorios.")
        return

    existing_user = db.get_user_by_email(email)
    if existing_user:
        st.warning("Ya existe un usuario registrado con ese correo.")
        return

    password_hash = hash_password(password)
    db.create_user(nombre, email, password_hash, bio, comuna)
    st.success("Registro exitoso ✅. Ahora puedes iniciar sesión.")


def login_user(email, password):
    """Verifica las credenciales del usuario"""
    user = db.get_user_by_email(email)
    if not user:
        st.error("Usuario no encontrado.")
        return None

    password_hash = hash_password(password)
    if user[3] == password_hash:  # password_hash está en la posición 3
        st.session_state["user"] = {
            "id": user[0],
            "nombre": user[1],
            "email": user[2],
            "bio": user[4],
            "comuna": user[5],
        }
        st.success(f"Bienvenido {user[1]} 👋")
        return user
    else:
        st.error("Contraseña incorrecta.")
        return None


def logout_user():
    """Cierra la sesión actual"""
    if "user" in st.session_state:
        del st.session_state["user"]
        st.success("Sesión cerrada correctamente.")
