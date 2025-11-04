# app.py
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
if "notificaciones" not in st.session_state:
    st.session_state.notificaciones = [
        {"tipo": "sistema", "texto": "Bienvenido a Conecta 👋", "leida": True},
    ]
if "chats" not in st.session_state:
    st.session_state.chats = {
        "María Gómez": ["Hola, ¿sigues paseando perros?", "Sí, claro 😊 ¿En qué comuna estás?"],
        "Pedro Ramírez": ["Gracias por tu ayuda, todo perfecto 👍"],
    }
if "perfil_propio" not in st.session_state:
    st.session_state.perfil_propio = {
        "nombre": "Ignacio",
        "edad": "XX",
        "descripcion": "Apasionado por ayudar y conectar personas. Confiable y responsable.",
        "servicios": ["Paseo de perros", "Cuidado por horas"],
        "valoracion": "★★★★☆",
    }

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
    div.stButton > button:hover { opacity: 0.95; transform: translateY(-1px); }
    .top-bar {
        position: fixed; top: 0; left: 0; right: 0; height: 64px;
        background-color: #2E8B57; color: white;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; font-weight: 700; z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .top-bar a { color: white; text-decoration: none; padding: 8px 16px; }
    .conecta-footer {
        position: fixed; bottom: 0; left: 0; right: 0; height: 72px;
        background-color: #ffffff; display: flex;
        justify-content: space-around; align-items: center;
        border-top: 1px solid rgba(0,0,0,0.08); z-index: 9999;
        box-shadow: 0 -4px 12px rgba(0,0,0,0.06);
    }
    .conecta-footer a {
        font-size: 26px; text-decoration: none; color: #333333;
        padding: 8px 16px; border-radius: 10px;
        display: flex; flex-direction: column; align-items: center;
    }
    .conecta-footer a div { font-size:11px; margin-top:4px; }
    .conecta-footer a:hover { background-color: rgba(0,0,0,0.03); }
    .main > div { margin-top: 90px; margin-bottom: 100px; }
    .conecta-title { text-align: center; margin-bottom: 8px; }
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
    st.markdown('<div class="top-bar"><a href="?pagina=inicio">ConectaServicios</a></div>', unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div class="conecta-footer">
        <a href="?pagina=chats">💬<div>Chats</div></a>
        <a href="?pagina=notificaciones">🔔<div>Notifs</div></a>
        <a href="?pagina=perfil_usuario">👤<div>Perfil</div></a>
    </div>""", unsafe_allow_html=True)

def agregar_notificacion(texto, tipo="mensaje"):
    """Agrega una notificación nueva al estado."""
    st.session_state.notificaciones.insert(0, {"tipo": tipo, "texto": texto, "leida": False})

# -------------------------
# TOPBAR
# -------------------------
render_topbar()

# ==========================================================
# PAGINAS
# ==========================================================

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
    st.write("Consejo: usa la barra inferior para acceder a Chats, Notificaciones o a tu Perfil.")
    render_footer()

# ---------- ACERCA ----------
elif st.session_state.pagina == "acerca":
    st.markdown('<h1 class="conecta-title">Acerca de Conecta</h1>', unsafe_allow_html=True)
    st.write("**Conecta** une a quienes buscan servicios con quienes los ofrecen.")
    volver("inicio")
    render_footer()

# ---------- SUBCATEGORIA ----------
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
    render_footer()

# ---------- UBICACION ----------
elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")
    comuna = st.selectbox("Comuna:", ["Providencia", "Ñuñoa", "Maipú", "Las Condes", "Santiago"])
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = comuna
        set_page("resultados")
    render_footer()

# ---------- RESULTADOS ----------
elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio} — {st.session_state.ubicacion}</h1>', unsafe_allow_html=True)
    volver("ubicacion")
    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "★★★★☆", "edad": 28},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "★★★★★", "edad": 32},
    ]
    for r in resultados:
        st.info(f"{r['nombre']} — {r['servicio']} — {r['valoracion']}")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")
    render_footer()

# ---------- PERFIL OTRO USUARIO ----------
elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write(f"**Edad:** {r['edad']} años")
    st.write(f"**Servicio:** {r['servicio']}")
    st.write(f"**Valoración:** {r['valoracion']}")
    mensaje = st.text_input("💬 Envía un mensaje:")
    if st.button("Enviar mensaje"):
        if mensaje.strip():
            agregar_notificacion(f"Nuevo mensaje enviado a {r['nombre']}: '{mensaje}'", tipo="mensaje")
            st.success("Mensaje enviado ✅")
    render_footer()

# ---------- 🔔 NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    notifs = st.session_state.notificaciones
    if not notifs:
        st.info("No tienes notificaciones nuevas.")
    else:
        for i, n in enumerate(notifs):
            color = "#e8ffe8" if not n["leida"] else "#f5f5f5"
            with st.container():
                st.markdown(f'<div style="padding:10px; background:{color}; border-radius:8px; margin-bottom:6px;">{n["texto"]}</div>', unsafe_allow_html=True)
                cols = st.columns(2)
                if cols[0].button("Marcar leída", key=f"leida_{i}"):
                    st.session_state.notificaciones[i]["leida"] = True
                    st.rerun()
                if cols[1].button("Eliminar", key=f"elim_{i}"):
                    st.session_state.notificaciones.pop(i)
                    st.rerun()
    render_footer()

# ---------- 💬 CHATS ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    chats = st.session_state.chats
    seleccion = st.selectbox("Selecciona una conversación:", ["--"] + list(chats.keys()))
    if seleccion != "--":
        st.subheader(f"Chat con {seleccion}")
        for msg in chats[seleccion]:
            st.markdown(f"💭 {msg}")
        nuevo = st.text_input("Escribe tu mensaje:")
        if st.button("Enviar"):
            if nuevo.strip():
                chats[seleccion].append(f"Tú: {nuevo}")
                agregar_notificacion(f"{seleccion} ha recibido tu mensaje: '{nuevo}'", tipo="mensaje")
                st.success("Mensaje enviado ✅")
                st.rerun()
    render_footer()

# ---------- 👤 PERFIL PROPIO ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    perfil = st.session_state.perfil_propio
    st.write(f"**Nombre:** {perfil['nombre']}")
    st.write(f"**Edad:** {perfil['edad']}")
    st.write(f"**Descripción:** {perfil['descripcion']}")
    st.write(f"**Servicios ofrecidos:** {', '.join(perfil['servicios'])}")
    st.write(f"**Valoración promedio:** {perfil['valoracion']}")
    render_footer()
