import streamlit as st

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="centered")

# --- ESTADO DE NAVEGACIÓN ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "categoria" not in st.session_state:
    st.session_state.categoria = None

# --- FUNCIÓN PARA VOLVER ATRÁS ---
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

# --- PANTALLA SUBCATEGORÍAS ---
elif st.session_state.pagina == "subcategoria":
    st.title(f"Categoría: {st.session_state.categoria}")
    volver("inicio")

    st.write("Selecciona un tipo de servicio específico:")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico"],
        "Clases": ["Matemáticas", "Inglés", "Música"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas"]
    }

    for opcion in opciones[st.session_state.categoria]:
        if st.button(opcion):
            st.session_state.servicio = opcion
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

    st.write("Aquí aparecería la lista de personas que ofrecen este servicio cerca de ti.")
    st.info("Ejemplo: Juan Pérez - Paseador de perros 🐶 - ★★★★☆")

    if st.button("Ver perfil"):
        st.session_state.pagina = "perfil"
        st.rerun()

# --- PANTALLA PERFIL ---
elif st.session_state.pagina == "perfil":
    st.title("👤 Perfil del oferente")
    volver("resultados")

    st.write("**Nombre:** Juan Pérez")
    st.write("**Edad:** 28 años")
    st.write("**Servicio:** Paseador de perros")
    st.write("**Valoración:** ⭐⭐⭐⭐☆ (4.5/5)")
    st.write("**Descripción:** Amante de los animales, con 3 años de experiencia.")

    st.subheader("💬 Chat con Juan")
    mensaje = st.text_input("Escribe un mensaje...")
    if st.button("Enviar"):
        if mensaje.strip():
            st.success("Mensaje enviado correctamente ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")
