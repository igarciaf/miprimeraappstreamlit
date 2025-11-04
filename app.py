import streamlit as st

# Configuración general
st.set_page_config(page_title="Conecta", layout="wide")

# ---- CSS para la barra superior e inferior ----
st.markdown("""
    <style>
    /* Barra superior fija */
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: white;
        border-bottom: 1px solid #ddd;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    .top-bar button {
        background: none;
        border: none;
        font-size: 28px;
        font-weight: bold;
        color: #333;
        cursor: pointer;
    }
    .top-bar button:hover {
        color: #0078ff;
    }

    /* Contenido principal */
    .main-content {
        padding-top: 80px;
        padding-bottom: 80px;
    }

    /* Barra inferior */
    .bottom-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: white;
        border-top: 1px solid #ddd;
        display: flex;
        justify-content: space-around;
        align-items: center;
        z-index: 1000;
    }
    .bottom-bar button {
        background: none;
        border: none;
        font-size: 18px;
        color: #555;
        cursor: pointer;
    }
    .bottom-bar button:hover {
        color: #0078ff;
    }
    </style>
""", unsafe_allow_html=True)


# ---- Estado inicial ----
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page):
    st.session_state.page = page


# ---- Barra superior (nombre como botón) ----
st.markdown("""
<div class="top-bar">
    <form action="#" method="get">
        <button name="home" type="submit" onclick="window.parent.postMessage({type: 'streamlit_setComponentValue', value: 'home'}, '*');">🤝 Conecta</button>
    </form>
</div>
""", unsafe_allow_html=True)


# ---- Contenido principal ----
st.markdown('<div class="main-content">', unsafe_allow_html=True)

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

elif st.session_state.page == "categorias":
    st.subheader("Selecciona el tipo de trabajo específico:")
    opciones = ["Pasear perros", "Cuidar gatos", "Entrenador", "Veterinario", "Peluquero de mascotas"]
    seleccion = st.selectbox("Selecciona una opción:", opciones)
    if st.button("Continuar"):
        go_to("ubicacion")

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

elif st.session_state.page == "resultados":
    st.subheader("Resultados en tu zona")
    st.write("• Juan Pérez — Paseador de perros (⭐ 4.8)")
    st.write("• María López — Cuidadora de mascotas (⭐ 4.9)")
    st.write("• Carlos Díaz — Entrenador canino (⭐ 4.7)")

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


# ---- Barra inferior ----
st.markdown(f"""
    <div class="bottom-bar">
        <button onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'chats'}}, '*');">💬 Chats</button>
        <button onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'notificaciones'}}, '*');">🔔 Notificaciones</button>
        <button onclick="window.parent.postMessage({{type: 'streamlit_setComponentValue', value: 'perfil'}}, '*');">👤 Perfil</button>
    </div>
""", unsafe_allow_html=True)

# ---- Detección de clics ----
event = st.session_state.get("_component_value", None)
if event == "chats":
    go_to("chats")
elif event == "notificaciones":
    go_to("notificaciones")
elif event == "perfil":
    go_to("perfil")
elif event == "home":
    go_to("home")
