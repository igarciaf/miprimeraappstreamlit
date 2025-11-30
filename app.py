# app.py — Archivo principal de la aplicación Streamlit
# Versión limpia y lista para presentar (fotos eliminadas)
# Incluye comentarios "EN PRESENTACIÓN" para ayudarte a explicar cada bloque

import streamlit as st
import db
import auth
from datetime import datetime

# -------------------------
# Inicialización
# -------------------------
# (EN PRESENTACIÓN) Aquí inicializamos la base de datos: crea tablas si no existen.
db.init_db()

# Configuración de la página Streamlit
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")


# -------------------------
# Helpers / rerun / sesión
# -------------------------
def rerun_safe():
    """Reejecución segura de la app (utilizar después de cambiar session_state)."""
    st.rerun()


def current_user_id():
    """
    Devuelve id del usuario actualmente en sesión (si existe).
    (EN PRESENTACIÓN) Esto permite saber si el usuario está logueado.
    """
    uid = st.session_state.get("user_id")
    if uid:
        return uid
    u = st.session_state.get("user")
    if isinstance(u, dict) and u.get("id"):
        return u.get("id")
    return None


def current_user_name():
    """
    Devuelve nombre del usuario en sesión o su email como fallback.
    (EN PRESENTACIÓN) Lo uso para mostrar quién está usando la app.
    """
    u = st.session_state.get("user")
    if isinstance(u, dict) and u.get("nombre"):
        return u.get("nombre")
    uid = current_user_id()
    if uid:
        row = db.get_user_by_id(uid)
        if row:
            return row.get("nombre") or row.get("email")
    return None


# -------------------------
# Valores por defecto para session_state
# -------------------------
defaults = {
    "page": "inicio",
    "user": None,
    "user_id": 0,
    "selected_user_id": None,
    "categoria": None,
    "servicio": None,
    "ubicacion": None,
    "publish_cat": None,
    "publish_service": None,
    "search_term": "",
    "search_comuna": "",
    "results_filter_price_min": "",
    "results_filter_price_max": "",
    "results_filter_rating_min": "",
    "solicitar_servicio_id": None,
    "solicitar_trabajador_id": None,
    "ver_trabajo_id": None,
    "show_new_chat_selector": False,
}

for k, v in defaults.items():
    st.session_state.setdefault(k, v)


# -------------------------
# Comunas (lista completa de Santiago)
# -------------------------
# (EN PRESENTACIÓN) Lista estática usada en formularios y filtros.
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
# Sidebar navigation (simple)
# -------------------------
pages_display = ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Mis Trabajos", "Chats", "Notificaciones"]
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
    """Devuelve la etiqueta del menú para la clave de página dada."""
    for label, key in mapping.items():
        if key == page_key:
            return label
    return None


with st.sidebar:
    st.markdown("### Navegación")
    if current_user_name():
        st.markdown(f"**{current_user_name()}**")
    else:
        st.markdown("**Invitado**")

    current_label = page_to_label(st.session_state.get("page", "inicio"))
    if current_label:
        try:
            sel_index = pages_display.index(current_label)
        except Exception:
            sel_index = 0
        selection = st.radio("Ir a:", pages_display, index=sel_index, key="sidebar_nav_radio")
        selected_page = mapping.get(selection, "inicio")
        if selected_page != st.session_state.get("page"):
            st.session_state.page = selected_page
            rerun_safe()
    else:
        st.info(f"📍 {st.session_state.get('page', 'navegando').replace('_', ' ').title()}")
        st.write("Usa los botones de navegación en la página principal.")

    st.markdown("---")
    if current_user_id():
        if st.button("🔒 Cerrar sesión", key="logout_btn"):
            st.session_state.user = None
            st.session_state.user_id = 0
            st.session_state.selected_user_id = None
            st.session_state.page = "inicio"
            rerun_safe()


# -------------------------
# Styles
# -------------------------
st.markdown(
    """
    <style>
    div.stButton > button { height:56px; width:200px; background:#2E8B57; color:white; border-radius:10px; font-size:15px; margin:6px 8px; border:none; }
    div.stButton > button:hover { background-color:#276e47; transform: translateY(-1px); }
    .conecta-title { text-align:center; margin-bottom:8px; }
    .service-card { border:1px solid rgba(0,0,0,0.06); padding:12px; border-radius:8px; margin-bottom:10px; }
    .chat-bubble { padding:10px 12px; border-radius:12px; margin:6px 0; display:inline-block; max-width:70%; }
    .chat-right { background:#DCF8C6; text-align:right; float:right; clear:both; }
    .chat-left { background:#F1F0F0; text-align:left; float:left; clear:both; }
    .chat-time { font-size:10px; color:#666; margin-top:4px; display:block; }
    </style>
""",
    unsafe_allow_html=True,
)


