import streamlit as st

# ---- Configuración de la app ----
st.set_page_config(page_title="ConectaServicios", layout="wide")

# ---- CSS personalizado para la barra superior e inferior ----
st.markdown("""
    <style>
    /* Barra superior */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #2c3e50;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        font-weight: bold;
        z-index: 1000;
    }
    .top-bar:hover {
        cursor: pointer;
    }

    /* Contenido principal */
    .main-content {
        padding-top: 80px;  /* Espacio para la barra superior */
        padding-bottom: 80px; /* Espacio para la barra inferior */
    }

    /* Barra inferior fija */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #2c3e50;
        color: white;
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-size: 18px;
        z-index: 1000;
    }

    .bottom-item:hover {
        color: #1abc9c;
        cursor: pointer;
    }

    /* Botones tipo opción */
    .option-button {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
        background-color: #ecf0f1;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 20px;
        font-weight: 500;
        color: #2c3e50;
    }
    .option-button:hover {
        background-color: #dfe6e9;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)


# ---- Inicializar sesión ----
if "page" not in st.session_state:
    st.session_state.page = "home"

# ---- Función para cambiar de página ----
def go_to(page):
    st.session_state.page = page

# ---- Barra superior (logo/nombre app) ----
st.markdown(f"""
    <div class="top-bar" onclick="window.location.reload()">ConectaServicios</div>
""", unsafe_allow_html=True)


# ---- Contenido principal ----
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Pantalla principal
if st.session_state.page == "home":
    st.subheader("¿Qué servicio estás buscando?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cuidado de mascotas", use_container_width=True):
            go_to("categorias")
        if st.button("Cuidado de niños", use_container_width=True):
            go_to("categorias")
        if st.button("Limpieza", use_container_width=True):
            go_to("categorias")

    with col2:
        if st.button("Electricidad", use_container_width=True):
            go_to("categorias")
        if st.button("Plomería", use_container_width=True):
            go_to("categorias")
        if st.button("Otros servicios", use_container_width=True):
            go_to("categorias")

# Segunda pantalla: lista desplegable de categorías
elif st.session_state.page == "categorias":
    st.subheader("Selecciona el tipo de trabajo específico:")
    opciones = ["Pasear perros", "Cuidar gatos", "Entrenador", "Veterinario", "Peluquero de mascotas"]
    seleccion = st.selectbox("Selecciona una opción:", opciones)
    if st.button("Continuar"):
        go_to("ubicacion")

# Filtro de ubicación
elif st.session_state.page == "ubicacion":
    st.subheader("Selecciona tu ubicación")

    ciudad = st.selectbox("Ciudad", ["Santiago"])
    comuna = st.selectbox("Comuna", [
        "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba",
        "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina",
        "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
        "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel",
        "Quilicura", "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel",
        "San Ramón", "Santiago Centro", "Vitacura"
    ])
    if st.button("Buscar resultados"):
        go_to("resultados")

# Resultados
elif st.session_state.page == "resultados":
    st.subheader("Resultados en tu zona")
    st.write("• Juan Pérez — Paseador de perros (⭐ 4.8)")
    st.write("• María López — Cuidadora de mascotas (⭐ 4.9)")
    st.write("• Carlos Díaz — Entrenador canino (⭐ 4.7)")

# Pantallas inferiores
elif st.session_state.page == "chats":
    st.subheader("Chats")
    st.write("Aquí podrás comunicarte con las personas con las que coordinas servicios.")

elif st.session_state.page == "notificaciones":
    st.subheader("Notificaciones")
    st.write("Aquí verás cuando alguien se interese en tu perfil o te deje una valoración.")

elif st.session_state.page == "perfil":
    st.subheader("Tu perfil")
    st.write("Aquí podrás editar tu perfil, agregar trabajos previos y ver tus valoraciones.")


st.markdown('</div>', unsafe_allow_html=True)

# ---- Barra inferior fija ----
st.markdown(f"""
    <div class="bottom-bar">
        <div class="bottom-item" onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'chats'}}, '*');">💬 Chats</div>
        <div class="bottom-item" onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'notificaciones'}}, '*');">🔔 Notificaciones</div>
        <div class="bottom-item" onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'perfil'}}, '*');">👤 Perfil</div>
    </div>
""", unsafe_allow_html=True)

# ---- Detectar clics en la barra inferior ----
event = st.session_state.get("_component_value", None)
if event == "chats":
    go_to("chats")
elif event == "notificaciones":
    go_to("notificaciones")
elif event == "perfil":
    go_to("perfil")
