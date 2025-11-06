import streamlit as st

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Si la URL trae ?pagina=... la respetamos
# -------------------------
query_params = st.experimental_get_query_params()
if "pagina" in query_params:
    st.session_state.pagina = query_params["pagina"][0]

# -------------------------
# ESTADOS POR DEFECTO
# -------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "servicio" not in st.session_state:
    st.session_state.servicio = None
if "ubicacion" not in st.session_state:
    st.session_state.ubicacion = None
if "perfil_usuario" not in st.session_state:
    st.session_state.perfil_usuario = None
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# -------------------------
# CSS
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
    }
    div.stButton > button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: #2E8B57;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 700;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .top-bar a { color: white; text-decoration: none; padding: 8px 16px; }
    .top-bar a:hover { opacity: 0.95; cursor: pointer; }
    .conecta-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 72px;
        background-color: #ffffff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid rgba(0,0,0,0.08);
        z-index: 9999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.06);
    }
    .conecta-footer a {
        font-size: 26px;
        text-decoration: none;
        color: #333333;
        padding: 8px 16px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .conecta-footer a div { font-size:11px; margin-top:4px; }
    .conecta-footer a:hover {
        background-color: rgba(0,0,0,0.03);
    }
    .main > div {
        margin-top: 90px;
        margin-bottom: 100px;
    }
    .conecta-title {
        text-align: center;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# FUNCIONES DE NAVEGACIÓN
# -------------------------
def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    st.experimental_set_query_params(pagina=pagina_name)
    st.rerun()

def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)

def render_topbar():
    top_html = """
    <div class="top-bar">
        <a href="?pagina=inicio">ConectaServicios</a>
    </div>
    """
    st.markdown(top_html, unsafe_allow_html=True)

def render_footer():
    footer_html = """
    <div class="conecta-footer">
        <a href="?pagina=chats" title="Chats">💬<div>Chats</div></a>
        <a href="?pagina=notificaciones" title="Notificaciones">🔔<div>Notifs</div></a>
        <a href="?pagina=perfil_usuario" title="Mi perfil">👤<div>Perfil</div></a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# -------------------------
# TOPBAR
# -------------------------
render_topbar()

# -------------------------
# PANTALLAS
# -------------------------

# ---------- INICIO ----------
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")

    if st.button("Acerca de"):
        set_page("acerca")

    st.subheader("Selecciona una categoría:")
    c1, c2 = st.columns(2)

    with c1:
        if st.button("Cuidado de mascotas"):
            st.session_state.categoria = "Mascotas"
            set_page("subcategoria")
        if st.button("Limpieza y hogar"):
            st.session_state.categoria = "Hogar"
            set_page("subcategoria")

    with c2:
        if st.button("Clases particulares"):
            st.session_state.categoria = "Clases"
            set_page("subcategoria")
        if st.button("Cuidado de niños"):
            st.session_state.categoria = "Niños"
            set_page("subcategoria")

    st.markdown("---")
    st.write("Consejo: usa la barra inferior para acceder rápidamente a Chats, Notificaciones o a tu Perfil.")
    render_footer()

# ---------- CHATS (corregido y funcional) ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chat</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.markdown("---")

    # Mostrar mensajes anteriores
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

    # Campo de entrada
    mensaje = st.text_input("Escribe un mensaje y presiona Enter para enviar:", key="msg_input")

    # Procesamiento del mensaje
    if st.session_state.msg_input and mensaje == st.session_state.msg_input:
        texto = st.session_state.msg_input.strip()
        if texto:
            st.session_state.mensajes_chat.append({"autor": "Tú", "texto": texto})
            # Limpieza segura (no directa)
            st.session_state.update({"msg_input": ""})
            st.rerun()

    render_footer()

# ---------- NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("✅ Tu perfil fue visitado por @usuario123")
    st.write("💬 Tienes una nueva reseña en tu último trabajo")
    st.write("⭐ Recibiste una valoración de 5 estrellas")
    render_footer()

# ---------- PERFIL ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("**Nombre:** Ignacio")
    st.write("**Edad:**  XX")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas (ejemplo)")
    render_footer()
