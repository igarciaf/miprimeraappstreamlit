# app.py
import streamlit as st
import db
import auth

# Inicializar DB (asegura tablas)
db.init_db()

st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Helpers / rerun
# -------------------------
def rerun_safe():
    # usar experimental_rerun por compatibilidad
    try:
        st.experimental_rerun()
    except Exception:
        try:
            st.rerun()
        except Exception:
            pass

# Helper seguro para obtener user id / name
def current_user_id():
    # prioriza user_id si está presente y no nulo
    uid = st.session_state.get("user_id")
    if uid:
        return uid
    u = st.session_state.get("user")
    if isinstance(u, dict) and u.get("id"):
        return u.get("id")
    return None

def current_user_name():
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
# session defaults
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
    "publish_service": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -------------------------
# Comunas (lista completa de Santiago)
# -------------------------
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
st.markdown(
    """
    <style>
    .top-bar{position:fixed; top:0; left:0; right:0; height:64px;
    background:#2E8B57; color:white; display:flex; align-items:center; justify-content:center;
    font-size:22px; font-weight:700; z-index:9999; box-shadow:0 2px 8px rgba(0,0,0,0.08);}
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    </style>
    <div class="top-bar">ConectaServicios</div>
    """, unsafe_allow_html=True
)
if st.button("🏠 Inicio", key="home_btn"):
    st.session_state.page = "inicio"
    rerun_safe()

# -------------------------
# Sidebar navigation (simple)
# -------------------------
pages_display = [
    "Inicio", "Subcategoría", "Ubicación", "Resultados", "Perfil público",
    "Iniciar sesión", "Registrarse", "Perfil", "Chats", "Notificaciones"
]

mapping = {
    "Inicio": "inicio",
    "Subcategoría": "subcategoria",
    "Ubicación": "ubicacion",
    "Resultados": "resultados",
    "Perfil público": "perfil_publico",
    "Iniciar sesión": "login",
    "Registrarse": "registro",
    "Perfil": "perfil",
    "Chats": "chats",
    "Notificaciones": "notificaciones",
}

# invert mapping to compute current label for radio
def page_to_label(page_key):
    for label, key in mapping.items():
        if key == page_key:
            return label
    return "Inicio"

with st.sidebar:
    st.markdown("### Navegación")
    if current_user_name():
        st.markdown(f"**{current_user_name()}**")
    else:
        st.markdown("**Invitado**")
    # determine current index
    current_label = page_to_label(st.session_state.get("page", "inicio"))
    try:
        sel_index = pages_display.index(current_label)
    except Exception:
        sel_index = 0
    selection = st.radio("Ir a:", pages_display, index=sel_index)
    selected_page = mapping.get(selection, "inicio")
    # only change if different
    if selected_page != st.session_state.get("page"):
        st.session_state.page = selected_page
        rerun_safe()

    st.markdown("---")
    if current_user_id():
        if st.button("🔒 Cerrar sesión"):
            st.session_state.user = None
            st.session_state.user_id = 0
            st.session_state.selected_user_id = None
            st.session_state.page = "inicio"
            rerun_safe()

# -------------------------
# Styles
# -------------------------
st.markdown("""
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
""", unsafe_allow_html=True)

# -------------------------
# Reusable options map
# -------------------------
opciones_map = {
    "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
    "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
    "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
    "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
}

# ============================
#        PÁGINA DE INICIO
# ============================
if st.session_state.get("page") == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    st.subheader("Selecciona una categoría:")

    c1, c2 = st.columns(2)

    # ---- BOTONES ARREGLADOS (SIN rerun_safe) ----
with c1:
    if st.button("Cuidado de mascotas", key="btn_mascotas"):
        st.session_state.categoria = "Mascotas"
        st.session_state.page = "subcategoria"
        rerun_safe()

    if st.button("Limpieza y hogar", key="btn_hogar"):
        st.session_state.categoria = "Hogar"
        st.session_state.page = "subcategoria"
        rerun_safe()

