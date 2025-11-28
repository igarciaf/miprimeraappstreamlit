# app.py — Archivo principal de la aplicación Streamlit

# Importamos Streamlit, que es la librería que permite crear la interfaz web
import streamlit as st
# Importamos nuestros archivos internos:
# - db: manejo de base de datos SQLite
# - auth: sistema de registro e inicio de sesión
import db
import auth
# Importamos datetime para trabajar con fechas y horas
from datetime import datetime
# Inicializa la base de datos: crea las tablas si no existen
db.init_db()
# Configuración inicial de la página de Streamlit:
# - Título de la ventana
# - Icono
# - Diseño ancho para que todo se vea más cómodo
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Helpers / rerun
# -------------------------

def rerun_safe():
    """Vuelve a ejecutar la app completa de forma segura.
    Se usa después de cambiar valores en session_state para actualizar la pantalla."""
    st.rerun()


def current_user_id():
    """Obtiene el ID del usuario actualmente logueado.
    
    Busca primero en session_state["user_id"].
    Si no está, revisa session_state["user"] (que es un dict con info del usuario).
    Si tampoco existe, devuelve None.
    """
    uid = st.session_state.get("user_id")
    if uid:  # Si se guardó directamente el user_id, lo devuelve
        return uid
    
    u = st.session_state.get("user")
    # Si hay un diccionario con datos del usuario, toma el id desde ahí
    if isinstance(u, dict) and u.get("id"):
        return u.get("id")
    
    # Si no hay sesión iniciada, devuelve None
    return None

def current_user_name():
    """Devuelve el nombre del usuario actualmente en sesión (si existe)."""
    
    # Primero intenta obtener el usuario almacenado directamente en session_state["user"]
    u = st.session_state.get("user")
    
    # Si existe un diccionario de usuario y tiene un nombre, lo devuelve al tiro
    if isinstance(u, dict) and u.get("nombre"):
        return u.get("nombre")

    # Si no está en session_state["user"], intenta obtener el ID del usuario conectado
    uid = current_user_id()
    
    if uid:
        # Busca al usuario en la base de datos
        row = db.get_user_by_id(uid)
        if row:
            # Devuelve el nombre; si no tiene nombre, devuelve su email como fallback
            return row.get("nombre") or row.get("email")

    # Si no hay usuario logueado, devuelve None
    return None
# -------------------------
# Valores por defecto para session_state
# -------------------------

# Diccionario con todos los valores iniciales de la sesión
defaults = {
    "page": "inicio",                 # Página actual que está viendo el usuario
    "user": None,                     # Datos completos del usuario logueado
    "user_id": 0,                     # ID del usuario (modo rápido)
    "selected_user_id": None,         # Usuario seleccionado en chats o perfiles

    "categoria": None,                # Categoría seleccionada al buscar
    "servicio": None,                 # Servicio seleccionado
    "ubicacion": None,                # Ubicación seleccionada

    "publish_cat": None,              # Categoría en creación de publicación
    "publish_service": None,          # Servicio en creación de publicación

    # --- Filtros de búsqueda ---
    "search_term": "",                # Palabra clave de la búsqueda
    "search_comuna": "",              # Comuna que filtra resultados
    "results_filter_price_min": "",   # Filtro: precio mínimo
    "results_filter_price_max": "",   # Filtro: precio máximo
    "results_filter_rating_min": "",  # Filtro: calificación mínima

    # --- Sistema de trabajos ---
    "solicitar_servicio_id": None,    # ID del servicio que el usuario quiere solicitar
    "solicitar_trabajador_id": None,  # ID del trabajador al que se le pedirá el servicio
    "ver_trabajo_id": None,           # ID de un trabajo para verlo en detalle
    "show_new_chat_selector": False,  # Muestra selector para iniciar chat nuevo
}

# Inicializa cada valor solo si no existe ya en session_state
for k, v in defaults.items():
    st.session_state.setdefault(k, v)



# -------------------------
# Comunas (lista completa de Santiago)
# -------------------------
# Esta es una lista fija de comunas que usaremos en los filtros de búsqueda
# y en los formularios donde el usuario elige de qué comuna es o dónde ofrece un servicio.
comunas_santiago = [
    "Cerrillos","Cerro Navia","Conchalí","El Bosque","Estación Central","Huechuraba",
    "Independencia","La Cisterna","La Florida","La Granja","La Pintana","La Reina",
    "Las Condes","Lo Barnechea","Lo Espejo","Lo Prado","Macul","Maipú","Ñuñoa",
    "Pedro Aguirre Cerda","Peñalolén","Providencia","Pudahuel","Quilicura",
    "Quinta Normal","Recoleta","Renca","San Joaquín","San Miguel","San Ramón",
    "Santiago","Vitacura","Puente Alto","Pirque","San José de Maipo","Colina",
    "Lampa","Tiltil","San Bernardo","Buin","Calera de Tango","Paine","Melipilla",
    "María Pinto","Curacaví","Talagante","El Monte","Padre Hurtado","Peñaflor"
]


# -------------------------
# Top bar (logo/nombre) y home button
# -------------------------

# Se agrega CSS personalizado para crear una barra fija arriba de la pantalla
# Esta barra funciona como encabezado de la app y le da una identidad visual.
st.markdown(
    """
    <style>
    .top-bar{
        position:fixed; top:0; left:0; right:0; height:64px;
        background:#2E8B57; 
        color:white; 
        display:flex; 
        align-items:center; 
        justify-content:center;
        font-size:22px; 
        font-weight:700; 
        z-index:9999; 
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }
    /* Empuja el contenido hacia abajo para que no quede oculto detrás del top bar */
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    </style>

    <!-- Contenedor HTML que muestra el título principal -->
    <div class="top-bar">ConectaServicios</div>
    """,
    unsafe_allow_html=True,
)

