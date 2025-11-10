import streamlit as st
import db
import auth

# Inicializar base de datos
db.init_db()

# --- Configuración general ---
st.set_page_config(page_title="Conecta App", layout="wide")

# --- Variables de sesión ---
if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# --- Funciones de navegación ---
def go_to(page_name):
    st.session_state.page = page_name

# --- Encabezado con botón de inicio ---
st.markdown(
    """
    <style>
    .top-button {
        position: fixed;
        top: 10px;
        right: 20px;
        background-color: #4CAF50;
        color: white;
        padding: 8px 15px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        z-index: 9999;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<a href="#" class="top-button" onclick="window.location.reload()">🏠 Inicio</a>', unsafe_allow_html=True)

# --- Barra lateral de navegación ---
st.sidebar.title("📱 Navegación")
if st.session_state.user_id:
    st.sidebar.write(f"👤 Conectado como: {db.get_user_by_id(st.session_state.user_id)['nombre']}")
else:
    st.sidebar.write("No has iniciado sesión")

menu = st.sidebar.radio(
    "Ir a:",
    ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Chat", "Notificaciones"],
    index=["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Chat", "Notificaciones"].index(
        st.session_state.page.capitalize() if st.session_state.page else "Inicio"
    )
)

if menu == "Inicio":
    st.session_state.page = "inicio"
elif menu == "Iniciar sesión":
    st.session_state.page = "login"
elif menu == "Registrarse":
    st.session_state.page = "registro"
elif menu == "Perfil":
    st.session_state.page = "perfil"
elif menu == "Chat":
    st.session_state.page = "chat"
elif menu == "Notificaciones":
    st.session_state.page = "notificaciones"

# --- Páginas ---
def pagina_inicio():
    st.title("🌟 Bienvenido a Conecta App")
    st.write("Conecta con personas que ofrecen o buscan servicios en tu zona.")
    st.image("https://cdn-icons-png.flaticon.com/512/1041/1041916.png", width=200)
    st.write("Usa el menú lateral para navegar por las secciones de la aplicación.")

def pagina_login():
    st.title("🔐 Iniciar sesión")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        user_id = auth.login_user(email, password)
        if user_id:
            st.session_state.user_id = user_id
            st.success("Sesión iniciada correctamente ✅")
            st.session_state.page = "inicio"
            st.experimental_rerun()
        else:
            st.error("Correo o contraseña incorrectos.")

def pagina_registro():
    st.title("📝 Registrarse")
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    bio = st.text_area("Descripción personal")
    comuna = st.text_input("Comuna (por ejemplo, Santiago Centro)")
    if st.button("Crear cuenta"):
        if nombre and email and password:
            user_id = auth.register_user(nombre, email, password, bio, comuna)
            if user_id:
                st.success("Cuenta creada correctamente 🎉 Ahora puedes iniciar sesión.")
            else:
                st.error("El correo ya está registrado.")
        else:
            st.warning("Completa todos los campos obligatorios.")

def pagina_perfil():
    if not st.session_state.user_id:
        st.warning("Primero debes iniciar sesión.")
        return
    user = db.get_user_by_id(st.session_state.user_id)
    st.title("👤 Mi perfil")
    st.write(f"**Nombre:** {user['nombre']}")
    st.write(f"**Correo:** {user['email']}")
    st.write(f"**Biografía:** {user['bio'] or 'Sin descripción.'}")
    st.write(f"**Comuna:** {user['comuna'] or 'No especificada.'}")
    st.divider()

    st.subheader("✏️ Editar perfil")
    nuevo_nombre = st.text_input("Nuevo nombre", user["nombre"])
    nueva_bio = st.text_area("Nueva descripción", user["bio"])
    nueva_comuna = st.text_input("Nueva comuna", user["comuna"])
    if st.button("Actualizar perfil"):
        db.update_user_profile(st.session_state.user_id, nuevo_nombre, nueva_bio, nueva_comuna)
        st.success("Perfil actualizado ✅")
        st.experimental_rerun()

def pagina_chat():
    if not st.session_state.user_id:
        st.warning("Primero debes iniciar sesión.")
        return

    st.title("💬 Chat")
    users = []
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, nombre FROM users WHERE id != ?", (st.session_state.user_id,))
    users = cur.fetchall()
    conn.close()

    user_names = [u["nombre"] for u in users]
    user_ids = [u["id"] for u in users]

    if user_names:
        selected_user = st.selectbox("Selecciona un usuario para chatear", user_names)
        receptor_id = user_ids[user_names.index(selected_user)]

        st.subheader(f"Conversación con {selected_user}")
        mensajes = db.get_messages_between(st.session_state.user_id, receptor_id)
        for m in mensajes:
            autor = "Tú" if m["emisor_id"] == st.session_state.user_id else selected_user
            st.write(f"**{autor}:** {m['contenido']}")

        nuevo_mensaje = st.text_input("Escribe un mensaje")
        if st.button("Enviar"):
            if nuevo_mensaje.strip():
                db.add_message(st.session_state.user_id, receptor_id, nuevo_mensaje)
                st.experimental_rerun()
    else:
        st.info("No hay otros usuarios registrados para chatear.")

def pagina_notificaciones():
    if not st.session_state.user_id:
        st.warning("Primero debes iniciar sesión.")
        return
    st.title("🔔 Notificaciones")
    notifs = db.get_notifications(st.session_state.user_id)
    if not notifs:
        st.info("No tienes notificaciones nuevas.")
    else:
        for n in notifs:
            estado = "✅ Leído" if n["leido"] else "🆕 Nuevo"
            st.write(f"**{n['tipo']}** - {n['mensaje']} ({estado})")

# --- Mostrar la página actual ---
if st.session_state.page == "inicio":
    pagina_inicio()
elif st.session_state.page == "login":
    pagina_login()
elif st.session_state.page == "registro":
    pagina_registro()
elif st.session_state.page == "perfil":
    pagina_perfil()
elif st.session_state.page == "chat":
    pagina_chat()
elif st.session_state.page == "notificaciones":
    pagina_notificaciones()