with c2:
    if st.button("Clases particulares", key="btn_clases"):
        st.session_state.categoria = "Clases"
        st.session_state.page = "subcategoria"
        rerun_safe()

    if st.button("Cuidado de niños", key="btn_ninos"):
        st.session_state.categoria = "Niños"
        st.session_state.page = "subcategoria"
        rerun_safe()


    st.markdown("---")
    st.subheader("Buscar por servicio")
    termino = st.text_input("¿Qué servicio necesitas?", key="search_term")
    comuna_filter = st.selectbox("Filtrar por comuna (opcional):", [""] + comunas_santiago, key="search_comuna")
    if st.button("Buscar"):
        if termino and termino.strip():
            comuna_sel = comuna_filter if comuna_filter else None
            servicios = db.get_services_filtered(termino.strip(), comuna_sel)
            if servicios:
                st.success(f"{len(servicios)} resultado(s) encontrados")
                for s in servicios:
                    st.markdown(
                        f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>'
                        f'Proveedor: <b>{s["user_nombre"]}</b> — {s.get("user_comuna") or "Sin comuna"}<br>'
                        f'Precio: {("$"+str(s["price"])) if s.get("price") else "No informado"}<br>'
                        f'<i>{s.get("user_bio") or ""}</i></div>',
                        unsafe_allow_html=True
                    )
                    if st.button(f"Chatear con {s['user_nombre']}", key=f"chat_service_{s['id']}"):
                        st.session_state.selected_user_id = s["user_id"]
                        st.session_state.page = "chats"
                        rerun_safe()
            else:
                st.warning("No se encontraron servicios con ese término.")
        else:
            st.warning("Ingresa un término para buscar.")

# FIN DE LA PÁGINA DE INICIO