# Botón de Inicio (siempre disponible)
# Permite volver a la página principal desde cualquier parte.
if st.button("🏠 Inicio", key="home_btn"):
    st.session_state.page = "inicio"
    rerun_safe()
# -------------------------
# Sidebar navigation (simple)
# -------------------------

# Lista de páginas que queremos mostrar en el menú lateral
pages_display = ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Mis Trabajos", "Chats", "Notificaciones"]

# Mapeo entre el texto que ve el usuario y la clave interna que usa la app
mapping = {
    "Inicio": "inicio",
    "Iniciar sesión": "login",
    "Registrarse": "registro",
    "Perfil": "perfil",
    "Mis Trabajos": "mis_trabajos",
    "Chats": "chats",
    "Notificaciones": "notificaciones",
}

def page_to_label(page_key):
    """
    Convierte una clave interna ('perfil', 'chats', etc.)
    en la etiqueta visible del menú ('Perfil', 'Chats', etc.)
    Solo lo usamos para que el sidebar se mantenga sincronizado
    con la página actual.
    """
    for label, key in mapping.items():
        if key == page_key:
            return label
    return None  # Si es una subpágina que no aparece en el menú


# -- Construcción del sidebar --
with st.sidebar:
    st.markdown("### Navegación")

    # Mostramos el nombre del usuario o "Invitado"
    if current_user_name():
        st.markdown(f"**{current_user_name()}**")
    else:
        st.markdown("**Invitado**")

    # Identifica qué página está actualmente activa
    current_label = page_to_label(st.session_state.get("page", "inicio"))

    # Si la página actual pertenece al menú principal, mostramos el radio
    if current_label:
        try:
            sel_index = pages_display.index(current_label)
        except Exception:
            sel_index = 0
        
        # Menú de navegación lateral
        selection = st.radio("Ir a:", pages_display, index=sel_index, key="sidebar_nav_radio")
        selected_page = mapping.get(selection, "inicio")
        
        # Solo cambiamos de página si el usuario eligió otra
        if selected_page != st.session_state.get("page"):
            st.session_state.page = selected_page
            rerun_safe()

    else:
        # Cuando estás en páginas que NO aparecen en el sidebar (subpáginas)
        st.info(f"📍 {st.session_state.get('page', 'navegando').replace('_', ' ').title()}")
        st.write("Usa los botones de navegación en la página principal.")

    st.markdown("---")

    # Botón de cerrar sesión
    if current_user_id():
        if st.button("🔒 Cerrar sesión", key="logout_btn"):
            # Reset de los datos de sesión
            st.session_state.user = None
            st.session_state.user_id = 0
            st.session_state.selected_user_id = None
            st.session_state.page = "inicio"
            rerun_safe()


# -------------------------
# Styles (estilos personalizados)
# -------------------------

