# app.py
import streamlit as st
import db
import auth
from datetime import datetime

# Inicializar DB
db.init_db()

st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# rerun seguro
def rerun_safe():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# session defaults
defaults = {
    "page": "inicio",
    "user_id": 0,
    "user": None,
    "categoria": None,
    "servicio": None,
    "ubicacion": None,
    "perfil_usuario": None,
    "selected_user_id": None,
    # flags para publicar servicio
    "publish_cat": None,
    "publish_service": None
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# comunas (misma lista que antes)
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

# helpers
def set_page(page_name: str):
    st.session_state.page = page_name
    rerun_safe()

def login_set(user: dict):
    st.session_state.user_id = user["id"]
    st.session_state.user = user

def logout():
    st.session_state.user_id = 0
    st.session_state.user = None
    set_page("inicio")

def require_login(redirect_to="login"):
    st.warning("Debes iniciar sesión para ver esta sección.")
    if st.button("Ir a Iniciar sesión"):
        set_page(redirect_to)

# topbar + home button
st.markdown("""
    <style>
    .top-bar{position:fixed; top:0; left:0; right:0; height:64px;
    background:#2E8B57; color:white; display:flex; align-items:center; justify-content:center;
    font-size:22px; font-weight:700; z-index:9999; box-shadow:0 2px 8px rgba(0,0,0,0.08);}
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    </style>
    <div class="top-bar">ConectaServicios</div>
    """, unsafe_allow_html=True)

if st.button("🏠 Inicio", key="home_btn"):
    set_page("inicio")

# sidebar navigation (no forzar páginas internas)
pages_display = ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Chats", "Notificaciones"]
pages_map = {
    "Inicio": "inicio",
    "Iniciar sesión": "login",
    "Registrarse": "registro",
    "Perfil": "perfil",
    "Chats": "chats",
    "Notificaciones": "notificaciones"
}
with st.sidebar:
    st.markdown("### 🌐 Navegación")
    if st.session_state.user:
        st.markdown(f"**{st.session_state.user.get('nombre')}**")
    else:
        st.markdown("**Invitado**")
    # radio safe
    current_label = None
    for label, key in pages_map.items():
        if key == st.session_state.page:
            current_label = label
            break
    if current_label is None:
        current_label = "Inicio"
    sel_index = pages_display.index(current_label) if current_label in pages_display else 0
    selection = st.radio("Ir a:", pages_display, index=sel_index)
    selected_page = pages_map.get(selection, "inicio")
    if st.session_state.page in pages_map.values():
        if selected_page != st.session_state.page:
            set_page(selected_page)

    st.markdown("---")
    if st.session_state.user:
        if st.button("🚪 Cerrar sesión"):
            logout()

# estilos
st.markdown("""
    <style>
    div.stButton > button { height:76px; width:200px; background:#2E8B57; color:white; border-radius:12px; font-size:17px; margin:6px 8px; border:none; }
    div.stButton > button:hover { background-color:#276e47; transform: translateY(-1px); }
    .conecta-title { text-align:center; margin-bottom:8px; }
    .chat-bubble { padding:10px 12px; border-radius:12px; margin:6px 0; display:inline-block; max-width:70%; word-wrap:break-word; }
    .chat-right { background:#DCF8C6; text-align:right; float:right; clear:both; }
    .chat-left { background:#F1F0F0; text-align:left; float:left; clear:both; }
    .chat-time { font-size:10px; color:#666; margin-top:4px; display:block; }
    .service-card { border:1px solid rgba(0,0,0,0.06); padding:12px; border-radius:8px; margin-bottom:10px; }
    </style>
    """, unsafe_allow_html=True)

# opciones y mapas de subcategorías (reutilizables)
opciones_map = {
    "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
    "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
    "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
    "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
}

# -------------------------
# PÁGINAS
# -------------------------

# INICIO
if st.session_state.page == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    st.subheader("Selecciona una categoría:")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Cuidado de mascotas", key="btn_mascotas"):
            st.session_state.categoria = "Mascotas"
            set_page("subcategoria")
        if st.button("Limpieza y hogar", key="btn_hogar"):
            st.session_state.categoria = "Hogar"
            set_page("subcategoria")
    with c2:
        if st.button("Clases particulares", key="btn_clases"):
            st.session_state.categoria = "Clases"
            set_page("subcategoria")
        if st.button("Cuidado de niños", key="btn_ninos"):
            st.session_state.categoria = "Niños"
            set_page("subcategoria")
    st.markdown("---")

    # búsqueda por término + opcional filtro comuna
    st.subheader("Buscar por servicio")
    termino = st.text_input("¿Qué servicio necesitas?", key="search_term")
    comuna_filter = st.selectbox("Filtrar por comuna (opcional):", [""] + comunas_santiago, key="search_comuna")
    if st.button("Buscar"):
        if termino.strip():
            comuna_selected = comuna_filter if comuna_filter else None
            servicios = db.get_services_filtered(termino.strip(), comuna_selected)
            if servicios:
                st.success(f"{len(servicios)} resultado(s) encontrados")
                for s in servicios:
                    st.markdown(f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>Proveedor: <b>{s["user_nombre"]}</b> — {s.get("user_comuna") or "Sin comuna"}<br>Precio: {(" $"+str(s["price"])) if s.get("price") else "No informado"}<br><i>{s.get("user_bio") or ""}</i></div>', unsafe_allow_html=True)
                    if st.button(f"Chatear con {s['user_nombre']}", key=f"chat_service_{s['id']}"):
                        st.session_state.selected_user_id = s["user_id"]
                        set_page("chats")
            else:
                st.warning("No se encontraron servicios con ese término.")
        else:
            st.warning("Ingresa un término para buscar.")

# SUBCATEGORIA
elif st.session_state.page == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("inicio")
    lista = opciones_map.get(st.session_state.categoria, [])
    if lista:
        cols_per_row = 3
        for i in range(0, len(lista), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, opt in enumerate(lista[i:i+cols_per_row]):
                with cols[idx]:
                    if st.button(opt, key=f"opt_{i+idx}"):
                        st.session_state.servicio = opt
                        set_page("ubicacion")
    else:
        st.info("No hay opciones para esta categoría.")

# UBICACION
elif st.session_state.page == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", comunas_santiago)
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")

# RESULTADOS
elif st.session_state.page == "resultados":
    servicio = st.session_state.get("servicio", "")
    ubic = st.session_state.get("ubicacion", "")
    st.markdown(f'<h1 class="conecta-title">Resultados: {servicio} — {ubic}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("ubicacion")

    # buscar servicios que coincidan con nombre del servicio y comuna (si aplica)
    term = servicio or ""
    comuna_name = ubic.split(",")[0] if ubic else None
    servicios = db.get_services_filtered(term, comuna_name)
    if servicios:
        for s in servicios:
            st.markdown(f'<div class="service-card"><b>{s["service"]}</b> — {s["category"]} <br>Proveedor: <b>{s["user_nombre"]}</b> — {s.get("user_comuna") or "Sin comuna"}<br>Precio: {(" $"+str(s["price"])) if s.get("price") else "No informado"}<br><i>{s.get("user_bio") or ""}</i></div>', unsafe_allow_html=True)
            if st.button(f"Chatear con {s['user_nombre']}", key=f"chat_result_{s['id']}"):
                st.session_state.selected_user_id = s["user_id"]
                set_page("chats")
    else:
        st.info("No hay servicios publicados que coincidan (aún).")

# PERFIL PÚBLICO
elif st.session_state.page == "perfil_publico":
    r = st.session_state.get("perfil_usuario", {"nombre":"Usuario"})
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("resultados")
    st.write(f"**Servicio:** {r.get('servicio','-')}")
    st.write(f"**Valoración:** {r.get('valoracion','-')}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio (simulación).")

# CHATS
elif st.session_state.page == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    if st.session_state.user_id == 0:
        require_login("login")
    else:
        # si arrived from a service, selected_user_id puede estar definido
        if st.session_state.selected_user_id:
            receptor_id = st.session_state.selected_user_id
        else:
            # elegir usuario manualmente
            conn = db.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT id, nombre FROM users WHERE id != ?", (st.session_state.user_id,))
            rows = cur.fetchall()
            conn.close()
            others = [dict(r) for r in rows]
            if not others:
                st.info("No hay otros usuarios registrados aún.")
                return
            names = [o["nombre"] for o in others]
            selected = st.selectbox("Selecciona un usuario", names)
            receptor = next(o for o in others if o["nombre"] == selected)
            receptor_id = receptor["id"]

        receptor = db.get_user_by_id(receptor_id)
        if receptor:
            st.subheader(f"Chat con {receptor['nombre']}")
            mensajes = db.get_messages_between(st.session_state.user_id, receptor_id)
            if mensajes:
                for m in mensajes:
                    autor = "Tú" if m["emisor_id"] == st.session_state.user_id else receptor['nombre']
                    clase = "chat-right" if autor == "Tú" else "chat-left"
                    st.markdown(f'<div class="chat-bubble {clase}">{autor}: {m["contenido"]} <span class="chat-time">{m["timestamp"][:16]}</span></div>', unsafe_allow_html=True)
            else:
                st.info("No hay mensajes aún. Escribe el primero.")

            with st.form("send_msg_form", clear_on_submit=True):
                nuevo = st.text_input("Escribe un mensaje", key="new_msg")
                if st.form_submit_button("Enviar"):
                    if nuevo and nuevo.strip():
                        db.add_message(st.session_state.user_id, receptor_id, nuevo.strip())
                        db.add_notification(receptor_id, "mensaje", f"Nuevo mensaje de {db.get_user_by_id(st.session_state.user_id)['nombre']}")
                        st.success("Mensaje enviado")
                        # limpiar selected_user para que no se quede seleccionado accidentalmente
                        st.session_state.selected_user_id = None
                        rerun_safe()
                    else:
                        st.warning("Escribe un mensaje antes de enviar.")
        else:
            st.error("Usuario receptor no encontrado.")

# NOTIFICACIONES
elif st.session_state.page == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    if st.session_state.user_id == 0:
        require_login("login")
    else:
        notifs = db.get_notifications(st.session_state.user_id)
        if notifs:
            for n in notifs:
                estado = "Leído" if n.get("leido") else "Nuevo"
                st.write(f"- {n.get('mensaje')} ({n.get('fecha')[:16]}) — {estado}")
                if not n.get("leido"):
                    if st.button(f"Marcar leído {n['id']}"):
                        db.mark_notification_read(n['id'])
                        rerun_safe()
        else:
            st.info("No tienes notificaciones nuevas.")

# PERFIL PROPIO (y publicar servicio con flow similar a inicio)
elif st.session_state.page == "perfil":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    if st.session_state.user_id == 0:
        require_login("login")
    else:
        user = db.get_user_by_id(st.session_state.user_id)
        if not user:
            st.warning("No se encontró tu usuario.")
        else:
            st.write(f"**Nombre:** {user['nombre']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Comuna:** {user['comuna'] or '-'}")
            st.write(f"**Bio:** {user['bio'] or '-'}")

            st.subheader("Servicios que ofreces")
            skills = db.get_user_skills(st.session_state.user_id)
            if skills:
                st.write(", ".join(skills))
            else:
                st.write("No has agregado servicios tipo 'skill' todavía.")

            # lista de servicios publicados por el usuario (tabla services)
            st.subheader("Tus publicaciones")
            user_services = db.get_user_services(st.session_state.user_id)
            if user_services:
                for s in user_services:
                    st.markdown(f"- {s['service']} ({s['category']}) — {s.get('comuna') or 'Sin comuna'} — Precio: {('$'+str(s['price'])) if s.get('price') else 'No informado'}")
            else:
                st.write("Aún no has publicado servicios.")

            st.markdown("---")
            st.write("### Publicar un servicio (flujo similar a la pantalla principal)")
            st.write("1) Selecciona una categoría (igual que en Inicio)")
            # paso 1: escoger categoría
            cat = st.selectbox("Categoría", [""] + list(opciones_map.keys()), key="pub_cat_select")
            if cat:
                st.session_state.publish_cat = cat
                # mostrar subcategorías como botones en columnas (igual que en subcategoria)
                sublista = opciones_map.get(cat, [])
                if sublista:
                    cols_per_row = 3
                    st.write("2) Selecciona el servicio específico")
                    for i in range(0, len(sublista), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for idx, opt in enumerate(sublista[i:i+cols_per_row]):
                            with cols[idx]:
                                if st.button(opt, key=f"pub_opt_{i+idx}"):
                                    st.session_state.publish_service = opt
                                    rerun_safe()

                # una vez elegido el servicio, mostramos formulario final para comuna/price
                if st.session_state.publish_service:
                    st.write(f"Has seleccionado: **{st.session_state.publish_service}**")
                    with st.form("publish_service_form"):
                        comuna_sel = st.selectbox("Comuna donde ofreces (opcional)", [""] + comunas_santiago)
                        price_input = st.text_input("Precio (opcional, números)", key="pub_price")
                        if st.form_submit_button("Publicar servicio"):
                            # validaciones mínimas
                            service_name = st.session_state.publish_service
                            category_name = st.session_state.publish_cat or cat
                            comuna_val = comuna_sel if comuna_sel else None
                            try:
                                price_val = float(price_input) if price_input.strip() else None
                            except ValueError:
                                st.warning("Precio inválido. Usa solo números (ej: 5000 o 12.5).")
                                price_val = None
                            # guardar en DB
                            sid = db.add_service(st.session_state.user_id, category_name, service_name, comuna_val, price_val)
                            if sid:
                                st.success("Servicio publicado correctamente ✅")
                                # limpiar estados de publicación
                                st.session_state.publish_cat = None
                                st.session_state.publish_service = None
                                rerun_safe()
                            else:
                                st.error("No se pudo publicar el servicio (error interno).")

            else:
                st.info("Selecciona primero una categoría para ver los servicios disponibles.")

            st.markdown("---")
            if st.button("Editar perfil"):
                with st.form("edit_profile_form"):
                    nuevo_nombre = st.text_input("Nombre", user["nombre"])
                    nueva_bio = st.text_area("Bio", user["bio"] or "")
                    nueva_comuna = st.selectbox("Comuna", [""] + comunas_santiago, index=(comunas_santiago.index(user["comuna"]) + 1) if user.get("comuna") in comunas_santiago else 0)
                    if st.form_submit_button("Guardar cambios"):
                        db.update_user_profile(st.session_state.user_id, nuevo_nombre, nueva_bio, nueva_comuna)
                        st.success("Perfil actualizado")
                        rerun_safe()

# LOGIN / REGISTRO
elif st.session_state.page == "login" or st.session_state.page == "registro":
    if st.session_state.page == "login":
        st.markdown('<h1 class="conecta-title">🔐 Iniciar sesión</h1>', unsafe_allow_html=True)
        email = st.text_input("Correo electrónico", key="login_email")
        password = st.text_input("Contraseña", type="password", key="login_pwd")
        if st.button("Entrar"):
            user = auth.login_user(email.strip(), password)
            if user:
                login_set(user)
                st.success("Inicio de sesión correcto")
                set_page("inicio")
            else:
                st.error("Credenciales incorrectas")
    else:
        st.markdown('<h1 class="conecta-title">📝 Registrarse</h1>', unsafe_allow_html=True)
        nombre = st.text_input("Nombre completo", key="reg_nombre")
        email_r = st.text_input("Correo electrónico", key="reg_email")
        pwd_r = st.text_input("Contraseña", type="password", key="reg_pwd")
        bio_r = st.text_area("Descripción / Bio (opcional)", key="reg_bio")
        comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago, key="reg_comuna")
        if st.button("Registrarse"):
            new_id = auth.register_user(nombre.strip(), email_r.strip(), pwd_r, bio_r, comuna_r)
            if new_id:
                st.success("Cuenta creada. Puedes iniciar sesión.")
                set_page("login")
            else:
                st.error("No se pudo crear la cuenta (correo ya existe o faltan datos).")

# fallback
else:
    set_page("inicio")