# -------------------------
# Reusable options map
# -------------------------
# (EN PRESENTACIÓN) Categorías y subcategorías reutilizables en la app.
opciones_map = {
    "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
    "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
    "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
    "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"],
}
# -------------------------
# TOP BAR global (siempre visible)
# -------------------------
st.markdown(
    """
    <style>
    .top-bar{
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 64px;
        background: #2E8B57;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 700;
        z-index: 9999;
        box-shadow:0 2px 8px rgba(0,0,0,0.08);
    }
    .main > div { margin-top: 90px; }
    </style>
    <div class="top-bar">ConectaServicios</div>
    """,
    unsafe_allow_html=True,
)

# botón siempre visible
if st.button("🏠 Inicio", key="home_btn"):
    st.session_state.page = "inicio"
    rerun_safe()


# -------------------------
# PAGES: flujo principal
# -------------------------

# ---------- INICIO ----------
if st.session_state.get("page") == "inicio":
    # (EN PRESENTACIÓN) Pantalla principal — el punto de entrada de la app.
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    st.subheader("Selecciona una categoría:")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cuidado de mascotas", key="btn_mascotas", use_container_width=True):
            st.session_state.categoria = "Mascotas"
            st.session_state.page = "subcategoria"
            rerun_safe()
        if st.button("Limpieza y hogar", key="btn_hogar", use_container_width=True):
            st.session_state.categoria = "Hogar"
            st.session_state.page = "subcategoria"
            rerun_safe()
    with c2:
        if st.button("Clases particulares", key="btn_clases", use_container_width=True):
            st.session_state.categoria = "Clases"
            st.session_state.page = "subcategoria"
            rerun_safe()
        if st.button("Cuidado de niños", key="btn_ninos", use_container_width=True):
            st.session_state.categoria = "Niños"
            st.session_state.page = "subcategoria"
            rerun_safe()


