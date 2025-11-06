import streamlit as st

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Si la URL trae ?pagina=... la respetamos (permite que el logo vuelva al inicio)
# -------------------------
query_params = st.experimental_get_query_params()
if "pagina" in query_params:
    # sólo setear si viene en query params para mantener compatibilidad con los enlaces del footer
    st.session_state.pagina = query_params["pagina"][0]

# -------------------------
# ESTADOS POR DEFECTO (seguros)
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

# historial de mensajes (lista de dicts: {"autor": "...", "texto": "...", "hora": "HH:MM"})
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []

# campo controlado para el input del chat
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

    /* chat bubbles minimal */
    .chat-bubble {
        padding: 10px 12px;
        border-radius: 12px;
        margin: 6px 0;
        display: inline-block;
        max-width: 70%;
        word-wrap: break-word;
    }
    .chat-right { background: #DCF8C6; text-align: right; float: right; clear: both; }
    .chat-left { background: #F1F0F0; text-align: left; float: left; clear: both; }
    .chat-time { font-size: 10px; color: #666; margin-top: 4px; display:block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# FUNCIONES DE NAVEGACIÓN
# -------------------------
def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    # actualizar query params para que los enlaces funcionen y para navegacion coherente
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
# FUNCION PARA ENVIAR MENSAJE (callback para text_input)
# -------------------------
from datetime import datetime

def send_chat_message():
    """
    callback seguro: se ejecuta fuera del render principal por Streamlit cuando
    el usuario presiona Enter (o el input cambia y pierde foco).
    """
    texto = st.session_state.get("msg_input", "").strip()
    if texto:
        hora = datetime.now().strftime("%H:%M")
        # append de forma segura al estado
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": texto, "hora": hora})
        # (opcional) simulamos una respuesta inmediata del otro usuario para pruebas
        # comentar o eliminar la siguiente 3 líneas si no quieres respuesta automática
        respuesta = "Gracias, te responderé pronto 👍"
        hora2 = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Otro", "texto": respuesta, "hora": hora2})
    # limpiar el campo de input de forma segura dentro del callback
    st.session_state.msg_input = ""

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

# ---------- CHATS (corregido y profesional) ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")

    st.markdown("---")

    # Mostrar mensajes previos (si existen)
    if st.session_state.mensajes_chat:
        # iterar y mostrar con burbujas y hora
        for msg in st.session_state.mensajes_chat:
            clase = "chat-right" if msg.get("autor") == "Tú" else "chat-left"
            texto = msg.get("texto", "")
            hora = msg.get("hora", "")
            st.markdown(
                f'<div class="chat-bubble {clase}">{texto}<span class="chat-time">{hora}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")

    # Campo de entrada controlado: al presionar Enter se ejecuta send_chat_message (callback)
    st.text_input(
        "Escribe un mensaje y presiona Enter para enviar:",
        key="msg_input",
        on_change=send_chat_message
    )

    render_footer()

# ---------- NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    # por ahora mostramos estático (puedes enlazar con st.session_state.notificaciones en el futuro)
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
