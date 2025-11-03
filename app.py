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

# --- PANTALLA SUBCATEGORÍAS CON BUSCADOR ---
elif st.session_state.pagina == "subcategoria":
    st.title(f"Categoría: {st.session_state.categoria}")
    volver("inicio")

    st.write("Selecciona un tipo de servicio específico o busca uno:")

    # Diccionario de subcategorías
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
    }

    # Buscador
    busqueda = st.text_input("🔍 Buscar servicio:")
    subcategorias_filtradas = [s for s in opciones[st.session_state.categoria] if busqueda.lower() in s.lower()]

    if not subcategorias_filtradas:
        st.info("No se encontraron resultados para tu búsqueda.")
    else:
        # Mostrar en columnas uniformes
        num_columnas = 2
        for i in range(0, len(subcategorias_filtradas), num_columnas):
            cols = st.columns(num_columnas)
            for j, sub in enumerate(subcategorias_filtradas[i:i+num_columnas]):
                if cols[j].button(sub):
                    st.session_state.servicio = sub
                    st.session_state.pagina = "ubicacion"
                    st.rerun()

# --- PANTALLA UBICACIÓN ---
elif st.session_state.pagina == "ubicacion":
    st.title("📍 Selecciona tu ubicación")
    volver("subcategoria")

    ubicacion = st.text_input("Ingresa tu comuna o ciudad:")
    if st.button("Buscar resultados"):
        if not ubicacion.strip():
            st.error("Por favor ingresa una ubicación válida.")
        else:
            st.session_state.ubicacion = ubicacion
            st.session_state.pagina = "resultados"
            st.rerun()

# --- PANTALLA RESULTADOS ---
elif st.session_state.pagina == "resultados":
    st.title(f"Resultados para '{st.session_state.servicio}' en {st.session_state.ubicacion}")
    volver("ubicacion")

    # Lista simulada de resultados
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
