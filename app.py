# app.py
import streamlit as st

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# LEER QUERY PARAMS (si vienen)
# -------------------------
query_params = st.experimental_get_query_params()
if "pagina" in query_params:
    # mantener coherencia: si la URL trae ?pagina=X, lo usamos
    st.session_state.pagina = query_params["pagina"][0]

# -------------------------
# ESTADO POR DEFECTO
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
# CSS: botones uniformes + footer fijo
# -------------------------
st.markdown(
    """
    <style>
    /* -- botones grandes uniformes (los que crea Streamlit) -- */
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

    /* -- footer fijo -- */
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
    .conecta-footer a {
        font-size: 26px;
        text-decoration: none;
        color: #333333;
        padding: 8px 16px;
        border-radius: 10px;
    }
    .conecta-footer a:hover {
        background-color: rgba(0,0,0,0.03);
    }

    /* dejar espacio inferior para que el contenido no quede debajo del footer */
    .main > div {
        margin-bottom: 100px;
    }

    /* Opcional: estilo para títulos centrados */
    .conecta-title {
        text-align: center;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# HELPERS
# -------------------------
def set_page(pagina_name):
    """Cambia la página en session_state y actualiza la URL (query param)"""
    st.session_state.pagina = pagina_name
    # actualizamos query params para que, si se recarga, mantenga la pantalla
    st.experimental_set_query_params(pagina=pagina_name)
    st.rerun()


def volver(pagina_destino="inicio"):
    """Botón volver (usa st.button normal)"""
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)


def render_footer():
    """Renderiza el footer fijo como HTML con enlaces que usan query params.
       Al hacer click la página recarga la app con ?pagina=... y la app lee ese param.
       Esto evita duplicar botones en el layout principal (los íconos solo aparecen en el footer)."""
    footer_html = """
    <div class="conecta-footer">
        <a href="?pagina=chats" title="Chats">💬<div style="font-size:11px;">Chats</div></a>
        <a href="?pagina=notificaciones" title="Notificaciones">🔔<div style="font-size:11px;">Notifs</div></a>
        <a href="?pagina=perfil_usuario" title="Mi perfil">👤<div style="font-size:11px;">Perfil</div></a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# -------------------------
# PANTALLAS
# -------------------------

# ---------- INICIO ----------
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
    st.write("Consejo: usa la barra inferior para acceder rápidamente a Chats, Notificaciones o a tu Perfil.")
    render_footer()


# ---------- ACERCA ----------
elif st.session_state.pagina == "acerca":
    st.markdown('<h1 class="conecta-title">Acerca de Conecta</h1>', unsafe_allow_html=True)
    st.write(
        """
        **Conecta** es una app pensada para unir a personas que buscan servicios
        con quienes los ofrecen.  
        Puedes crear tu perfil, mostrar trabajos previos y contactar directamente.
        """
    )
    volver("inicio")
    render_footer()


# ---------- SUBCATEGORIAS (selectbox) ----------
elif st.session_state.pagina == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Selecciona un tipo de servicio:")

    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
    }

    seleccion = st.selectbox("Selecciona el servicio:", ["-- Elige una opción --"] + opciones.get(st.session_state.categoria, []))
    if seleccion != "-- Elige una opción --":
        st.session_state.servicio = seleccion
        set_page("ubicacion")

    render_footer()


# ---------- UBICACIÓN (Ciudad + Comuna) ----------
elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
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
            set_page("resultados")

    render_footer()


# ---------- RESULTADOS ----------
elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio} — {st.session_state.ubicacion}</h1>', unsafe_allow_html=True)
    volver("ubicacion")

    # lista simulada (cada oferente tiene lista de comunas donde trabaja)
    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "★★★★☆", "edad": 28, "comunas": ["Providencia", "Ñuñoa"]},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "★★★★★", "edad": 32, "comunas": ["Las Condes", "Providencia"]},
        {"nombre": "Pedro Ramírez", "servicio": st.session_state.servicio, "valoracion": "★★★☆☆", "edad": 24, "comunas": ["Maipú", "Santiago"]},
    ]

    comuna_actual = st.session_state.get("ubicacion", "").split(",")[0]
    # mostrar solo quienes trabajan en la comuna actual; si ninguno, mostrar todos (esto es demo)
    mostrados = [r for r in resultados if comuna_actual in r.get("comunas", [])]
    if not mostrados:
        st.info("No hay coincidencias exactas en tu comuna; mostrando resultados cercanos.")
        mostrados = resultados

    for r in mostrados:
        st.info(f"{r['nombre']}  —  {r['servicio']}  —  {r['valoracion']}  —  {r['edad']} años")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")

    render_footer()


# ---------- PERFIL DE OTRO USUARIO ----------
elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario", "edad": "-", "servicio": "-", "valoracion": "—"}
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")

    st.write(f"**Edad:** {r.get('edad','-')} años")
    st.write(f"**Servicio:** {r.get('servicio','-')}")
    st.write(f"**Valoración:** {r.get('valoracion','-')}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio (simulación).")

    st.subheader("💬 Chat")
    mensaje = st.text_input("Escribe un mensaje...")
    if st.button("Enviar mensaje"):
        if mensaje.strip():
            st.success("Mensaje enviado correctamente ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")

    render_footer()


# ---------- CHATS (desde footer) ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí estarán tus conversaciones (simulación).")
    render_footer()


# ---------- NOTIFICACIONES (desde footer) ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí verás cuando alguien visite tu perfil o deje una valoración (simulación).")
    render_footer()


# ---------- PERFIL PROPIO (desde footer) ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("Aquí puedes ver y editar tu información (simulación).")
    # ejemplo de datos propios
    st.write("**Nombre:** Ignacio")
    st.write("**Edad:**  XX")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas (ejemplo)")
    render_footer()
