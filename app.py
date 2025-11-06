import streamlit as st

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# CONTROL DE ESTADO Y NAVEGACIÓN
# -------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    st.experimental_rerun()

def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)

# -------------------------
# CSS MEJORADO
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
        transition: background-color 0.2s ease;
    }
    div.stButton > button:hover {
        background-color: #276e47;
        transform: translateY(-1px);
    }

    .top-bar {
        position: fixed;
        top: 0; left: 0; right: 0;
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

    .conecta-footer {
        position: fixed;
        bottom: 0; left: 0; right: 0;
        height: 72px;
        background-color: #ffffff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid rgba(0,0,0,0.08);
        z-index: 9999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.06);
    }

    .footer-btn {
        font-size: 26px;
        text-decoration: none;
        color: #333333;
        padding: 8px 16px;
        border-radius: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }
    .footer-btn:hover {
        background-color: rgba(0,0,0,0.05);
    }
    .footer-text { font-size: 11px; margin-top: 4px; }

    .main > div { margin-top: 90px; margin-bottom: 100px; }
    .conecta-title { text-align: center; margin-bottom: 8px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# TOP BAR
# -------------------------
st.markdown('<div class="top-bar">ConectaServicios</div>', unsafe_allow_html=True)

# -------------------------
# FOOTER (ahora funcional dentro de Streamlit)
# -------------------------
def render_footer():
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬 Chats"):
            set_page("chats")
    with col2:
        if st.button("🔔 Notifs"):
            set_page("notificaciones")
    with col3:
        if st.button("👤 Perfil"):
            set_page("perfil_usuario")

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

# ---------- CHATS ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chat</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.markdown("---")

    # Mostrar mensajes previos
    if st.session_state.mensajes_chat:
        for msg in st.session_state.mensajes_chat:
            align = "right" if msg["autor"] == "Tú" else "left"
            color = "#DCF8C6" if msg["autor"] == "Tú" else "#F1F0F0"
            st.markdown(
                f"<div style='text-align:{align}; background-color:{color}; padding:10px; border-radius:12px; "
                f"margin:6px; display:inline-block; max-width:70%;'><b>{msg['autor']}:</b> {msg['texto']}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")

    mensaje = st.text_input("Escribe un mensaje y presiona Enter para enviar:", key="msg_input")
    if mensaje.strip():
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": mensaje})
        st.session_state.msg_input = ""
        st.experimental_rerun()

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
    st.write("**Edad:** XX")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas (ejemplo)")
    render_footer()
