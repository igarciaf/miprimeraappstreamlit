# app.py
import streamlit as st
from datetime import datetime

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Si la URL trae ?pagina=... la respetamos (permite que el logo vuelva al inicio)
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
if "chat" not in st.session_state:
    st.session_state.chat = []  # historial del chat actual
if "notificaciones" not in st.session_state:
    st.session_state.notificaciones = []
if "notificaciones_no_leidas" not in st.session_state:
    st.session_state.notificaciones_no_leidas = 0

# -------------------------
# CSS: botones uniformes + footer fijo + top bar fija + chat burbujas
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
        position: relative;
    }
    .conecta-footer a div { font-size:11px; margin-top:4px; }
    .conecta-footer a:hover {
        background-color: rgba(0,0,0,0.03);
    }
    .notif-badge {
        position: absolute;
        top: 2px;
        right: 12px;
        background-color: red;
        color: white;
        font-size: 12px;
        border-radius: 50%;
        width: 18px;
        height: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .main > div {
        margin-top: 90px;
        margin-bottom: 100px;
    }
    .conecta-title {
        text-align: center;
        margin-bottom: 8px;
    }
    /* burbujas de chat */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    .mensaje {
        display: flex;
        margin: 6px 0;
    }
    .mensaje-yo {
        justify-content: flex-end;
    }
    .burbuja {
        max-width: 70%;
        padding: 10px;
        border-radius: 15px;
        font-size: 15px;
        position: relative;
    }
    .yo {
        background-color: #DCF8C6;
        align-self: flex-end;
    }
    .otro {
        background-color: #ffffff;
        border: 1px solid #ddd;
    }
    .hora {
        font-size: 10px;
        color: #666;
        margin-top: 2px;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# FUNCIONES
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
    notif_count = st.session_state.get("notificaciones_no_leidas", 0)
    notif_html = f'<span class="notif-badge">{notif_count}</span>' if notif_count > 0 else ""
    footer_html = f"""
    <div class="conecta-footer">
        <a href="?pagina=chats" title="Chats">💬<div>Chats</div></a>
        <a href="?pagina=notificaciones" title="Notificaciones">🔔{notif_html}<div>Notifs</div></a>
        <a href="?pagina=perfil_usuario" title="Mi perfil">👤<div>Perfil</div></a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def agregar_notificacion(texto):
    st.session_state.notificaciones.append({"texto": texto, "leida": False})
    st.session_state.notificaciones_no_leidas += 1

# -------------------------
# RENDER TOPBAR
# -------------------------
render_topbar()

# -------------------------
# PANTALLAS
# -------------------------
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
    render_footer()

elif st.session_state.pagina == "acerca":
    st.markdown('<h1 class="conecta-title">Acerca de Conecta</h1>', unsafe_allow_html=True)
    st.write("**Conecta** une a personas que buscan servicios con quienes los ofrecen.")
    volver("inicio")
    render_footer()

elif st.session_state.pagina == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Selecciona un tipo de servicio:")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas"],
        "Hogar": ["Limpieza general", "Cuidado de jardín"],
        "Clases": ["Matemáticas", "Inglés", "Música"],
        "Niños": ["Cuidado por horas", "Apoyo escolar"]
    }
    seleccion = st.selectbox("Selecciona el servicio:", ["-- Elige una opción --"] + opciones.get(st.session_state.categoria, []))
    if seleccion != "-- Elige una opción --":
        st.session_state.servicio = seleccion
        set_page("ubicacion")
    render_footer()

elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", ["Providencia", "Ñuñoa", "Maipú"])
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")
    render_footer()

elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio}</h1>', unsafe_allow_html=True)
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
    render_footer()

elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario"}
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write("**Descripción:** Persona confiable (simulación).")
    st.subheader("💬 Chat")
    # mostrar mensajes como burbujas
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for m in st.session_state.chat:
        clase = "mensaje mensaje-yo" if m["autor"] == "yo" else "mensaje"
        estilo = "yo" if m["autor"] == "yo" else "otro"
        st.markdown(
            f'<div class="{clase}"><div class="burbuja {estilo}">{m["texto"]}<div class="hora">{m["hora"]}</div></div></div>',
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    mensaje = st.text_input("Escribe un mensaje...", key="chat_input")
    if st.session_state.get("enter_pressed", False):
        mensaje = st.session_state.chat_input
        if mensaje.strip():
            hora = datetime.now().strftime("%H:%M")
            st.session_state.chat.append({"autor": "yo", "texto": mensaje, "hora": hora})
            agregar_notificacion(f"Nueva respuesta en el chat con {r['nombre']}")
            st.session_state.chat.append({"autor": "otro", "texto": "Perfecto, gracias por tu mensaje 👍", "hora": hora})
        st.session_state.chat_input = ""
        st.session_state.enter_pressed = False
        st.rerun()

    if st.button("Enviar mensaje"):
        if mensaje.strip():
            hora = datetime.now().strftime("%H:%M")
            st.session_state.chat.append({"autor": "yo", "texto": mensaje, "hora": hora})
            agregar_notificacion(f"Nueva respuesta en el chat con {r['nombre']}")
            st.session_state.chat.append({"autor": "otro", "texto": "Perfecto, gracias por tu mensaje 👍", "hora": hora})
            st.rerun()

    render_footer()

elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    if not st.session_state.notificaciones:
        st.info("No tienes notificaciones nuevas.")
    else:
        for n in st.session_state.notificaciones:
            st.write(f"📩 {n['texto']}")
        st.session_state.notificaciones_no_leidas = 0
    render_footer()

elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("**Nombre:** Ignacio")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas")
    render_footer()
