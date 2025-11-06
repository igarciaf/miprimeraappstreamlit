import streamlit as st

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="ConectaServicios", layout="wide")

# --- ESTADOS INICIALES ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []  # lista para mensajes del chat


def cambiar_pagina(pagina):
    st.session_state.pagina = pagina


# --- ENCABEZADO FIJO ---
st.markdown(
    """
    <div style="position:fixed; top:0; left:0; right:0; height:60px; 
                background-color:white; border-bottom:1px solid #ddd; 
                display:flex; align-items:center; justify-content:center; 
                z-index:1000;">
        <h2 style="margin:0; cursor:pointer;" onclick="window.location.reload()">ConectaServicios</h2>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown("<div style='height:70px'></div>", unsafe_allow_html=True)


# --- CONTENIDO SEGÚN PANTALLA ---
if st.session_state.pagina == "inicio":
    st.title("Encuentra o publica servicios cerca de ti")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Buscar servicios"):
            cambiar_pagina("servicios")
    with col2:
        if st.button("Ofrecer un servicio"):
            cambiar_pagina("ofrecer")

elif st.session_state.pagina == "notificaciones":
    st.subheader("🔔 Notificaciones")
    st.markdown("---")
    st.write("✅ Tu perfil fue visitado por @usuario123")
    st.write("💬 Tienes una nueva reseña en tu último trabajo")
    st.write("⭐ Recibiste una valoración de 5 estrellas")
    if st.button("Volver"):
        cambiar_pagina("inicio")

elif st.session_state.pagina == "perfil":
    st.subheader("👤 Mi Perfil")
    st.markdown("---")
    st.write("Nombre: Ignacio García")
    st.write("Edad: 23")
    st.write("Servicios ofrecidos: Pasear perros, jardinería, limpieza")
    st.write("Valoración promedio: ⭐⭐⭐⭐☆ (4.5)")
    if st.button("Volver"):
        cambiar_pagina("inicio")

elif st.session_state.pagina == "chat":
    st.subheader("💬 Chat con usuarios")
    st.markdown("---")

    # Mostrar los mensajes enviados
    if st.session_state.mensajes:
        for msg in st.session_state.mensajes:
            if msg["usuario"] == "Tú":
                st.markdown(f"<div style='text-align:right; background-color:#DCF8C6; padding:8px; border-radius:10px; margin:4px;'>**{msg['usuario']}:** {msg['texto']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left; background-color:#F1F0F0; padding:8px; border-radius:10px; margin:4px;'>**{msg['usuario']}:** {msg['texto']}</div>", unsafe_allow_html=True)
    else:
        st.info("No tienes mensajes todavía.")

    # Input para escribir mensaje
    mensaje = st.text_input("Escribe tu mensaje...", key="mensaje_chat")

    # Enviar mensaje con Enter o botón
    col1, col2 = st.columns([4, 1])
    with col1:
        pass
    with col2:
        if st.button("Enviar") and mensaje.strip():
            st.session_state.mensajes.append({"usuario": "Tú", "texto": mensaje})
            st.session_state.mensaje_chat = ""  # limpia el campo
            st.rerun()

    if st.button("Volver"):
        cambiar_pagina("inicio")


# --- BARRA INFERIOR FIJA ---
st.markdown(
    """
    <div style="position:fixed; bottom:0; left:0; right:0; height:70px;
                background-color:white; border-top:1px solid #ddd; 
                display:flex; align-items:center; justify-content:space-around;
                z-index:1000;">
        <div style="text-align:center; cursor:pointer;" onclick="window.parent.postMessage('chat','*')">💬<br>Chat</div>
        <div style="text-align:center; cursor:pointer;" onclick="window.parent.postMessage('notificaciones','*')">🔔<br>Notificaciones</div>
        <div style="text-align:center; cursor:pointer;" onclick="window.parent.postMessage('perfil','*')">👤<br>Perfil</div>
    </div>

    <script>
    window.addEventListener("message", (event) => {
        if (event.data === "chat") {
            window.location.search = "?pagina=chat";
        } else if (event.data === "notificaciones") {
            window.location.search = "?pagina=notificaciones";
        } else if (event.data === "perfil") {
            window.location.search = "?pagina=perfil";
        }
    });
    </script>
    """,
    unsafe_allow_html=True
)