# SUBCATEGORIA
if st.session_state.get("page") == "subcategoria":

    st.markdown(
        f'<h1 class="conecta-title">Categoría: {st.session_state.get("categoria")}</h1>',
        unsafe_allow_html=True
    )

    if st.button("⬅️ Volver"):
        st.session_state.page = "inicio"
        rerun_safe()

    lista = opciones_map.get(st.session_state.get("categoria"), [])

    if lista:
        cols_per_row = 3
        for i in range(0, len(lista), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, opt in enumerate(lista[i:i+cols_per_row]):
                with cols[idx]:
                    if st.button(opt, key=f"opt_{i+idx}"):
                        st.session_state.servicio = opt
                        st.session_state.page = "ubicacion"
                        rerun_safe()
    else:
        st.info("No hay opciones para esta categoría.")

# UBICACION
elif st.session_state.get("page") == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        st.session_state.page = "subcategoria"
        rerun_safe()
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", comunas_santiago)
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        st.session_state.page = "resultados"
        rerun_safe()

# RESULTADOS
elif st.session_state.get("page") == "resultados":
    servicio = st.session_state.get("servicio", "")
    ubic = st.session_state.get("ubicacion", "")
    st.markdown(f'<h1 class="conecta-title">Resultados: {servicio} — {ubic}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        st.session_state.page = "ubicacion"
        rerun_safe()
    term = servicio or ""
    comuna_name = ubic.split(",")[0] if ubic else None
    servicios = db.get_services_filtered(term, comuna_name)
    if servicios:
        for s in servicios:
            st.markdown(
                f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>'
                f'Proveedor: <b>{s["user_nombre"]}</b> — {s.get("user_comuna") or "Sin comuna"}<br>'
                f'Precio: {("$"+str(s["price"])) if s.get("price") else "No informado"}<br>'
                f'<i>{s.get("user_bio") or ""}</i></div>',
                unsafe_allow_html=True
            )
            if st.button(f"Chatear con {s['user_nombre']}", key=f"chat_result_{s['id']}"):
                st.session_state.selected_user_id = s["user_id"]
                st.session_state.page = "chats"
                rerun_safe()
    else:
        st.info("No hay servicios publicados que coincidan (aún).")

# PERFIL PÚBLICO
elif st.session_state.get("page") == "perfil_publico":
    r = st.session_state.get("perfil_usuario", {"nombre":"Usuario"})
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        st.session_state.page = "resultados"
        rerun_safe()
    st.write(f"**Servicio:** {r.get('servicio','-')}")
    st.write(f"**Valoración:** {r.get('valoracion','-')}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio (simulación).")

# CHATS
elif st.session_state.get("page") == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    if not current_user_id():
        st.warning("Debes iniciar sesión para usar el chat.")
    else:
        # seleccionar receptor o usar el seleccionado por búsqueda
        receptor_id = st.session_state.get("selected_user_id")
        if receptor_id is None:
            # mostrar lista simple de otros usuarios
            conn = db.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM users WHERE id != ?", (current_user_id(),))
            rows = cur.fetchall()
            conn.close()
            others = [dict(r) for r in rows]
            if not others:
                st.info("No hay otros usuarios registrados aún.")
            else:
                names = [o["nombre"] for o in others]
                sel = st.selectbox("Selecciona un usuario", names)
                receptor = next(o for o in others if o["nombre"] == sel)
                receptor_id = receptor["id"]
        receptor = db.get_user_by_id(receptor_id)
        if receptor:
            st.subheader(f"Chat con {receptor['nombre']}")
            mensajes = db.get_messages_between(current_user_id(), receptor_id)
            if mensajes:
                for m in mensajes:
                    autor = "Tú" if m["emisor_id"] == current_user_id() else receptor['nombre']
                    clase = "chat-right" if autor == "Tú" else "chat-left"
                    st.markdown(f'<div class="chat-bubble {clase}"><b>{autor}:</b> {m["contenido"]}<span class="chat-time">{m["timestamp"][:16]}</span></div>', unsafe_allow_html=True)
            else:
                st.info("No hay mensajes aún. Escribe el primero.")
            with st.form("send_msg_form", clear_on_submit=True):
                nuevo = st.text_input("Escribe un mensaje", key="new_msg")
                if st.form_submit_button("Enviar"):
                    if nuevo and nuevo.strip():
                        db.add_message(current_user_id(), receptor_id, nuevo.strip())
                        db.add_notification(receptor_id, "mensaje", f"Nuevo mensaje de {current_user_name() or 'Usuario'}")
                        st.success("Mensaje enviado")
                        st.session_state.selected_user_id = None
                        rerun_safe()
                    else:
                        st.warning("Escribe un mensaje antes de enviar.")

# NOTIFICACIONES
elif st.session_state.get("page") == "notificaciones":
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
                    if st.button(f"Marcar leído {n['id']}"):
                        db.mark_notification_read(n['id'])
                        rerun_safe()
        else:
            st.info("No tienes notificaciones.")

# PERFIL (y publicar servicio)
elif st.session_state.get("page") == "perfil":
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

            st.subheader("Tus publicaciones")
            user_services = db.get_user_services(current_user_id())
            if user_services:
                for s in user_services:
                    st.write(f"- {s['service']} ({s['category']}) — {s.get('comuna') or 'Sin comuna'} — Precio: {('$'+str(s['price'])) if s.get('price') else 'No informado'}")
            else:
                st.write("Aún no has publicado servicios.")

            st.markdown("---")
            st.write("### Publicar un servicio (igual al flujo de búsqueda)")
            cat = st.selectbox("Categoría", [""] + list(opciones_map.keys()), key="pub_cat_select")
            if cat:
                st.session_state.publish_cat = cat
                sublista = opciones_map.get(cat, [])
                if sublista:
                    cols_per_row = 3
                    for i in range(0, len(sublista), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for idx, opt in enumerate(sublista[i:i+cols_per_row]):
                            with cols[idx]:
                                if st.button(opt, key=f"pub_opt_{i+idx}"):
                                    st.session_state.publish_service = opt
                                    rerun_safe()
                if st.session_state.publish_service:
                    st.write(f"Has seleccionado: **{st.session_state.publish_service}**")
                    with st.form("publish_service_form"):
                        comuna_sel = st.selectbox("Comuna donde ofreces (opcional)", [""] + comunas_santiago, key="pub_comuna")
                        price_input = st.text_input("Precio (opcional)", key="pub_price")
                        if st.form_submit_button("Publicar servicio"):
                            service_name = st.session_state.publish_service
                            category_name = st.session_state.publish_cat or cat
                            comuna_val = comuna_sel if comuna_sel else None
                            try:
                                price_val = float(price_input) if price_input.strip() else None
                            except ValueError:
                                st.warning("Precio inválido; usa solo números.")
                                price_val = None
                            sid = db.add_service(current_user_id(), category_name, service_name, comuna_val, price_val)
                            if sid:
                                st.success("Servicio publicado correctamente")
                                st.session_state.publish_cat = None
                                st.session_state.publish_service = None
                                rerun_safe()
                            else:
                                st.error("No se pudo publicar el servicio (error interno).")
            st.markdown("---")
            if st.button("Editar perfil"):
                with st.form("edit_profile_form"):
                    nuevo_nombre = st.text_input("Nombre", user["nombre"])
                    nueva_bio = st.text_area("Bio", user["bio"] or "")
                    # select default index safely
                    default_idx = 0
                    if user.get("comuna") in comunas_santiago:
                        try:
                            default_idx = comunas_santiago.index(user.get("comuna")) + 1
                        except Exception:
                            default_idx = 0
                    nueva_comuna = st.selectbox("Comuna", [""] + comunas_santiago, index=default_idx)
                    if st.form_submit_button("Guardar cambios"):
                        db.update_user_profile(current_user_id(), nuevo_nombre, nueva_bio, nueva_comuna)
                        st.success("Perfil actualizado")
                        rerun_safe()

# LOGIN / REGISTRO
elif st.session_state.get("page") in ["login","registro"]:
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

# fallback
else:
    st.session_state.page = "inicio"
    rerun_safe()