# ---------- SUBCATEGORIA ----------
elif st.session_state.get("page") == "subcategoria":
    # (EN PRESENTACIÓN) Muestra subcategorías según la categoría elegida.
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.get("categoria") or "-"}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver", key="volver_subcat"):
        st.session_state.page = "inicio"
        rerun_safe()

    lista = opciones_map.get(st.session_state.get("categoria"), [])
    if not lista:
        st.info("No hay opciones para esta categoría.")
    else:
        st.write("Busca o selecciona una opción:")
        filtro = st.text_input("Filtrar opciones...", key="subcat_busqueda")
        filtered = [x for x in lista if filtro.lower() in x.lower()] if filtro else lista

        cols_per_row = 3
        for i in range(0, len(filtered), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, opt in enumerate(filtered[i:i + cols_per_row]):
                with cols[idx]:
                    if st.button(opt, key=f"subcat_opt_{i+idx}"):
                        st.session_state.servicio = opt
                        st.session_state.page = "ubicacion"
                        rerun_safe()


# ---------- UBICACION ----------
elif st.session_state.get("page") == "ubicacion":
    # (EN PRESENTACIÓN) Permite elegir comuna para filtrar resultados.
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver", key="volver_ubic"):
        st.session_state.page = "subcategoria"
        rerun_safe()

    st.write("Selecciona la comuna donde quieres buscar el servicio:")
    ciudad = st.selectbox("Ciudad:", ["Santiago"], index=0, key="ubic_ciudad")
    comuna = st.selectbox("Comuna:", [""] + comunas_santiago, index=0, key="ubic_comuna")
    if st.button("Buscar resultados en esta ubicación", key="ubic_buscar_btn"):
        if not comuna:
            st.warning("Selecciona una comuna para limitar la búsqueda.")
        else:
            st.session_state.ubicacion = f"{comuna}, {ciudad}"
            st.session_state.page = "resultados"
            rerun_safe()


# ---------- RESULTADOS ----------
elif st.session_state.get("page") == "resultados":
    # (EN PRESENTACIÓN) Aquí mostramos los resultados que vienen de la BD y aplicamos filtros locales.
    servicio = st.session_state.get("servicio", "") or st.session_state.get("search_term", "")
    ubic = st.session_state.get("ubicacion", "") or (st.session_state.get("search_comuna") and f"{st.session_state.get('search_comuna')}, Santiago") or ""
    st.markdown(f'<h1 class="conecta-title">Resultados: {servicio} — {ubic or "Todas las comunas"}</h1>', unsafe_allow_html=True)

    if st.button("⬅️ Volver", key="volver_resultados"):
        if st.session_state.get("servicio") and st.session_state.get("ubicacion"):
            st.session_state.page = "ubicacion"
        else:
            st.session_state.page = "inicio"
        rerun_safe()

    # Filtros y ordenamiento
    st.subheader("Filtros y Ordenamiento")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        pmin = st.text_input("💰 Precio mín", value=st.session_state.get("results_filter_price_min", ""), key="f_pmin", placeholder="Ej: 5000")
    with col2:
        pmax = st.text_input("💰 Precio máx", value=st.session_state.get("results_filter_price_max", ""), key="f_pmax", placeholder="Ej: 50000")
    with col3:
        orden_opciones = ["Más recientes primero", "Precio: menor a mayor", "Precio: mayor a menor", "Alfabético (A-Z)", "Alfabético (Z-A)"]
        orden_seleccionado = st.selectbox("🔽 Ordenar por", orden_opciones, index=0, key="orden_select")
    with col4:
        st.write(""); st.write("")
        if st.button("Aplicar", key="apply_result_filters", use_container_width=True):
            st.session_state.results_filter_price_min = pmin
            st.session_state.results_filter_price_max = pmax
            st.session_state.results_order = orden_seleccionado
            rerun_safe()

    st.markdown("---")

    # Obtener servicios desde la BD
    term = servicio or ""
    comuna_name = ubic.split(",")[0] if ubic else None
    servicios = db.get_services_filtered(term, comuna_name)

    # Aplicar filtros locales (precio)
    filtered_services = []
    for s in servicios:
        ok = True
        try:
            pmin_v = float(st.session_state.get("results_filter_price_min")) if st.session_state.get("results_filter_price_min") else None
            pmax_v = float(st.session_state.get("results_filter_price_max")) if st.session_state.get("results_filter_price_max") else None
        except Exception:
            pmin_v = pmax_v = None

        price = s.get("price")
        if price is not None and pmin_v is not None and price < pmin_v:
            ok = False
        if price is not None and pmax_v is not None and price > pmax_v:
            ok = False
        if ok:
            filtered_services.append(s)

    # Ordenamiento
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

    # Mostrar resultados
    if filtered_services:
        st.success(f"{len(filtered_services)} resultado(s) encontrados")
        for s in filtered_services:
            st.markdown(
                f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>'
                f'Proveedor: <b>{s["user_nombre"]}</b> — {s.get("comunas") or "Sin comunas"}<br>'
                f'Precio: {("$"+str(int(s["price"]))) if s.get("price") else "A convenir"}<br>'
                f'<i>{s.get("user_bio") or ""}</i></div>',
                unsafe_allow_html=True,
            )
            cols = st.columns([1, 1, 1])
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
            with cols[1]:
                if st.button(f"💬 Chatear", key=f"chat_result_{s['id']}"):
                    st.session_state.selected_user_id = s["user_id"]
                    st.session_state.page = "chats"
                    rerun_safe()
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
    # (EN PRESENTACIÓN) Muestra la información pública del proveedor seleccionado.
    perfil = st.session_state.get("perfil_usuario", {})
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {perfil.get("nombre","Usuario")}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver", key="volver_perfil_publico"):
        st.session_state.page = "resultados"
        rerun_safe()
    st.write(f"**Servicio:** {perfil.get('servicio','-')}")
    st.write(f"**Valoración:** {perfil.get('valoracion','-')}")
    st.write(f"**Bio:** {perfil.get('bio','')}")
    if st.button("Iniciar chat con esta persona", key="perfil_publico_chat"):
        if perfil.get("id"):
            st.session_state.selected_user_id = perfil.get("id")
            st.session_state.page = "chats"
            rerun_safe()


# ---------- CHATS ----------
elif st.session_state.get("page") == "chats":
    # (EN PRESENTACIÓN) Módulo de mensajería entre usuarios.
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para usar el chat.")
    else:
        recent_chats = db.get_recent_chats(current_user_id())
        receptor_id = st.session_state.get("selected_user_id")
        col_list, col_chat = st.columns([1, 2])

        with col_list:
            st.subheader("Conversaciones")
            if recent_chats:
                for chat in recent_chats:
                    preview = chat['last_message'][:30] + "..." if len(chat['last_message']) > 30 else chat['last_message']
                    time_preview = chat['last_timestamp'][11:16] if chat['last_timestamp'] else ""
                    is_selected = (receptor_id == chat['other_user_id'])
                    button_style = "🟢" if is_selected else "💬"
                    if st.button(f"{button_style} {chat['other_user_name']}\n{preview} · {time_preview}", key=f"chat_item_{chat['other_user_id']}", use_container_width=True):
                        st.session_state.selected_user_id = chat['other_user_id']
                        rerun_safe()
                st.markdown("---")

            if st.button("➕ Nuevo chat", key="new_chat_btn", use_container_width=True):
                conn = db.get_conn()
                cur = conn.cursor()
                cur.execute("SELECT id, nombre FROM users WHERE id != ?", (current_user_id(),))
                rows = cur.fetchall()
                conn.close()
                others = [dict(r) for r in rows]
                chat_user_ids = [c['other_user_id'] for c in recent_chats] if recent_chats else []
                new_users = [u for u in others if u['id'] not in chat_user_ids]
                if new_users:
                    st.session_state.show_new_chat_selector = True
                    rerun_safe()
                else:
                    st.info("Ya tienes chats con todos los usuarios.")

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
                    sel = st.selectbox("Selecciona usuario:", names, key="new_chat_select")
                    if st.button("Iniciar chat", key="start_new_chat"):
                        selected_user = next(u for u in new_users if u["nombre"] == sel)
                        st.session_state.selected_user_id = selected_user["id"]
                        st.session_state.show_new_chat_selector = False
                        rerun_safe()
                    if st.button("Cancelar", key="cancel_new_chat"):
                        st.session_state.show_new_chat_selector = False
                        rerun_safe()

        with col_chat:
            if receptor_id:
                receptor = db.get_user_by_id(receptor_id)
                if receptor:
                    st.subheader(f"Chat con {receptor['nombre']}")
                    mensajes = db.get_messages_between(current_user_id(), receptor_id)
                    if mensajes:
                        for m in mensajes:
                            autor = "Tú" if m["emisor_id"] == current_user_id() else receptor["nombre"]
                            clase = "chat-right" if autor == "Tú" else "chat-left"
                            st.markdown(
                                f'<div class="chat-bubble {clase}"><b>{autor}:</b> {m["contenido"]}'
                                f'<span class="chat-time">{m["timestamp"][11:16]}</span></div>',
                                unsafe_allow_html=True,
                            )
                        st.markdown('<div style="clear:both;"></div>', unsafe_allow_html=True)
                    else:
                        st.info("No hay mensajes aún. Escribe el primero.")

                    with st.form("send_msg_form", clear_on_submit=True):
                        nuevo = st.text_input("Escribe un mensaje", key="new_msg_input", placeholder="Escribe aquí...")
                        col1, col2 = st.columns([5, 1])
                        with col2:
                            send_btn = st.form_submit_button("Enviar", use_container_width=True)
                        if send_btn:
                            if nuevo and nuevo.strip():
                                db.add_message(current_user_id(), receptor_id, nuevo.strip())
                                db.add_notification(receptor_id, "mensaje", f"Nuevo mensaje de {current_user_name() or 'Usuario'}")
                                rerun_safe()
                            else:
                                st.warning("Escribe un mensaje antes de enviar.")
                else:
                    st.warning("Usuario no encontrado.")
            else:
                st.info("👈 Selecciona una conversación o inicia un nuevo chat")


# ========== NOTIFICACIONES ==========
elif st.session_state.get("page") == "notificaciones":
    # (EN PRESENTACIÓN) Panel donde el usuario ve y marca notificaciones.
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para ver notificaciones.")
    else:
        notifs = db.get_notifications(current_user_id())
        if notifs:
            for n in notifs:
                estado = "Leído" if n.get("leido") else "Nuevo"
                st.write(f"- {n.get('mensaje')} ({n.get('fecha')[:16]}) — {estado}")
                if not n.get("leido"):
                    if st.button(f"Marcar leído {n['id']}", key=f"marcar_{n['id']}"):
                        db.mark_notification_read(n['id'])
                        rerun_safe()
        else:
            st.info("No tienes notificaciones.")


# ========== PERFIL ==========
elif st.session_state.get("page") == "perfil":
    # (EN PRESENTACIÓN) Muestra el perfil del usuario logueado, sus publicaciones y estadísticas.
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para ver tu perfil.")
    else:
        user = db.get_user_by_id(current_user_id())
        if not user:
            st.warning("Usuario no encontrado.")
        else:
            st.write(f"**Nombre:** {user['nombre']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Comuna:** {user['comuna'] or '-'}")
            st.write(f"**Bio:** {user['bio'] or '-'}")

            st.markdown("---")
            st.subheader("⭐ Valoraciones")

            try:
                prom = db.get_promedio_calificacion(user["id"])
                if prom and prom > 0:
                    st.metric("Calificación promedio", f"{prom} / 5", "⭐")
                else:
                    st.info("Aún no tiene evaluaciones.")
            except Exception:
                st.warning("No se pudo cargar el promedio de calificaciones.")

            try:
                stats = db.get_estadisticas_trabajador(user["id"])
                if stats and stats.get('total_evaluaciones', 0) > 0:
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Trabajos completados", stats['trabajos_completados'])
                    with col2:
                        st.metric("Evaluaciones", stats['total_evaluaciones'])
                    with col3:
                        st.metric("Recomendaciones", stats['recomendaciones'])
            except Exception:
                st.warning("No se pudieron cargar las estadísticas.")

            st.markdown("---")
            st.markdown("### 📝 Reseñas de clientes")
            try:
                evaluaciones = db.get_evaluaciones_trabajador(user["id"])
                if not evaluaciones or len(evaluaciones) == 0:
                    st.write("Aún no tiene reseñas.")
                else:
                    for ev in evaluaciones:
                        with st.expander(f"⭐ {ev.get('calificacion', 0)}/5 - {ev.get('cliente_nombre', 'Anónimo')} ({ev.get('fecha', '')[:10]})"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Calificación general:** ⭐ {ev.get('calificacion', 0)} / 5")
                                st.write(f"**Puntualidad:** {ev.get('puntualidad', 0)} / 5")
                                st.write(f"**Calidad:** {ev.get('calidad', 0)} / 5")
                            with col2:
                                st.write(f"**Comunicación:** {ev.get('comunicacion', 0)} / 5")
                                st.write(f"**¿Recomendaría?:** {'✅ Sí' if ev.get('recomendaria') == 1 else '❌ No'}")
                            if ev.get('comentario'):
                                st.write(f"**Comentario:** {ev['comentario']}")
                            else:
                                st.write("**Comentario:** _Sin comentario_")
                            st.caption(f"Servicio: {ev.get('servicio_nombre', 'N/A')}")
            except Exception as e:
                st.error(f"Error al cargar las reseñas: {str(e)}")
                st.write("No se pudieron cargar las reseñas en este momento.")

            st.markdown("---")
            st.subheader("Tus publicaciones")
            user_services = db.get_user_services(current_user_id())
            if user_services:
                for s in user_services:
                    st.write(f"- {s['service']} ({s['category']}) — {s.get('comuna') or 'Sin comuna'} — Precio: {('$'+str(s['price'])) if s.get('price') else 'No informado'}")
            else:
                st.write("Aún no has publicado servicios.")

            st.markdown("---")
            st.write("### Publicar un servicio")
            cat = st.selectbox("Categoría", [""] + list(opciones_map.keys()), key="pub_cat_select")
            if cat:
                st.session_state.publish_cat = cat
                sublista = opciones_map.get(cat, [])
                if sublista:
                    cols_per_row = 3
                    for i in range(0, len(sublista), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for idx, opt in enumerate(sublista[i:i + cols_per_row]):
                            with cols[idx]:
                                if st.button(opt, key=f"pub_opt_{i+idx}"):
                                    st.session_state.publish_service = opt
                                    rerun_safe()

            if st.session_state.get("publish_service"):
                st.write(f"Has seleccionado: **{st.session_state.publish_service}**")
                with st.form("publish_service_form"):
                    comuna_sel = st.selectbox("Comuna donde ofreces (opcional)", [""] + comunas_santiago, key="pub_comuna_select")
                    price_input = st.text_input("Precio (opcional)", key="pub_price_input")
                    if st.form_submit_button("Publicar servicio"):
                        service_name = st.session_state.publish_service
                        category_name = st.session_state.publish_cat or cat
                        comuna_val = comuna_sel if comuna_sel else None
                        try:
                            price_val = float(price_input) if price_input.strip() else None
                        except:
                            st.warning("Precio inválido; usa sólo números.")
                            price_val = None
                        sid = db.add_service(current_user_id(), category_name, service_name, comuna_val, price_val)
                        if sid:
                            st.success("Servicio publicado correctamente")
                            st.session_state.publish_cat = None
                            st.session_state.publish_service = None
                            rerun_safe()
                        else:
                            st.error("No se pudo publicar el servicio.")

            st.markdown("---")
            if st.button("Editar perfil", key="editar_perfil_btn"):
                with st.form("edit_profile_form"):
                    nuevo_nombre = st.text_input("Nombre", user["nombre"], key="edit_nombre")
                    nueva_bio = st.text_area("Bio", user["bio"] or "", key="edit_bio")
                    default_idx = 0
                    if user.get("comuna") in comunas_santiago:
                        try:
                            default_idx = comunas_santiago.index(user.get("comuna")) + 1
                        except Exception:
                            default_idx = 0
                    nueva_comuna = st.selectbox("Comuna", [""] + comunas_santiago, index=default_idx, key="edit_comuna")
                    if st.form_submit_button("Guardar cambios"):
                        db.update_user_profile(current_user_id(), nuevo_nombre, nueva_bio, nueva_comuna)
                        st.success("Perfil actualizado")
                        rerun_safe()


# ========== MIS TRABAJOS ==========
elif st.session_state.get("page") == "mis_trabajos":
    # (EN PRESENTACIÓN) Aquí el usuario revisa trabajos solicitados y recibidos.
    st.markdown('<h1 class="conecta-title">📋 Mis Trabajos</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para ver tus trabajos.")
    else:
        tab1, tab2 = st.tabs(["📤 Solicitados por mí", "📥 Recibidos (como trabajador)"])
        with tab1:
            st.subheader("Trabajos que has solicitado")
            trabajos_cliente = db.get_trabajos_cliente(current_user_id())
            if trabajos_cliente:
                for trabajo in trabajos_cliente:
                    estado_emoji = {"pendiente": "⏳", "aceptado": "✅", "rechazado": "❌", "completado": "🎉", "evaluado": "⭐", "cancelado": "🚫"}
                    emoji = estado_emoji.get(trabajo['estado'], "📋")
                    with st.expander(f"{emoji} {trabajo['servicio_nombre']} - {trabajo['trabajador_nombre']} ({trabajo['estado'].upper()})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Fecha:** {trabajo['fecha_solicitada']}")
                            st.write(f"**Hora:** {trabajo['hora_solicitada']}")
                            st.write(f"**Dirección:** {trabajo['direccion']}")
                        with col2:
                            st.write(f"**Estado:** {trabajo['estado'].upper()}")
                            if trabajo.get('precio_propuesto'):
                                st.write(f"**Precio propuesto:** ${int(trabajo['precio_propuesto'])}")
                            if trabajo.get('precio_final'):
                                st.write(f"**Precio final:** ${int(trabajo['precio_final'])}")
                        st.write(f"**Descripción:** {trabajo['descripcion']}")
                        if trabajo['estado'] == "completado":
                            if st.button("⭐ Evaluar trabajo", key=f"evaluar_{trabajo['id']}"):
                                st.session_state.ver_trabajo_id = trabajo['id']
                                st.session_state.page = "evaluar_trabajo"
                                rerun_safe()
            else:
                st.info("No has solicitado ningún trabajo aún.")
        with tab2:
            st.subheader("Trabajos recibidos")
            trabajos_trabajador = db.get_trabajos_trabajador(current_user_id())
            if trabajos_trabajador:
                for trabajo in trabajos_trabajador:
                    estado_emoji = {"pendiente": "⏳", "aceptado": "✅", "rechazado": "❌", "completado": "🎉", "evaluado": "⭐", "cancelado": "🚫"}
                    emoji = estado_emoji.get(trabajo['estado'], "📋")
                    with st.expander(f"{emoji} {trabajo['servicio_nombre']} - Cliente: {trabajo['cliente_nombre']} ({trabajo['estado'].upper()})"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Fecha:** {trabajo['fecha_solicitada']}")
                            st.write(f"**Hora:** {trabajo['hora_solicitada']}")
                            st.write(f"**Dirección:** {trabajo['direccion']}")
                        with col2:
                            st.write(f"**Estado:** {trabajo['estado'].upper()}")
                            if trabajo.get('precio_propuesto'):
                                st.write(f"**Precio propuesto:** ${int(trabajo['precio_propuesto'])}")
                            if trabajo.get('precio_final'):
                                st.write(f"**Precio final:** ${int(trabajo['precio_final'])}")
                        st.write(f"**Descripción:** {trabajo['descripcion']}")
                        if trabajo['estado'] == "pendiente":
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button("✅ Aceptar", key=f"aceptar_{trabajo['id']}", use_container_width=True):
                                    db.update_trabajo_estado(trabajo['id'], "aceptado")
                                    db.add_notification(trabajo['cliente_id'], "trabajo_aceptado", f"{current_user_name()} aceptó tu solicitud de {trabajo['servicio_nombre']}")
                                    st.success("Trabajo aceptado")
                                    rerun_safe()
                            with col_btn2:
                                if st.button("❌ Rechazar", key=f"rechazar_{trabajo['id']}", use_container_width=True):
                                    db.update_trabajo_estado(trabajo['id'], "rechazado")
                                    db.add_notification(trabajo['cliente_id'], "trabajo_rechazado", f"{current_user_name()} rechazó tu solicitud de {trabajo['servicio_nombre']}")
                                    st.warning("Trabajo rechazado")
                                    rerun_safe()
                        elif trabajo['estado'] == "aceptado":
                            if st.button("🎉 Marcar como completado", key=f"completar_{trabajo['id']}"):
                                db.update_trabajo_estado(trabajo['id'], "completado")
                                db.add_notification(trabajo['cliente_id'], "trabajo_completado", f"Tu trabajo con {current_user_name()} fue completado. ¡Evalúalo!")
                                st.success("Trabajo marcado como completado")
                                rerun_safe()
            else:
                st.info("No has recibido solicitudes de trabajo aún.")


# ---------- SOLICITAR SERVICIO ----------
elif st.session_state.get("page") == "solicitar_servicio":
    # (EN PRESENTACIÓN) Flujo que usa el cliente para pedir un servicio a un trabajador.
    st.markdown('<h1 class="conecta-title">✅ Solicitar Servicio</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para solicitar un servicio.")
        if st.button("Ir a iniciar sesión"):
            st.session_state.page = "login"
            rerun_safe()
    else:
        servicio_id = st.session_state.get("solicitar_servicio_id")
        trabajador_id = st.session_state.get("solicitar_trabajador_id")
        if not servicio_id or not trabajador_id:
            st.error("Error: No se encontró el servicio.")
            if st.button("⬅️ Volver"):
                st.session_state.page = "resultados"
                rerun_safe()
        else:
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
            if servicio:
                servicio = dict(servicio)
                st.info(f"📋 **Servicio:** {servicio['service']} ({servicio['category']})")
                st.info(f"👷 **Trabajador:** {servicio['trabajador_nombre']}")
                if servicio.get('price'):
                    st.info(f"💰 **Precio:** ${int(servicio['price'])}")
                st.markdown("---")
                st.subheader("Completa los detalles de tu solicitud:")
                with st.form("solicitud_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        fecha = st.date_input("📅 Fecha deseada", min_value=datetime.now().date())
                    with col2:
                        hora = st.time_input("🕐 Hora aproximada")
                    direccion = st.text_input("📍 Dirección completa", placeholder="Calle, número, comuna, depto/casa")
                    descripcion = st.text_area("📝 Describe el trabajo que necesitas", placeholder="Detalles específicos del servicio que necesitas...", height=100)
                    if not servicio.get('price'):
                        precio_propuesto = st.number_input("💵 Propón un precio", min_value=0, step=1000)
                    else:
                        precio_propuesto = servicio['price']
                    col_btn1, col_btn2 = st.columns(2)
                    with col_btn1:
                        submit = st.form_submit_button("✅ Enviar solicitud", use_container_width=True)
                    with col_btn2:
                        cancel = st.form_submit_button("❌ Cancelar", use_container_width=True)
                    if submit:
                        if not direccion or not descripcion:
                            st.error("Por favor completa todos los campos obligatorios.")
                        else:
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
                            if trabajo_id:
                                db.add_notification(
                                    trabajador_id,
                                    "solicitud_trabajo",
                                    f"Nueva solicitud de {current_user_name()} para {servicio['service']}"
                                )
                                st.success("¡Solicitud enviada! El trabajador recibirá una notificación.")
                                st.balloons()
                                st.session_state.solicitar_servicio_id = None
                                st.session_state.solicitar_trabajador_id = None
                                st.session_state.page = "mis_trabajos"
                                rerun_safe()
                            else:
                                st.error("Error al crear la solicitud. Intenta nuevamente.")
                    if cancel:
                        st.session_state.solicitar_servicio_id = None
                        st.session_state.solicitar_trabajador_id = None
                        st.session_state.page = "resultados"
                        rerun_safe()


# ---------- EVALUAR TRABAJO ----------
elif st.session_state.get("page") == "evaluar_trabajo":
    # (EN PRESENTACIÓN) Formulario para que el cliente evalúe el trabajo completado.
    trabajo_id = st.session_state.get("ver_trabajo_id")
    if not trabajo_id:
        st.error("No se encontró el trabajo para evaluar.")
    else:
        trabajo = db.get_trabajo_by_id(trabajo_id)
        if not trabajo or trabajo['cliente_id'] != current_user_id():
            st.warning("Solo el cliente puede evaluar el trabajo.")
        else:
            st.markdown('<h1 class="conecta-title">⭐ Evaluar Trabajo</h1>', unsafe_allow_html=True)
            st.write(f"**Servicio:** {trabajo['servicio_nombre']}")
            st.write(f"**Trabajador:** {trabajo['trabajador_nombre']}")
            st.markdown("---")
            calificacion = st.slider("Calificación general", 1, 5, 5, key="eval_calificacion")
            puntualidad = st.slider("Puntualidad", 1, 5, 5, key="eval_puntualidad")
            calidad = st.slider("Calidad del trabajo", 1, 5, 5, key="eval_calidad")
            comunicacion = st.slider("Comunicación", 1, 5, 5, key="eval_comunicacion")
            recomendaria = st.selectbox("¿Lo recomendarías?", [1, 0], format_func=lambda x: "Sí" if x == 1 else "No", key="eval_recomendaria")
            comentario = st.text_area("Comentario (opcional)", key="eval_comentario", height=120)
            if st.button("Enviar evaluación", key="enviar_eval"):
                db.create_evaluacion(trabajo_id, trabajo["cliente_id"], trabajo["trabajador_id"],
                                     int(calificacion), comentario or "", int(puntualidad), int(calidad),
                                     int(comunicacion), int(recomendaria))
                db.add_notification(trabajo["trabajador_id"], "evaluacion_recibida", f"Has recibido una nueva evaluación de {current_user_name()}")
                st.success("¡Gracias! Tu evaluación fue enviada.")
                st.session_state.ver_trabajo_id = None
                st.session_state.page = "mis_trabajos"
                rerun_safe()


# ---------- LOGIN / REGISTRO ----------
elif st.session_state.get("page") in ["login", "registro"]:
    if st.session_state.get("page") == "login":
        st.markdown('<h1 class="conecta-title">🔐 Iniciar sesión</h1>', unsafe_allow_html=True)
        with st.form("login_form"):
            email = st.text_input("Correo electrónico", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pwd")
            if st.form_submit_button("Entrar"):
                user = auth.login_user(email.strip(), password)
                if user:
                    st.session_state.user = {"id": user["id"], "nombre": user["nombre"], "email": user["email"]}
                    st.session_state.user_id = user["id"]
                    st.success("Inicio de sesión correcto")
                    st.session_state.page = "inicio"
                    rerun_safe()
                else:
                    st.error("Credenciales incorrectas")
    else:
        st.markdown('<h1 class="conecta-title">📝 Registrarse</h1>', unsafe_allow_html=True)
        with st.form("register_form"):
            nombre = st.text_input("Nombre completo", key="reg_nombre")
            email_r = st.text_input("Correo electrónico", key="reg_email")
            pwd_r = st.text_input("Contraseña", type="password", key="reg_pwd")
            bio_r = st.text_area("Descripción / Bio (opcional)", key="reg_bio")
            comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago, key="reg_comuna")
            if st.form_submit_button("Registrarse"):
                new_id = auth.register_user(nombre.strip(), email_r.strip(), pwd_r, bio_r, comuna_r)
                if new_id:
                    st.success("Cuenta creada. Puedes iniciar sesión.")
                    st.session_state.page = "login"
                    rerun_safe()
                else:
                    st.error("No se pudo crear la cuenta (correo ya existe o faltan datos).")


# ---------- fallback ----------
else:
    st.session_state.page = "inicio"
    rerun_safe()
