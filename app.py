import streamlit as st
import db, auth

# -------------------------
# CONFIGURACIÓN INICIAL
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# Inicializa la base de datos
auth.init()

# -------------------------
# ESTADOS DE SESIÓN
# -------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# -------------------------
# LISTA DE COMUNAS DE SANTIAGO
# -------------------------
comunas_santiago = [
    "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba", "Independencia",
    "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina", "Las Condes", "Lo Barnechea",
    "Lo Espejo", "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén",
    "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín",
    "San Miguel", "San Ramón", "Santiago", "Vitacura"
]

# -------------------------
# FUNCIÓN CAMBIAR PÁGINA
# -------------------------
def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    st.experimental_rerun()

# -------------------------
# BLOQUE DE AUTENTICACIÓN
# -------------------------
if st.session_state.user_id == 0:
    st.sidebar.title("Conecta 🤝")
    st.sidebar.markdown("### Inicia sesión o regístrate")

    tab_login, tab_register = st.tabs(["Iniciar sesión", "Registrarse"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            email_l = st.text_input("Correo electrónico")
            password_l = st.text_input("Contraseña", type="password")
            btn = st.form_submit_button("Iniciar sesión")
            if btn:
                user_id = auth.login_user(email_l.strip(), password_l)
                if user_id:
                    user = db.get_user_by_id(user_id)
                    st.session_state.user_id = user_id
                    st.session_state.user_name = user["nombre"]
                    st.success("Has iniciado sesión ✅")
                    st.experimental_rerun()
                else:
                    st.error("Correo o contraseña incorrectos.")

    with tab_register:
        with st.form("register_form", clear_on_submit=False):
            nombre = st.text_input("Nombre completo")
            email_r = st.text_input("Correo electrónico")
            password_r = st.text_input("Contraseña", type="password")
            comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago)
            bio_r = st.text_area("Sobre ti (opcional)")
            btnr = st.form_submit_button("Crear cuenta")
            if btnr:
                new_id = auth.register_user(nombre.strip(), email_r.strip(), password_r, bio_r, comuna_r)
                if new_id:
                    st.success("Cuenta creada correctamente. Ahora inicia sesión.")
                else:
                    st.error("Ya existe un usuario con ese correo.")
    st.stop()

# -------------------------
# BARRA LATERAL DE NAVEGACIÓN
# -------------------------
st.sidebar.title("Navegación")
st.sidebar.write(f"👤 {st.session_state.user_name}")
st.sidebar.button("🏠 Inicio", on_click=lambda: set_page("inicio"))
st.sidebar.button("💬 Chat", on_click=lambda: set_page("chats"))
st.sidebar.button("🔔 Notificaciones", on_click=lambda: set_page("notificaciones"))
st.sidebar.button("👤 Mi Perfil", on_click=lambda: set_page("perfil_usuario"))
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Cerrar sesión"):
    st.session_state.user_id = 0
    st.session_state.user_name = ""
    st.experimental_rerun()

# -------------------------
# ESTILOS CSS
# -------------------------
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 76px;
        width: 200px;
        background-color: #2E8B57;
        color: white;
        border-radius: 12px;
        font-size: 17px;
        margin: 6px 8px;
        border: none;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        background-color: #256f47;
        transform: translateY(-1px);
    }
    .conecta-title {
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# CONTENIDO PRINCIPAL SEGÚN PÁGINA
# -------------------------

# ---------- INICIO ----------
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")

    if st.button("Acerca de"):
        st.info("Conecta es una plataforma para conectar personas que ofrecen y buscan servicios cotidianos.")

    st.subheader("Selecciona una categoría:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cuidado de mascotas"):
            st.session_state.categoria = "Mascotas"
            st.success("Abrir sección Mascotas (en desarrollo)")
        if st.button("Limpieza y hogar"):
            st.session_state.categoria = "Hogar"
            st.success("Abrir sección Hogar (en desarrollo)")
    with c2:
        if st.button("Clases particulares"):
            st.session_state.categoria = "Clases"
            st.success("Abrir sección Clases (en desarrollo)")
        if st.button("Cuidado de niños"):
            st.session_state.categoria = "Niños"
            st.success("Abrir sección Niños (en desarrollo)")

    st.markdown("---")
    st.info("Usa la barra lateral para navegar entre Inicio, Chats, Notificaciones o tu Perfil.")

# ---------- CHATS ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chat</h1>', unsafe_allow_html=True)

    st.markdown("---")

    if st.session_state.mensajes_chat:
        for msg in st.session_state.mensajes_chat:
            align = "right" if msg["autor"] == "Tú" else "left"
            color = "#DCF8C6" if msg["autor"] == "Tú" else "#F1F0F0"
            st.markdown(
                f"<div style='text-align:{align}; background-color:{color}; "
                f"padding:10px; border-radius:12px; margin:6px; "
                f"display:inline-block; max-width:70%;'>"
                f"<b>{msg['autor']}:</b> {msg['texto']}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")

    mensaje = st.text_input("Escribe un mensaje y presiona Enter para enviar:", key="msg_input")
    if mensaje.strip() != "":
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": mensaje})
        st.session_state.msg_input = ""
        st.rerun()

# ---------- NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    notifs = db.get_notifications(st.session_state.user_id)
    if notifs:
        for n in notifs:
            st.write(f"🔸 {n['mensaje']} ({n['fecha'][:10]})")
    else:
        st.info("No tienes notificaciones nuevas.")

# ---------- PERFIL ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)

    user = db.get_user_by_id(st.session_state.user_id)
    if not user:
        st.warning("No se encontró tu usuario.")
    else:
        st.write(f"**Nombre:** {user['nombre']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Comuna:** {user['comuna'] or '-'}")
        st.write(f"**Bio:** {user['bio'] or '-'}")

        with st.form("editar_perfil"):
            nuevo_nombre = st.text_input("Editar nombre", user['nombre'])
            nueva_bio = st.text_area("Editar bio", user['bio'] or "")
            nueva_comuna = st.selectbox("Editar comuna", [""] + comunas_santiago, index=(comunas_santiago.index(user['comuna'])+1 if user['comuna'] in comunas_santiago else 0))
            if st.form_submit_button("Guardar cambios"):
                db.update_user_profile(st.session_state.user_id, nuevo_nombre, nueva_bio, nueva_comuna)
                st.success("Perfil actualizado correctamente")
                st.experimental_rerun()
