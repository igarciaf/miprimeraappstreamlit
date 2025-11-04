import streamlit as st

# Configuración inicial
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="centered")

# Estado inicial
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

# --- FUNCIONES DE INTERFAZ ---

def barra_superior():
    st.markdown("""
    <style>
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        border-bottom: 1px solid #ddd;
        z-index: 9999;
        font-size: 24px;
        font-weight: bold;
    }
    .top-bar a {
        text-decoration: none;
        color: black;
    }
    .top-bar a:hover {
        opacity: 0.8;
        cursor: pointer;
    }
    .main-content {
        margin-top: 80px;
        margin-bottom: 80px;
    }
    </style>
    <div class="top-bar">
        <a href="#" onclick="window.location.reload()">🤝 Conecta</a>
    </div>
    """, unsafe_allow_html=True)

def barra_inferior():
    st.markdown("""
    <style>
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 65px;
        background-color: white;
        border-top: 1px solid #ddd;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 9999;
    }
    .bottom-icon {
        font-size: 25px;
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
    """, unsafe_allow_html=True)

# --- PANTALLAS ---

def pantalla_inicio():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Encuentra o publica servicios")
    st.write("Selecciona una opción para comenzar:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Buscar servicios"):
            st.session_state.pagina = "buscador"
    with col2:
        if st.button("Ofrecer servicios"):
            st.session_state.pagina = "buscador"

    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_buscador():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Selecciona una categoría")

    with st.expander("Abrir lista de servicios disponibles"):
        opciones = ["Cuidado de niños", "Paseo de perros", "Limpieza", "Electricista", "Jardinería"]
        seleccion = st.radio("Elige una opción:", opciones)
        if seleccion:
            st.write(f"Has seleccionado **{seleccion}**")

    if st.button("Siguiente"):
        st.session_state.pagina = "ubicacion"

    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"

    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_ubicacion():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Selecciona tu ubicación")

    ciudades = ["Santiago"]
    comunas = [
        "Las Condes", "Providencia", "Ñuñoa", "La Florida", "Puente Alto", "Maipú", 
        "Recoleta", "Santiago Centro", "Vitacura", "Peñalolén"
    ]

    ciudad = st.selectbox("Ciudad:", ciudades)
    comuna = st.selectbox("Comuna:", comunas)

    if st.button("Ver resultados"):
        st.session_state.pagina = "resultados"

    if st.button("Volver"):
        st.session_state.pagina = "buscador"

    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_resultados():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("Resultados encontrados")

    resultados = [
        {"nombre": "María López", "servicio": "Paseo de perros", "valoración": 4.8},
        {"nombre": "Carlos Pérez", "servicio": "Electricista", "valoración": 4.5},
        {"nombre": "Ana Torres", "servicio": "Limpieza", "valoración": 4.9},
    ]

    for r in resultados:
        st.markdown(f"**{r['nombre']}** — {r['servicio']} ⭐ {r['valoración']}")

    if st.button("Volver"):
        st.session_state.pagina = "ubicacion"

    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_chats():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("💬 Chats")
    st.write("Aquí verás tus conversaciones.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_notificaciones():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("🔔 Notificaciones")
    st.write("Aquí recibirás tus notificaciones.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)

def pantalla_perfil():
    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    st.title("👤 Perfil")
    st.write("Aquí podrás ver y editar tu información.")
    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
    st.markdown("</div>", unsafe_allow_html=True)

# --- NAVEGACIÓN ---

barra_superior()

pagina = st.session_state.pagina

if "pagina" in st.query_params:
    pagina = st.query_params["pagina"]

if pagina == "inicio":
    pantalla_inicio()
elif pagina == "buscador":
    pantalla_buscador()
elif pagina == "ubicacion":
    pantalla_ubicacion()
elif pagina == "resultados":
    pantalla_resultados()
elif pagina == "chats":
    pantalla_chats()
elif pagina == "notificaciones":
    pantalla_notificaciones()
elif pagina == "perfil":
    pantalla_perfil()
else:
    pantalla_inicio()

barra_inferior()
