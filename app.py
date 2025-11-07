import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Conecta", layout="wide")

# Estado inicial de navegación
if "page" not in st.session_state:
    st.session_state.page = "inicio"

def set_page(page):
    st.session_state.page = page
    st.experimental_rerun()

# Estilos CSS
st.markdown("""
    <style>
        body {
            background-color: #f8f9fa;
        }
        .main {
            padding-top: 1rem;
        }
        .header {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            background-color: white;
            padding: 10px 0;
            text-align: center;
            font-size: 30px;
            font-weight: 700;
            color: #333;
            border-bottom: 1px solid #ddd;
            z-index: 999;
        }
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: white;
            display: flex;
            justify-content: space-around;
            border-top: 1px solid #ddd;
            padding: 10px 0;
            z-index: 999;
        }
        .nav-button {
            text-align: center;
            font-size: 14px;
            color: #333;
        }
        .nav-button:hover {
            color: #007bff;
            cursor: pointer;
        }
        .service-card {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            text-align: center;
            transition: 0.2s;
        }
        .service-card:hover {
            transform: translateY(-4px);
            background-color: #f1f1f1;
        }
        .search-box {
            border-radius: 10px;
            border: 1px solid #ccc;
            padding: 0.5rem;
            width: 100%;
        }
        .space {
            height: 60px;
        }
    </style>
""", unsafe_allow_html=True)

# Header con el logo (botón al inicio)
st.markdown(
    f"""
    <div class="header" onclick="window.location.reload()">
        🤝 Conecta
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='space'></div>", unsafe_allow_html=True)

# --- Pantallas ---
if st.session_state.page == "inicio":
    st.markdown("### 🔍 Encuentra servicios cerca de ti")

    comunas_santiago = [
        "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba",
        "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina",
        "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
        "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura",
        "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón",
        "Santiago Centro", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo",
        "Colina", "Lampa", "Til Til", "San Bernardo", "Buin", "Calera de Tango", "Paine",
        "Melipilla", "María Pinto", "Curacaví", "Talagante", "El Monte", "Padre Hurtado", "Peñaflor"
    ]

    comuna = st.selectbox("Selecciona tu comuna:", comunas_santiago)

    st.text_input("¿Qué servicio buscas?", placeholder="Ej. cuidado de mascotas, jardinería, limpieza...", key="busqueda")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='service-card'>👩‍🍼 Niñera</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='service-card'>🐶 Paseador de perros</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='service-card'>🧹 Limpieza</div>", unsafe_allow_html=True)

elif st.session_state.page == "notificaciones":
    st.markdown("### 🔔 Notificaciones")
    st.info("Aún no tienes notificaciones nuevas.")

elif st.session_state.page == "chat":
    st.markdown("### 💬 Chat")
    st.write("Selecciona una conversación o inicia una nueva.")

elif st.session_state.page == "perfil":
    st.markdown("### 👤 Tu perfil")
    st.text_input("Nombre completo")
    st.text_input("Correo electrónico")
    st.text_area("Descripción o experiencia")
    st.button("Guardar cambios")

# --- Barra inferior fija ---
st.markdown("""
<div class='bottom-nav'>
    <div class='nav-button' onclick="window.location.href='?page=inicio'">🏠<br>Inicio</div>
    <div class='nav-button' onclick="window.location.href='?page=notificaciones'">🔔<br>Notificaciones</div>
    <div class='nav-button' onclick="window.location.href='?page=chat'">💬<br>Chat</div>
    <div class='nav-button' onclick="window.location.href='?page=perfil'">👤<br>Perfil</div>
</div>
""", unsafe_allow_html=True)