# CSS personalizado para mejorar la apariencia de la app
st.markdown(
    """
    <style>
    /* Botones estándar */
    div.stButton > button {
        height:56px; 
        width:200px; 
        background:#2E8B57; 
        color:white; 
        border-radius:10px; 
        font-size:15px; 
        margin:6px 8px; 
        border:none;
    }

    /* Hover de botones */
    div.stButton > button:hover {
        background-color:#276e47; 
        transform: translateY(-1px);
    }

    /* Títulos centrados */
    .conecta-title {
        text-align:center; 
        margin-bottom:8px;
    }

    /* Estilo de las tarjetas de servicios */
    .service-card {
        border:1px solid rgba(0,0,0,0.06); 
        padding:12px; 
        border-radius:8px; 
        margin-bottom:10px;
    }

    /* Burbujas de chat */
    .chat-bubble { 
        padding:10px 12px; 
        border-radius:12px; 
        margin:6px 0; 
        display:inline-block; 
        max-width:70%;
    }

    /* Mensajes enviados por el usuario */
    .chat-right { 
        background:#DCF8C6; 
        text-align:right; 
        float:right; 
        clear:both;
    }

    /* Mensajes recibidos */
    .chat-left { 
        background:#F1F0F0; 
        text-align:left; 
        float:left; 
        clear:both;
    }

    /* Hora del mensaje */
    .chat-time { 
        font-size:10px; 
        color:#666; 
        margin-top:4px; 
        display:block;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# -------------------------
# Reusable options map
# -------------------------
opciones_map = {
    "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
    "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
    "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
    "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"],
}


# -------------------------
# PAGES: flujo solicitado
# -------------------------
# ---------------------------
# PÁGINA DE INICIO (ARREGLADO)
# ---------------------------
if st.session_state.get("page") == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    st.subheader("Selecciona una categoría:")

    c1, c2 = st.columns(2)

    with c1:
        if st.button("Cuidado de mascotas", key="btn_mascotas", use_container_width=True):
            st.session_state.categoria = "Mascotas"
            st.session_state.page = "subcategoria"
            st.rerun()

        if st.button("Limpieza y hogar", key="btn_hogar", use_container_width=True):
            st.session_state.categoria = "Hogar"
            st.session_state.page = "subcategoria"
            st.rerun()

    with c2:
        if st.button("Clases particulares", key="btn_clases", use_container_width=True):
            st.session_state.categoria = "Clases"
            st.session_state.page = "subcategoria"
            st.rerun()

        if st.button("Cuidado de niños", key="btn_ninos", use_container_width=True):
            st.session_state.categoria = "Niños"
            st.session_state.page = "subcategoria"
            st.rerun()

# ---------- SUBCATEGORIA ----------
elif st.session_state.get("page") == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.get("categoria") or "-"}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver", key="volver_subcat"):
        st.session_state.page = "inicio"
        rerun_safe()

    lista = opciones_map.get(st.session_state.get("categoria"), [])
    if not lista:
        st.info("No hay opciones para esta categoría.")
    else:
        st.write("Busca o selecciona una opción:")
        # buscador simple
        filtro = st.text_input("Filtrar opciones...", key="subcat_busqueda")
        filtered = [x for x in lista if filtro.lower() in x.lower()] if filtro else lista

        # mostramos en grid (3 columnas por fila)
        cols_per_row = 3
        for i in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, opt in enumerate(filtered[i:i + cols_per_row]):
                with cols[idx]:
                    if st.button(opt, key=f"subcat_opt_{i+idx}"):
                        st.session_state.servicio = opt
                        st.session_state.page = "ubicacion"
                        rerun_safe()# -------------------------
# Reusable options map
# -------------------------
# Este diccionario define todas las categorías y sus subcategorías.
# Se usa tanto en la pantalla de inicio como en el perfil al publicar servicios.
opciones_map = {
    "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
    "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
    "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
    "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"],
}


# -------------------------
# PAGES: flujo solicitado
# -------------------------
# ---------------------------
# PÁGINA DE INICIO
# ---------------------------
if st.session_state.get("page") == "inicio":
    # Título principal
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    st.subheader("Selecciona una categoría:")

    # Dos columnas para mostrar botones grandes
    c1, c2 = st.columns(2)

    # Primera columna
    with c1:
        # Categoría Mascotas
        if st.button("Cuidado de mascotas", key="btn_mascotas", use_container_width=True):
            st.session_state.categoria = "Mascotas"
            st.session_state.page = "subcategoria"
            st.rerun()

        # Categoría Hogar
        if st.button("Limpieza y hogar", key="btn_hogar", use_container_width=True):
            st.session_state.categoria = "Hogar"
            st.session_state.page = "subcategoria"
            st.rerun()

    # Segunda columna
    with c2:
        # Categoría Clases
        if st.button("Clases particulares", key="btn_clases", use_container_width=True):
            st.session_state.categoria = "Clases"
            st.session_state.page = "subcategoria"
            st.rerun()

        # Categoría Niños
        if st.button("Cuidado de niños", key="btn_ninos", use_container_width=True):
            st.session_state.categoria = "Niños"
            st.session_state.page = "subcategoria"
            st.rerun()


# ---------------------------
# SUBCATEGORÍA
# ---------------------------
elif st.session_state.get("page") == "subcategoria":

    # Título dinámico según la categoría seleccionada
    st.markdown(
        f'<h1 class="conecta-title">Categoría: {st.session_state.get("categoria") or "-"}</h1>',
        unsafe_allow_html=True
    )

    # Botón para volver
    if st.button("⬅️ Volver", key="volver_subcat"):
        st.session_state.page = "inicio"
        rerun_safe()

    # Lista de opciones según la categoría
    lista = opciones_map.get(st.session_state.get("categoria"), [])

    if not lista:
        st.info("No hay opciones para esta categoría.")
    else:
        st.write("Busca o selecciona una opción:")

        # Buscador simple para filtrar subcategorías
        filtro = st.text_input("Filtrar opciones...", key="subcat_busqueda")

        # Si se escribe algo, filtramos la lista
        filtered = [x for x in lista if filtro.lower() in x.lower()] if filtro else lista

        # Se muestran en una cuadrícula de 3 columnas
        cols_per_row = 3
        for i in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, opt in enumerate(filtered[i:i + cols_per_row]):
                with cols[idx]:
                    # Cada opción es un botón
                    if st.button(opt, key=f"subcat_opt_{i+idx}"):
                        st.session_state.servicio = opt
                        st.session_state.page = "ubicacion"
                        rerun_safe()
# ---------- UBICACION ----------
elif st.session_state.get("page") == "ubicacion":

    # Título de la página
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)

    # Botón para volver a la subcategoría
    if st.button("⬅️ Volver", key="volver_ubic"):
        st.session_state.page = "subcategoria"
        rerun_safe()

    # Selección de comuna
    st.write("Selecciona la comuna donde quieres buscar el servicio:")

    # Por ahora la ciudad es fija
    ciudad = st.selectbox("Ciudad:", ["Santiago"], index=0, key="ubic_ciudad")

    # Lista completa de comunas
    comuna = st.selectbox("Comuna:", [""] + comunas_santiago, index=0, key="ubic_comuna")
    
    # Confirmar búsqueda
    if st.button("Buscar resultados en esta ubicación", key="ubic_buscar_btn"):
        if not comuna:
            st.warning("Selecciona una comuna para limitar la búsqueda.")
        else:
            # Guardamos la ubicación y pasamos a resultados
            st.session_state.ubicacion = f"{comuna}, {ciudad}"
            st.session_state.page = "resultados"
            rerun_safe()



# ---------- RESULTADOS ----------
elif st.session_state.get("page") == "resultados":

    # Servicio buscado (puede venir del buscador o del flujo guiado)
    servicio = st.session_state.get("servicio", "") or st.session_state.get("search_term", "")

    # Ubicación seleccionada
    ubic = (
        st.session_state.get("ubicacion", "") or
        (st.session_state.get("search_comuna") and f"{st.session_state.get('search_comuna')}, Santiago") or ""
    )

    # Título dinámico
    st.markdown(
        f'<h1 class="conecta-title">Resultados: {servicio} — {ubic or "Todas las comunas"}</h1>',
        unsafe_allow_html=True
    )
    
    # Botón volver
    if st.button("⬅️ Volver", key="volver_resultados"):
        # Si viene del flujo guiado, vuelve a ubicación
        if st.session_state.get("servicio") and st.session_state.get("ubicacion"):
            st.session_state.page = "ubicacion"
        else:
            # Si viene del buscador libre, vuelve al inicio
            st.session_state.page = "inicio"
        rerun_safe()

    # -------------------------
    # Filtros
    # -------------------------
    st.subheader("Filtros y Ordenamiento")
    col1, col2, col3, col4 = st.columns(4)
    
    # Precio mínimo
    with col1:
        pmin = st.text_input(
            "💰 Precio mín",
            value=st.session_state.get("results_filter_price_min", ""),
            key="f_pmin",
            placeholder="Ej: 5000"
        )
    
    # Precio máximo
    with col2:
        pmax = st.text_input(
            "💰 Precio máx",
            value=st.session_state.get("results_filter_price_max", ""),
            key="f_pmax",
            placeholder="Ej: 50000"
        )
    
    # Ordenamiento
    with col3:
        orden_opciones = [
            "Más recientes primero",
            "Precio: menor a mayor",
            "Precio: mayor a menor",
            "Alfabético (A-Z)",
            "Alfabético (Z-A)"
        ]
        orden_seleccionado = st.selectbox(
            "🔽 Ordenar por",
            orden_opciones,
            index=0,
            key="orden_select"
        )
    
    # Botón aplicar filtros
    with col4:
        st.write("")
        st.write("")
        if st.button("Aplicar", key="apply_result_filters", use_container_width=True):
            st.session_state.results_filter_price_min = pmin
            st.session_state.results_filter_price_max = pmax
            st.session_state.results_order = orden_seleccionado
            rerun_safe()

    st.markdown("---")

    # -------------------------
    # Obtener servicios desde BD
    # -------------------------
    term = servicio or ""
    comuna_name = ubic.split(",")[0] if ubic else None
    
    # Consulta principal
    servicios = db.get_services_filtered(term, comuna_name)

    # -------------------------
    # Filtros de precio locales
    # -------------------------
    filtered_services = []

    for s in servicios:
        ok = True

        # Convertir filtros a números
        try:
            pmin_v = float(st.session_state.get("results_filter_price_min")) if st.session_state.get("results_filter_price_min") else None
            pmax_v = float(st.session_state.get("results_filter_price_max")) if st.session_state.get("results_filter_price_max") else None
        except Exception:
            pmin_v = pmax_v = None

        price = s.get("price")

        # Aplicar reglas
        if price is not None and pmin_v is not None and price < pmin_v:
            ok = False
        if price is not None and pmax_v is not None and price > pmax_v:
            ok = False

        if ok:
            filtered_services.append(s)

    # -------------------------
    # Ordenamiento
    # -------------------------
    orden = st.session_state.get("results_order", "Más recientes primero")
    
    if orden == "Precio: menor a mayor":
        with_price = [s for s in filtered_services if s.get("price") is not None]
        without_price = [s for s in filtered_services if s.get("price") is None]
        with_price.sort(key=lambda x: x["price"])
        filtered_services = with_price + without_price
        
    elif orden == "Precio: mayor a menor":
        with_price = [s for s in filtered_services if s.get("price") is not None]
        without_price = [s for s in filtered_services if s.get("price") is None]
        with_price.sort(key=lambda x: x["price"], reverse=True)
        filtered_services = with_price + without_price
        
    elif orden == "Alfabético (A-Z)":
        filtered_services.sort(key=lambda x: x["service"].lower())
        
    elif orden == "Alfabético (Z-A)":
        filtered_services.sort(key=lambda x: x["service"].lower(), reverse=True)

    # -------------------------
    # Mostrar resultados
    # -------------------------
    if filtered_services:
        st.success(f"{len(filtered_services)} resultado(s) encontrados")
        
        for s in filtered_services:

            # Tarjeta visual del servicio
            st.markdown(
                f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>'
                f'Proveedor: <b>{s["user_nombre"]}</b> — {s.get("comunas") or "Sin comunas"}<br>'
                f'Precio: {("$"+str(int(s["price"]))) if s.get("price") else "A convenir"}<br>'
                f'<i>{s.get("user_bio") or ""}</i></div>',
                unsafe_allow_html=True,
            )
            
            # Botones de acción
            cols = st.columns([1, 1, 1])
            
            # Ver perfil
            with cols[0]:
                if st.button("👤 Ver perfil", key=f"verperfil_{s['id']}"):
                    st.session_state.perfil_usuario = {
                        "id": s.get("user_id"),
                        "nombre": s.get("user_nombre"),
                        "servicio": s.get("service"),
                        "valoracion": s.get("rating", "N/A"),
                        "bio": s.get("user_bio")
                    }
                    st.session_state.page = "perfil_publico"
                    rerun_safe()
            
            # Chatear
            with cols[1]:
                if st.button(f"💬 Chatear", key=f"chat_result_{s['id']}"):
                    st.session_state.selected_user_id = s["user_id"]
                    st.session_state.page = "chats"
                    rerun_safe()
            
            # Solicitar trabajo
            with cols[2]:
                if current_user_id() and current_user_id() != s["user_id"]:
                    if st.button(f"✅ Solicitar", key=f"solicitar_result_{s['id']}"):
                        st.session_state.solicitar_servicio_id = s["id"]
                        st.session_state.solicitar_trabajador_id = s["user_id"]
                        st.session_state.page = "solicitar_servicio"
                        rerun_safe()

    else:
        st.info("No hay servicios publicados que coincidan con tu búsqueda.")

# ---------- PERFIL PÚBLICO ----------
elif st.session_state.get("page") == "perfil_publico":
    # --- Carga los datos del usuario cuyo perfil se va a mostrar ---
    perfil = st.session_state.get("perfil_usuario", {})

    # --- Título del perfil público ---
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {perfil.get("nombre","Usuario")}</h1>', unsafe_allow_html=True)

    # --- Botón para volver a los resultados ---
    if st.button("⬅️ Volver", key="volver_perfil_publico"):
        st.session_state.page = "resultados"
        rerun_safe()

    # --- Información visible del usuario ---
    st.write(f"**Servicio:** {perfil.get('servicio','-')}")
    st.write(f"**Valoración:** {perfil.get('valoracion','-')}")
    st.write(f"**Bio:** {perfil.get('bio','')}")

    # --- Botón para iniciar chat desde el perfil público ---
    if st.button("Iniciar chat con esta persona", key="perfil_publico_chat"):
        if perfil.get("id"):
            st.session_state.selected_user_id = perfil.get("id")
            st.session_state.page = "chats"
            rerun_safe()


# ---------- CHATS ----------
elif st.session_state.get("page") == "chats":
    # --- Título de la sección de chats ---
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)

    # --- Si el usuario no ha iniciado sesión ---
    if not current_user_id():
        st.warning("Debes iniciar sesión para usar el chat.")

    else:
        # --- Cargar chats recientes desde la base de datos ---
        recent_chats = db.get_recent_chats(current_user_id())

        # --- ID del usuario con el que se está conversando ---
        receptor_id = st.session_state.get("selected_user_id")

        # --- Layout de dos columnas: lista de chats | área del chat ---
        col_list, col_chat = st.columns([1, 2])

        # ================================
        # 🟦 COLUMNA IZQUIERDA — LISTA DE CHATS
        # ================================
        with col_list:
            st.subheader("Conversaciones")

            # --- Mostrar listado de chats recientes ---
            if recent_chats:
                for chat in recent_chats:
                    # --- Preview del contenido del mensaje ---
                    preview = (
                        chat['last_message'][:30] + "..."
                        if len(chat['last_message']) > 30
                        else chat['last_message']
                    )

                    # --- Hora del último mensaje ---
                    time_preview = chat['last_timestamp'][11:16] if chat['last_timestamp'] else ""

                    # --- Destacar si es el chat actualmente seleccionado ---
                    is_selected = (receptor_id == chat['other_user_id'])
                    button_style = "🟢" if is_selected else "💬"

                    # --- Botón de un chat ---
                    if st.button(
                        f"{button_style} {chat['other_user_name']}\n{preview} · {time_preview}",
                        key=f"chat_item_{chat['other_user_id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_user_id = chat['other_user_id']
                        st.rerun()

                st.markdown("---")

            # --- Botón para iniciar un chat nuevo ---
            if st.button("➕ Nuevo chat", key="new_chat_btn", use_container_width=True):
                conn = db.get_conn()
                cur = conn.cursor()
                # --- Obtiene todos los usuarios excepto el actual ---
                cur.execute("SELECT id, nombre FROM users WHERE id != ?", (current_user_id(),))
                rows = cur.fetchall()
                conn.close()

                others = [dict(r) for r in rows]

                # --- Filtrar usuarios que YA tienen chat ---
                chat_user_ids = [c['other_user_id'] for c in recent_chats]
                new_users = [u for u in others if u['id'] not in chat_user_ids]

                if new_users:
                    st.session_state.show_new_chat_selector = True
                    st.rerun()
                else:
                    st.info("Ya tienes chats con todos los usuarios.")

            # --- Selector para comenzar un chat desde cero ---
            if st.session_state.get("show_new_chat_selector"):
                conn = db.get_conn()
                cur = conn.cursor()
                cur.execute("SELECT id, nombre FROM users WHERE id != ?", (current_user_id(),))
                rows = cur.fetchall()
                conn.close()

                others = [dict(r) for r in rows]
                chat_user_ids = [c['other_user_id'] for c in recent_chats] if recent_chats else []
                new_users = [u for u in others if u['id'] not in chat_user_ids]

                if new_users:
                    names = [u["nombre"] for u in new_users]

                    # --- Selector visual ---
                    sel = st.selectbox("Selecciona usuario:", names, key="new_chat_select")

                    # --- Crear chat con ese usuario ---
                    if st.button("Iniciar chat", key="start_new_chat"):
                        selected_user = next(u for u in new_users if u["nombre"] == sel)
                        st.session_state.selected_user_id = selected_user["id"]
                        st.session_state.show_new_chat_selector = False
                        st.rerun()

                    # --- Cancelar operación ---
                    if st.button("Cancelar", key="cancel_new_chat"):
                        st.session_state.show_new_chat_selector = False
                        st.rerun()

        # ================================
        # 🟧 COLUMNA DERECHA — MENSAJES DEL CHAT
        # ================================
        with col_chat:
            if receptor_id:
                receptor = db.get_user_by_id(receptor_id)

                if receptor:
                    st.subheader(f"Chat con {receptor['nombre']}")

                    # --- Obtener todos los mensajes de la conversación ---
                    mensajes = db.get_messages_between(current_user_id(), receptor_id)

                    # --- Mostrar mensajes con estilo tipo chat ---
                    if mensajes:
                        for m in mensajes:
                            autor = "Tú" if m["emisor_id"] == current_user_id() else receptor["nombre"]
                            clase = "chat-right" if autor == "Tú" else "chat-left"

                            st.markdown(
                                f'<div class="chat-bubble {clase}"><b>{autor}:</b> {m["contenido"]}'
                                f'<span class="chat-time">{m["timestamp"][11:16]}</span></div>',
                                unsafe_allow_html=True,
                            )

                        # --- Asegura espacio limpio al final del chat ---
                        st.markdown('<div style="clear:both;"></div>', unsafe_allow_html=True)

                    else:
                        st.info("No hay mensajes aún. Escribe el primero.")

                    # --- Formulario para enviar mensajes ---
                    with st.form("send_msg_form", clear_on_submit=True):
                        nuevo = st.text_input("Escribe un mensaje", key="new_msg_input", placeholder="Escribe aquí...")
                        col1, col2 = st.columns([5, 1])

                        with col2:
                            send_btn = st.form_submit_button("Enviar", use_container_width=True)

                        # --- Guardar y enviar el mensaje ---
                        if send_btn:
                            if nuevo and nuevo.strip():
                                db.add_message(current_user_id(), receptor_id, nuevo.strip())
                                db.add_notification(
                                    receptor_id,
                                    "mensaje",
                                    f"Nuevo mensaje de {current_user_name() or 'Usuario'}"
                                )
                                st.rerun()
                            else:
                                st.warning("Escribe un mensaje antes de enviar.")

            else:
                st.info("👈 Selecciona una conversación o inicia un nuevo chat")


# ========== NOTIFICACIONES ==========
elif st.session_state.get("page") == "notificaciones":
    st.markdown('<h1>🔔 Notificaciones</h1>', unsafe_allow_html=True)

    # Verificar si el usuario está logueado
    if not current_user_id():
        st.warning("Debes iniciar sesión para ver notificaciones.")
    
    else:
        # Obtener notificaciones desde la base de datos
        notifs = db.get_notifications(current_user_id())

        if notifs:
            for n in notifs:
                # Mostrar cada notificación con fecha y estado
                estado = "Leído" if n.get("leido") else "Nuevo"
                st.write(f"- {n['mensaje']} ({n['fecha'][:16]}) — {estado}")

                # Botón para marcar una notificación como leída
                if not n.get("leido"):
                    if st.button(f"Marcar leído {n['id']}"):
                        db.mark_notification_read(n['id'])
                        rerun_safe()
        else:
            st.info("No tienes notificaciones.")


# ========== PERFIL ==========
elif st.session_state.get("page") == "perfil":
    st.markdown('<h1>👤 Mi Perfil</h1>', unsafe_allow_html=True)

    # Validar sesión
    if not current_user_id():
        st.warning("Debes iniciar sesión para ver tu perfil.")
    else:
        user = db.get_user_by_id(current_user_id())

        # Mostrar información básica del usuario
        st.write(f"Nombre: {user['nombre']}")
        st.write(f"Email: {user['email']}")
        st.write(f"Comuna: {user['comuna'] or '-'}")
        st.write(f"Bio: {user['bio'] or '-'}")

        st.markdown("---")
        st.subheader("⭐ Valoraciones")

        # Promedio general de evaluaciones
        prom = db.get_promedio_calificacion(user["id"])
        if prom:
            st.metric("Calificación promedio", f"{prom} / 5")
        else:
            st.info("Aún no tiene evaluaciones.")

        # Estadísticas del trabajador (trabajos completados, recomendaciones, etc.)
        stats = db.get_estadisticas_trabajador(user["id"])
        if stats:
            st.metric("Trabajos completados", stats['trabajos_completados'])
            st.metric("Evaluaciones", stats['total_evaluaciones'])
            st.metric("Recomendaciones", stats['recomendaciones'])

        # Mostrar reseñas de clientes
        st.markdown("### 📝 Reseñas de clientes")
        evaluaciones = db.get_evaluaciones_trabajador(user["id"])

        if evaluaciones:
            for ev in evaluaciones:
                with st.expander(f"{ev['calificacion']}⭐ - {ev['cliente_nombre']}"):
                    st.write(f"Puntualidad: {ev['puntualidad']}")
                    st.write(f"Calidad: {ev['calidad']}")
                    st.write(f"Comunicación: {ev['comunicacion']}")
                    st.write(f"Recomendaría: {'Sí' if ev['recomendaria'] else 'No'}")
                    st.write(f"Comentario: {ev['comentario'] or 'Sin comentario'}")
        else:
            st.write("Aún no tiene reseñas.")

        st.markdown("---")
        st.subheader("Tus publicaciones")

        # Listar servicios publicados por el usuario
        user_services = db.get_user_services(current_user_id())
        for s in user_services:
            st.write(f"- {s['service']} ({s['category']}) — {s['comuna']} — ${s.get('price') or 'No informado'}")

        st.markdown("---")
        st.subheader("Publicar un servicio")

        # Formulario para publicar servicios
        cat = st.selectbox("Categoría", [""] + list(opciones_map.keys()))
        
        if st.session_state.get("publish_service"):
            with st.form("publish_service_form"):
                comuna_sel = st.selectbox("Comuna", [""] + comunas_santiago)
                precio = st.text_input("Precio")

                if st.form_submit_button("Publicar servicio"):
                    db.add_service(current_user_id(), cat, st.session_state.publish_service, comuna_sel, precio)
                    st.success("Servicio publicado correctamente")
                    rerun_safe()

        # Botón para editar perfil
        if st.button("Editar perfil"):
            with st.form("edit_profile_form"):
                nuevo_nombre = st.text_input("Nombre", user["nombre"])
                nueva_bio = st.text_area("Bio", user["bio"])
                nueva_comuna = st.selectbox("Comuna", [""] + comunas_santiago)

                if st.form_submit_button("Guardar cambios"):
                    db.update_user_profile(current_user_id(), nuevo_nombre, nueva_bio, nueva_comuna)
                    st.success("Perfil actualizado")
                    rerun_safe()


# ========== MIS TRABAJOS ==========
elif st.session_state.get("page") == "mis_trabajos":
    st.markdown('<h1>📋 Mis Trabajos</h1>', unsafe_allow_html=True)

    if not current_user_id():
        st.warning("Debes iniciar sesión para ver tus trabajos.")
    else:
        tab1, tab2 = st.tabs(["Solicitados por mí", "Recibidos"])

        # --- Trabajos solicitados por mí (Cliente) ---
        with tab1:
            trabajos_cliente = db.get_trabajos_cliente(current_user_id())

            for trabajo in trabajos_cliente:
                with st.expander(f"{trabajo['servicio_nombre']} - {trabajo['estado']}"):
                    st.write(f"Fecha: {trabajo['fecha_solicitada']}")
                    st.write(f"Descripción: {trabajo['descripcion']}")

                    # Si el trabajador terminó, permitir evaluar
                    if trabajo['estado'] == "completado":
                        if st.button(f"Evaluar trabajo {trabajo['id']}"):
                            st.session_state.ver_trabajo_id = trabajo['id']
                            st.session_state.page = "evaluar_trabajo"
                            rerun_safe()

        # --- Trabajos recibidos (Trabajador) ---
        with tab2:
            trabajos_trabajador = db.get_trabajos_trabajador(current_user_id())

            for trabajo in trabajos_trabajador:
                with st.expander(f"{trabajo['servicio_nombre']} - Cliente: {trabajo['cliente_nombre']}"):
                    st.write(f"Estado: {trabajo['estado']}")

                    # Botones para aceptar o rechazar
                    if trabajo['estado'] == "pendiente":
                        if st.button("Aceptar"):
                            db.update_trabajo_estado(trabajo['id'], "aceptado")
                            db.add_notification(trabajo['cliente_id'], "trabajo_aceptado", "Acepté tu trabajo")
                            rerun_safe()

                        if st.button("Rechazar"):
                            db.update_trabajo_estado(trabajo['id'], "rechazado")
                            db.add_notification(trabajo['cliente_id'], "trabajo_rechazado", "Rechacé tu trabajo")
                            rerun_safe()

                    # Marcar como completado
                    elif trabajo['estado'] == "aceptado":
                        if st.button("Marcar como completado"):
                            db.update_trabajo_estado(trabajo['id'], "completado")
                            db.add_notification(trabajo['cliente_id'], "trabajo_completado",
                                "Tu trabajo fue completado, ya puedes evaluarlo.")
                            rerun_safe()                
# ---------- SOLICITAR SERVICIO ----------
elif st.session_state.get("page") == "solicitar_servicio":

    # Título de la página
    st.markdown('<h1 class="conecta-title">✅ Solicitar Servicio</h1>', unsafe_allow_html=True)

    # Si el usuario no está logueado, no puede solicitar servicios
    if not current_user_id():
        st.warning("Debes iniciar sesión para solicitar un servicio.")
        if st.button("Ir a iniciar sesión"):
            st.session_state.page = "login"
            rerun_safe()

    else:
        # IDs guardados al presionar “Solicitar” en los resultados
        servicio_id = st.session_state.get("solicitar_servicio_id")
        trabajador_id = st.session_state.get("solicitar_trabajador_id")

        # Si faltan datos, error
        if not servicio_id or not trabajador_id:
            st.error("Error: No se encontró el servicio.")
            if st.button("⬅️ Volver"):
                st.session_state.page = "resultados"
                rerun_safe()

        else:
            # Cargar datos del servicio desde la base de datos
            conn = db.get_conn()
            cur = conn.cursor()
            cur.execute("""
                SELECT s.*, u.nombre as trabajador_nombre
                FROM services s
                JOIN users u ON s.user_id = u.id
                WHERE s.id = ?
            """, (servicio_id,))
            servicio = cur.fetchone()
            conn.close()

            # Si el servicio existe, mostrar datos
            if servicio:
                servicio = dict(servicio)
                st.info(f"📋 **Servicio:** {servicio['service']} ({servicio['category']})")
                st.info(f"👷 **Trabajador:** {servicio['trabajador_nombre']}")

                # Precio si está definido
                if servicio.get('price'):
                    st.info(f"💰 **Precio:** ${int(servicio['price'])}")

                # Formulario para completar la solicitud
                st.markdown("---")
                st.subheader("Completa los detalles de tu solicitud:")

                with st.form("solicitud_form"):

                    # Fecha y hora
                    col1, col2 = st.columns(2)
                    with col1:
                        fecha = st.date_input("📅 Fecha deseada", min_value=datetime.now().date())
                    with col2:
                        hora = st.time_input("🕐 Hora aproximada")

                    # Dirección y descripción
                    direccion = st.text_input("📍 Dirección completa")
                    descripcion = st.text_area("📝 Describe el trabajo que necesitas", height=100)

                    # Si el servicio NO tiene precio fijo, el cliente propone uno
                    if not servicio.get('price'):
                        precio_propuesto = st.number_input("💵 Propón un precio", min_value=0, step=1000)
                    else:
                        precio_propuesto = servicio['price']

                    # Botones de enviar/cancelar
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submit = st.form_submit_button("✅ Enviar solicitud")
                    with col_btn2:
                        cancel = st.form_submit_button("❌ Cancelar")

                    # Enviar la solicitud
                    if submit:
                        if not direccion or not descripcion:
                            st.error("Por favor completa todos los campos obligatorios.")
                        else:
                            # Registrar el trabajo en la BD
                            trabajo_id = db.create_trabajo(
                                servicio_id,
                                current_user_id(),
                                trabajador_id,
                                fecha.isoformat(),
                                hora.strftime("%H:%M"),
                                direccion,
                                descripcion,
                                precio_propuesto if not servicio.get('price') else None
                            )

                            # Si se creó bien
                            if trabajo_id:
                                # Notificar a trabajador
                                db.add_notification(
                                    trabajador_id,
                                    "solicitud_trabajo",
                                    f"Nueva solicitud de {current_user_name()} para {servicio['service']}"
                                )

                                st.success("¡Solicitud enviada!")
                                st.balloons()

                                # Limpiar sesión y volver
                                st.session_state.solicitar_servicio_id = None
                                st.session_state.solicitar_trabajador_id = None
                                st.session_state.page = "mis_trabajos"
                                rerun_safe()

                    # Cancelar
                    if cancel:
                        st.session_state.solicitar_servicio_id = None
                        st.session_state.solicitar_trabajador_id = None
                        st.session_state.page = "resultados"
                        rerun_safe()
# ---------- EVALUAR TRABAJO ----------
elif st.session_state.get("page") == "evaluar_trabajo"):

    # Obtener el ID del trabajo que se va a evaluar
    trabajo_id = st.session_state.get("ver_trabajo_id")

    if not trabajo_id:
        st.error("No se encontró el trabajo para evaluar.")

    else:
        trabajo = db.get_trabajo_by_id(trabajo_id)

        # Solo el cliente puede evaluar el trabajo
        if not trabajo or trabajo['cliente_id'] != current_user_id():
            st.warning("Solo el cliente puede evaluar el trabajo.")

        else:
            # Información del trabajo
            st.markdown('<h1 class="conecta-title">⭐ Evaluar Trabajo</h1>', unsafe_allow_html=True)
            st.write(f"**Servicio:** {trabajo['servicio_nombre']}")
            st.write(f"**Trabajador:** {trabajo['trabajador_nombre']}")
            st.markdown("---")

            # Campos de evaluación (sliders)
            calificacion = st.slider("Calificación general", 1, 5, 5)
            puntualidad = st.slider("Puntualidad", 1, 5, 5)
            calidad = st.slider("Calidad del trabajo", 1, 5, 5)
            comunicacion = st.slider("Comunicación", 1, 5, 5)

            recomendaria = st.selectbox("¿Lo recomendarías?", [1, 0],
                format_func=lambda x: "Sí" if x == 1 else "No")

            comentario = st.text_area("Comentario (opcional)", height=120)

            # Botón para enviar evaluación
            if st.button("Enviar evaluación"):

                # Guardar en BD
                db.create_evaluacion(
                    trabajo_id,
                    trabajo["cliente_id"],
                    trabajo["trabajador_id"],
                    int(calificacion),
                    comentario or "",
                    int(puntualidad),
                    int(calidad),
                    int(comunicacion),
                    int(recomendaria)
                )

                # Notificar al trabajador
                db.add_notification(
                    trabajo["trabajador_id"],
                    "evaluacion_recibida",
                    f"Has recibido una nueva evaluación de {current_user_name()}"
                )

                # Confirmación
                st.success("¡Gracias! Tu evaluación fue enviada.")
                st.session_state.ver_trabajo_id = None
                st.session_state.page = "mis_trabajos"
                rerun_safe()
# ---------- LOGIN / REGISTRO ----------
elif st.session_state.get("page") in ["login", "registro"]:
    if st.session_state.get("page") == "login":
        st.markdown('<h1 class="conecta-title">🔐 Iniciar sesión</h1>', unsafe_allow_html=True)
        
        # FORMULARIO DE LOGIN
        with st.form("login_form"):
            email = st.text_input("Correo electrónico", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pwd")
            
            # BOTÓN PARA ENTRAR
            if st.form_submit_button("Entrar"):
                
                # Verificar usuario en BD
                user = auth.login_user(email.strip(), password)
                
                if user:
                    # Guardar los datos del usuario en la sesión
                    st.session_state.user = {"id": user["id"], "nombre": user["nombre"], "email": user["email"]}
                    st.session_state.user_id = user["id"]
                    st.success("Inicio de sesión correcto")
                    
                    # Redirigir al inicio
                    st.session_state.page = "inicio"
                    rerun_safe()
                else:
                    st.error("Credenciales incorrectas")
    
    # ----- REGISTRO -----
    else:
        st.markdown('<h1 class="conecta-title">📝 Registrarse</h1>', unsafe_allow_html=True)

        with st.form("register_form"):
            nombre = st.text_input("Nombre completo", key="reg_nombre")
            email_r = st.text_input("Correo electrónico", key="reg_email")
            pwd_r = st.text_input("Contraseña", type="password", key="reg_pwd")
            bio_r = st.text_area("Descripción / Bio (opcional)", key="reg_bio")
            comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago, key="reg_comuna")
            
            # BOTÓN REGISTRARSE
            if st.form_submit_button("Registrarse"):
                
                # Crear usuario en BD
                new_id = auth.register_user(nombre.strip(), email_r.strip(), pwd_r, bio_r, comuna_r)
                
                if new_id:
                    st.success("Cuenta creada. Puedes iniciar sesión.")
                    
                    # Redirigir al login
                    st.session_state.page = "login"
                    rerun_safe()
                else:
                    st.error("No se pudo crear la cuenta (correo ya existe o faltan datos).")


# ---------- fallback ----------
else:
    st.session_state.page = "inicio"
    rerun_safe()
