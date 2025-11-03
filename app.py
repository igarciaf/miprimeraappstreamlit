import streamlit as st

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="centered")

# --- ESTILO CSS PARA BOTONES UNIFORMES ---
st.markdown("""
<style>
div.stButton > button {
    height: 80px;
    width: 200px;
    background-color: #4CAF50;
    color: white;
    border-radius: 12px;
    font-size: 18px;
    margin: 5px 10px;
}
div.stButton > button:hover {
    background-color: #45a049;
}
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE NAVEGACIÓN ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "categoria" not in st.session_state:
    st.session_state.categoria = None

# --- FUNCIONES AUXILIARES ---
def volver(pagina):
    if st.button("⬅️ Volver"):
        st.session_state.pagina = pagina
        st.rerun()

# --- FUNCION PARA FOOTER TIPO INSTAGRAM ---
def barra_inferior():
    st.markdown("---")  # separador visual
    col1, col2, col3 = st.columns([1,1,1])

    with col1:  # izquierda - chats
        if st.button("💬"):
            st.session_state.pagina = "chats"
            st.rerun()
    with col2:  # centro - notificaciones
        if st.button("🔔"):
            st.session_state.pagina = "notificaciones"
            st.rerun()
    with col3:  # derecha - perfil
        if st.button("👤"):
            st.session_state.pagina = "perfil_usuario"
            st.rerun()

# --- PANTALLA INICIO ---
if st.session_state.pagina == "inicio":
    st.title("🤝 Conecta")
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")

    if st.button("Acerca de"):
        st.session_state.pagina = "acerca"

    st.subheader("Selecciona una categoría:")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Cuidado de mascotas"):
            st.session_state.categoria = "Mascotas"
            st.session_state.pagina = "subcategoria"
        if st.button("Limpieza y hogar"):
            st.session_state.categoria = "Hogar"
            st.session_state.pagina = "subcategoria"

    with col2:
        if st.button("Clases particulares"):
            st.session_state.categoria = "Clases"
            st.session_state.pagina = "subcategoria"
        if st.button("Cuidado de niños"):
            st.session_state.categoria = "Niños"
            st.session_state.pagina = "subcategoria"

    barra_inferior()

# --- PANTALLA ACERCA DE ---
elif st.session_state.pagina == "acerca":
    st.title("Acerca de Conecta")
    st.write("""
    **Conecta** es una aplicación pensada para unir a personas que buscan
    servicios con quienes los ofrecen.  
    Puedes crear tu perfil, mostrar tus trabajos y contactar directamente
    con otros usuarios de tu zona.
    """)
    volver("inicio")
    barra_inferior()

# --- PANTALLA SUBCATEGORÍAS SOLO LISTA DESPLEGABLE ---
elif st.session_state.pagina == "subcategoria":
    st.title(f"Categoría: {st.session_state.categoria}")
    volver("inicio")
    st.write("Selecciona un tipo de servicio:")

    # Diccionario de subcategorías
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
    }

    seleccion = st.selectbox("Selecciona el servicio:", ["-- Elige una opción --"] + opciones[st.session_state.categoria])
    if seleccion != "-- Elige una opción --":
        st.session_state.servicio = seleccion
        st.session_state.pagina = "ubicacion"
        st.rerun()

    barra_inferior()

# --- PANTALLA UBICACIÓN (CIUDAD Y COMUNA) ---
elif st.session_state.pagina == "ubicacion":
    st.title("📍 Selecciona tu ubicación")
    volver("subcategoria")

    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comunas_santiago = [
        "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central",
        "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja",
        "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo",
        "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén",
        "Providencia", "Pudahuel", "Quilicura", "Quinta Normal", "Recoleta",
        "Renca", "San Joaquín", "San Miguel", "San Ramón", "Vitacura", "San Bernardo",
        "Puente Alto", "Pirque", "San José de Maipo", "Colina", "Lampa", "Tiltil"
    ]
    comuna = st.selectbox("Comuna:", comunas_santiago)

    if st.button("Buscar resultados"):
        if not ciudad or not comuna:
            st.error("Por favor selecciona ciudad y comuna válidas.")
        else:
            st.session_state.ubicacion = f"{comuna}, {ciudad}"
            st.session_state.pagina = "resultados"
            st.rerun()

    barra_inferior()

# --- PANTALLA RESULTADOS ---
elif st.session_state.pagina == "resultados":
    st.title(f"Resultados para '{st.session_state.servicio}' en {st.session_state.ubicacion}")
    volver("ubicacion")

    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "★★★★☆", "edad": 28},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "★★★★★", "edad": 32},
        {"nombre": "Pedro Ramírez", "servicio": st.session_state.servicio, "valoracion": "★★★☆☆", "edad": 24},
    ]

    for r in resultados:
        st.info(f"{r['nombre']} - {r['servicio']} - {r['valoracion']} - {r['edad']} años")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            st.session_state.pagina = "perfil"
            st.rerun()

    barra_inferior()

# --- PANTALLA PERFIL Y CHAT ---
elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario
    st.title(f"👤 Perfil de {r['nombre']}")
    volver("resultados")

    st.write(f"**Edad:** {r['edad']} años")
    st.write(f"**Servicio:** {r['servicio']}")
    st.write(f"**Valoración:** {r['valoracion']}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio.")

    st.subheader("💬 Chat")
    mensaje = st.text_input("Escribe un mensaje...")
    if st.button("Enviar mensaje"):
        if mensaje.strip():
            st.success("Mensaje enviado correctamente ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")

    barra_inferior()

# --- PANTALLA CHATS ---
elif st.session_state.pagina == "chats":
    st.title("💬 Chats")
    volver("inicio")
    st.write("Aquí estarán todos tus chats con usuarios.")
    barra_inferior()

# --- PANTALLA NOTIFICACIONES ---
elif st.session_state.pagina == "notificaciones":
    st.title("🔔 Notificaciones")
    volver("inicio")
    st.write("Aquí recibirás alertas cuando alguien vea tu perfil o deje una reseña.")
    barra_inferior()

# --- PANTALLA PERFIL PROPIO ---
elif st.session_state.pagina == "perfil_usuario":
    st.title("👤 Mi Perfil")
    volver("inicio")
    st.write("Aquí puedes editar tu perfil, ver tus valoraciones y trabajos realizados.")
    barra_inferior()
