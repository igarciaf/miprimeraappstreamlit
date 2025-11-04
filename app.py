import streamlit as st

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# ESTADOS
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


# -------------------------
# CSS
# -------------------------
st.markdown("""
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
.footer-button {
    background: none;
    border: none;
    font-size: 26px;
    cursor: pointer;
}
.footer-label {
    font-size: 11px;
    margin-top: -6px;
    color: #333;
}
.main > div {
    margin-bottom: 100px;
}
.conecta-title {
    text-align: center;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)


# -------------------------
# FUNCIONES
# -------------------------
def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    st.rerun()

def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)

def render_footer():
    """Footer fijo con botones funcionales"""
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💬", key="footer_chat"):
            set_page("chats")
        st.markdown("<div class='footer-label' style='text-align:center;'>Chats</div>", unsafe_allow_html=True)
    with col2:
        if st.button("🔔", key="footer_notif"):
            set_page("notificaciones")
        st.markdown("<div class='footer-label' style='text-align:center;'>Notifs</div>", unsafe_allow_html=True)
    with col3:
        if st.button("👤", key="footer_perfil"):
            set_page("perfil_usuario")
        st.markdown("<div class='footer-label' style='text-align:center;'>Perfil</div>", unsafe_allow_html=True)


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

    st.markdown("---")
    st.write("Usa la barra inferior para acceder a tus chats, notificaciones o perfil.")
    render_footer()


elif st.session_state.pagina == "acerca":
    st.markdown('<h1 class="conecta-title">Acerca de Conecta</h1>', unsafe_allow_html=True)
    st.write("Conecta une personas que buscan servicios con quienes los ofrecen.")
    volver("inicio")
    render_footer()


elif st.session_state.pagina == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Selecciona un tipo de servicio:")

    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Adiestramiento"],
        "Hogar": ["Limpieza", "Jardinería", "Electricidad"],
        "Clases": ["Matemáticas", "Inglés", "Música"],
        "Niños": ["Cuidado por horas", "Apoyo escolar"]
    }

    seleccion = st.selectbox("Servicio:", ["-- Elige --"] + opciones.get(st.session_state.categoria, []))
    if seleccion != "-- Elige --":
        st.session_state.servicio = seleccion
        set_page("ubicacion")
    render_footer()


elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comunas_santiago = ["Ñuñoa", "Providencia", "Las Condes", "Maipú", "Puente Alto", "La Florida"]
    comuna = st.selectbox("Comuna:", comunas_santiago)

    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")
    render_footer()


elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio}</h1>', unsafe_allow_html=True)
    volver("ubicacion")

    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "★★★★☆", "edad": 28},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "★★★★★", "edad": 32},
    ]

    for r in resultados:
        st.info(f"{r['nombre']} — {r['valoracion']} — {r['edad']} años")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")
    render_footer()


elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario", "edad": "-", "valoracion": "—"}
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write(f"**Edad:** {r['edad']} años")
    st.write(f"**Valoración:** {r['valoracion']}")
    mensaje = st.text_input("Mensaje:")
    if st.button("Enviar mensaje"):
        if mensaje.strip():
            st.success("Mensaje enviado ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")
    render_footer()


elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí estarán tus conversaciones (simulación).")
    render_footer()


elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí verás tus notificaciones y valoraciones (simulación).")
    render_footer()


elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí puedes ver y editar tu información (simulación).")
    render_footer()
