import streamlit as st

# Configuración inicial de la app
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="centered")

# Inicializar el estado de navegación
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# -------------------------------
# FUNCIONES DE INTERFAZ
# -------------------------------

def render_topbar():
    """Barra superior fija con el nombre de la app (texto). Al hacer clic va al inicio."""
    top_html = """
    <style>
    /* Barra superior fija */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 700;
        z-index: 9999;
        border-bottom: 1px solid #ddd;
    }
    .top-bar a {
        color: inherit;
        text-decoration: none;
        padding: 8px 12px;
    }
    .top-bar a:hover {
        opacity: 0.8;
        cursor: pointer;
    }
    /* Ajuste del contenido para que no quede debajo */
    .main-content {
        margin-top: 80px;
        margin-bottom: 80px;
    }
    </style>

    <div class="top-bar">
        <a href="?pagina=inicio">🤝 Conecta</a>
    </div>
    """
    st.markdown(top_html, unsafe_allow_html=True)


def render_bottombar():
    """Barra inferior fija con los íconos de navegación."""
    bottom_html = """
    <style>
    /* Barra inferior fija */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 65px;
        background-color: white;
        border-top: 1px solid #ddd;
        display: flex;
        align-items: center;
        justify-content: space-around;
        z-index: 9999;
    }
    .bottom-icon {
        font-size: 24px;
        text-decoration: none;
        color: black;
        transition: transform 0.1s ease-in-out;
    }
    .bottom-icon:hover {
        transform: scale(1.1);
        opacity: 0.8;
    }
    </style>

    <div class="bottom-bar">
        <a class="bottom-icon" href="?pagina=chats">💬</a>
        <a class="bottom-icon" href="?pagina=notificaciones">🔔</a>
        <a class="bottom-icon" href="?pagina=perfil">👤</a>
    </div>
    """
    st.markdown(bottom_html, unsafe_allow_html=True)


# -------------------------------
# PANTALLAS
# -------------------------------

def pantalla_inicio():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Encuentra o publica servicios")

    # Simulación del buscador
    comuna = st.text_input("Busca servicios en tu comuna:", "")
    if comuna:
        st.write(f"Mostrando resultados para **{comuna}**...")

    # Botones de ejemplo para acceder a otras secciones
    if st.button("Ver categorías disponibles"):
        st.session_state.pagina = "buscador"

    st.markdown("</div>", unsafe_allow_html=True)


def pantalla_buscador():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Selecciona una categoría")

    opciones = ["Cuidado de niños", "Paseo de perros", "Limpieza", "Electricista", "Jardinería"]
    seleccion = st.selectbox("Filtra servicios", opciones)

    if seleccion:
        st.write(f"Mostrando personas que ofrecen **{seleccion}** en tu zona.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"

    st.markdown("</div>", unsafe_allow_html=True)


def pantalla_chats():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("💬 Tus chats")
    st.write("Aquí verás tus conversaciones con personas que ofrecen o buscan servicios.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)


def pantalla_notificaciones():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("🔔 Notificaciones")
    st.write("Aquí recibirás avisos cuando alguien vea tu perfil o te deje una reseña.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)


def pantalla_perfil():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("👤 Tu perfil")
    st.write("Aquí podrás editar tu información, ver tus trabajos y tus valoraciones.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)


# -------------------------------
# RENDER PRINCIPAL
# -------------------------------

render_topbar()

pagina_actual = st.session_state.pagina

if "pagina" in st.query_params:
    pagina_actual = st.query_params["pagina"]

# Render según la página actual
if pagina_actual == "inicio":
    pantalla_inicio()
elif pagina_actual == "buscador":
    pantalla_buscador()
elif pagina_actual == "chats":
    pantalla_chats()
elif pagina_actual == "notificaciones":
    pantalla_notificaciones()
elif pagina_actual == "perfil":
    pantalla_perfil()
else:
    pantalla_inicio()

render_bottombar()
