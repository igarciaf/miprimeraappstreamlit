# app.py (versión corregida - reemplaza tu archivo actual)
import streamlit as st
from datetime import datetime

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# LEER QUERY PARAMS (permite que los enlaces href="?pagina=..." funcionen)
# -------------------------
query_params = st.experimental_get_query_params()
if "pagina" in query_params:
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

if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# -------------------------
# CSS (hover mejorado + footer fijo + chat bubbles)
# -------------------------
st.markdown(
    """
    <style>
    /* botones large */
    div.stButton > button {
        height: 76px;
        width: 200px;
        background-color: #2E8B57;
        color: white;
        border-radius: 12px;
        font-size: 17px;
        margin: 6px 8px;
        border: none;
        transition: background-color 0.15s ease, transform 0.12s ease;
    }
    div.stButton > button:hover {
        background-color: #276e47;
        transform: translateY(-1px);
    }

    .top-bar {
        position: fixed; top: 0; left: 0; right: 0; height: 64px;
        background-color: #2E8B57; color: white;
        display:flex; align-items:center; justify-content:center;
        font-size:22px; font-weight:700; z-index:9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .top-bar a { color: white; text-decoration: none; padding: 8px 16px; }
    .top-bar a:hover { opacity: 0.95; cursor: pointer; }

    .conecta-footer {
        position: fixed; bottom: 0; left: 0; right: 0; height: 72px;
        background-color: #ffffff; display:flex; justify-content:space-around;
        align-items:center; border-top:1px solid rgba(0,0,0,0.08);
        z-index:9999; box-shadow:0 -4px 12px rgba(0,0,0,0.06);
    }
    .conecta-footer a {
        font-size:26px; text-decoration:none; color:#333333; padding:8px 16px;
        border-radius:10px; display:flex; flex-direction:column; align-items:center;
    }
    .conecta-footer a div { font-size:11px; margin-top:4px; }
    .conecta-footer a:hover { background-color: rgba(0,0,0,0.03); cursor:pointer; }

    .main > div { margin-top: 90px; margin-bottom: 100px; }
    .conecta-title { text-align:center; margin-bottom:8px; }

    /* chat bubbles */
    .chat-bubble { padding:10px 12px; border-radius:12px; margin:6px 0; display:inline-block; max-width:70%; word-wrap:break-word; }
    .chat-right { background:#DCF8C6; text-align:right; float:right; clear:both; }
    .chat-left { background:#F1F0F0; text-align:left; float:left; clear:both; }
    .chat-time { font-size:10px; color:#666; margin-top:4px; display:block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# NAVEGACIÓN: función segura (sin experimental_rerun)
# -------------------------
def set_page(pagina_name):
    """
    Actualiza st.session_state y la URL (query param).
    No forzamos rerun para evitar errores en algunos entornos.
    Streamlit volverá a ejecutar el script en la siguiente interacción automáticamente.
    """
    st.session_state.pagina = pagina_name
    st.experimental_set_query_params(pagina=pagina_name)


def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)


# -------------------------
# TOPBAR y FOOTER (footer fijo HTML con hrefs ?pagina=...)
# -------------------------
def render_topbar():
    st.markdown('<div class="top-bar"><a href="?pagina=inicio">ConectaServicios</a></div>', unsafe_allow_html=True)

def render_footer_html():
    footer_html = """
    <div class="conecta-footer">
        <a href="?pagina=chats" title="Chats">💬<div>Chats</div></a>
        <a href="?pagina=notificaciones" title="Notificaciones">🔔<div>Notifs</div></a>
        <a href="?pagina=perfil_usuario" title="Mi perfil">👤<div>Perfil</div></a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# -------------------------
# CALLBACK del chat (on_change)
# -------------------------
def send_chat_message():
    texto = st.session_state.get("msg_input", "").strip()
    if texto:
        hora = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": texto, "hora": hora})
        # respuesta automática de prueba (puedes quitarla)
        hora2 = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Otro", "texto": "Gracias, te respondo pronto 👍", "hora": hora2})
    # limpiar el campo desde el callback (es seguro)
    st.session_state.msg_input = ""

# -------------------------
# RENDER TOPBAR
# -------------------------
render_topbar()

# -------------------------
# PÁGINAS (idénticas en lógica a las previas)
# -------------------------
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")

    # botones que usan set_page (no cambian)
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
    render_footer_html()

elif st.session_state.pagina == "acerca":
    st.markdown('<h1 class="conecta-title">Acerca de Conecta</h1>', unsafe_allow_html=True)
    st.write("**Conecta** une a quienes buscan servicios con quienes los ofrecen.")
    volver("inicio")
    render_footer_html()

elif st.session_state.pagina == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    volver("inicio")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Electricidad", "Pintura"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Acompañamiento"]
    }
    seleccion = st.selectbox("Selecciona el servicio:", ["-- Elige --"] + opciones.get(st.session_state.categoria, []))
    if seleccion != "-- Elige --":
        st.session_state.servicio = seleccion
        set_page("ubicacion")
    render_footer_html()

elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", ["Providencia", "Ñuñoa", "Maipú", "Las Condes", "Santiago"])
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")
    render_footer_html()

elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio} — {st.session_state.ubicacion}</h1>', unsafe_allow_html=True)
    volver("ubicacion")
    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "★★★★☆"},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "★★★★★"},
    ]
    for r in resultados:
        st.info(f"{r['nombre']} — {r['servicio']} — {r['valoracion']}")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")
    render_footer_html()

elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario"}
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write("**Descripción:** Persona confiable (simulación).")
    # chat dentro de perfil (opcional)
    mensaje_key = f"msg_profile_{r.get('nombre','')}"
    st.text_input("💬 Envía un mensaje:", key=mensaje_key, on_change=lambda: None)
    render_footer_html()

elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.markdown("---")
    if st.session_state.mensajes_chat:
        for msg in st.session_state.mensajes_chat:
            clase = "chat-right" if msg.get("autor") == "Tú" else "chat-left"
            texto = msg.get("texto", "")
            hora = msg.get("hora", "")
            st.markdown(f'<div class="chat-bubble {clase}">{texto}<span class="chat-time">{hora}</span></div>', unsafe_allow_html=True)
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")
    # input controlado: al presionar Enter se ejecuta send_chat_message
    st.text_input("Escribe un mensaje y presiona Enter para enviar:", key="msg_input", on_change=send_chat_message)
    render_footer_html()

elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("✅ Tu perfil fue visitado por @usuario123")
    st.write("💬 Tienes una nueva reseña en tu último trabajo")
    st.write("⭐ Recibiste una valoración de 5 estrellas")
    render_footer_html()

elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("**Nombre:** Ignacio")
    st.write("**Edad:**  XX")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas (ejemplo)")
    render_footer_html()
