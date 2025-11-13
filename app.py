import streamlit as st
import auth
import db

auth.init()

st.set_page_config(page_title="ConectaApp", page_icon="🤝", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Inicio"
if "user_id" not in st.session_state:
    st.session_state.user_id = None

def go_to(page):
    st.session_state.page = page

# --- SIDEBAR ---
with st.sidebar:
    st.title("ConectaApp")
    if st.session_state.user_id:
        user = db.get_user_by_id(st.session_state.user_id)
        st.subheader(f"👋 Hola, {user['nombre']}")
        st.button("Inicio", on_click=lambda: go_to("Inicio"))
        st.button("Perfil", on_click=lambda: go_to("Perfil"))
        st.button("Chat", on_click=lambda: go_to("Chat"))
        st.button("Notificaciones", on_click=lambda: go_to("Notificaciones"))
        st.button("Agregar servicio", on_click=lambda: go_to("Agregar servicio"))
        if st.button("Cerrar sesión"):
            st.session_state.user_id = None
            go_to("Inicio")
    else:
        st.button("Iniciar sesión", on_click=lambda: go_to("Iniciar sesión"))
        st.button("Registrarse", on_click=lambda: go_to("Registrarse"))

# --- PÁGINAS ---
if st.session_state.page == "Inicio":
    st.title("🔎 Busca servicios o ayuda en tu zona")

    search = st.text_input("¿Qué servicio necesitas?")
    if st.button("Buscar"):
        if search.strip():
            resultados = db.search_users_by_service(search)
            if resultados:
                st.success(f"Usuarios que ofrecen '{search}':")
                for r in resultados:
                    st.write(f"👤 {r['nombre']} — 📍 {r['comuna']} — 💬 {r['servicios']}")
            else:
                st.warning("No se encontraron resultados.")
        else:
            st.warning("Por favor escribe algo para buscar.")

elif st.session_state.page == "Registrarse":
    st.header("📝 Crear cuenta")
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    comuna = st.text_input("Comuna")
    servicios = st.text_input("Servicios que puedes ofrecer (separados por comas)")
    bio = st.text_area("Cuéntanos un poco sobre ti")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrarme"):
        user_id = auth.register_user(nombre, email, password, bio, comuna, servicios)
        if user_id:
            st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
            go_to("Iniciar sesión")
        else:
            st.error("El correo ya está en uso o hubo un error.")

elif st.session_state.page == "Iniciar sesión":
    st.header("🔐 Iniciar sesión")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        user_id = auth.login_user(email, password)
        if user_id:
            st.session_state.user_id = user_id
            go_to("Inicio")
        else:
            st.error("Credenciales incorrectas.")

elif st.session_state.page == "Perfil":
    if not st.session_state.user_id:
        st.warning("Inicia sesión para ver tu perfil.")
    else:
        user = db.get_user_by_id(st.session_state.user_id)
        st.header(f"👤 Perfil de {user['nombre']}")
        st.write(f"📧 {user['email']}")
        st.write(f"📍 {user['comuna']}")
        st.write(f"🛠️ Servicios: {user['servicios'] or 'No especificado'}")
        st.write(f"💬 Bio: {user['bio'] or 'Sin descripción'}")

elif st.session_state.page == "Agregar servicio":
    if not st.session_state.user_id:
        st.warning("Inicia sesión para agregar servicios.")
    else:
        user = db.get_user_by_id(st.session_state.user_id)
        st.header("🛠️ Agregar o modificar servicios que ofreces")
        servicios_actuales = user["servicios"] or ""
        nuevos_servicios = st.text_input("Lista de servicios (separados por comas):", value=servicios_actuales)
        if st.button("Guardar cambios"):
            db.update_user_profile(user["id"], servicios=nuevos_servicios)
            st.success("Servicios actualizados con éxito.")
            go_to("Perfil")
