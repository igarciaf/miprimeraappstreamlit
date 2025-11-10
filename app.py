# app.py
import streamlit as st
from datetime import datetime
import db
import auth

# -------------------------
# Inicializar DB (auth.init llama a db.init_db)
# -------------------------
auth.init()

# -------------------------
# Configuración página
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Leer query params para soportar el botón superior que apunta a ?page=inicio
# -------------------------
qp = st.experimental_get_query_params()
if "page" in qp:
    st.session_state.page = qp["page"][0]

# -------------------------
# Estados por defecto
# -------------------------
if "page" not in st.session_state:
    st.session_state.page = "inicio"
if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "servicio" not in st.session_state:
    st.session_state.servicio = None
if "ubicacion" not in st.session_state:
    st.session_state.ubicacion = None
if "perfil_usuario" not in st.session_state:
    st.session_state.perfil_usuario = None

# chat temp state (keeps showing messages in UI; DB-backed chat implemented later)
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []

# -------------------------
# Lista comunas (completa)
# -------------------------
comunas_santiago = [
    "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", "Huechuraba",
    "Independencia", "La Cisterna", "La Florida", "La Granja", "La Pintana", "La Reina",
    "Las Condes", "Lo Barnechea", "Lo Espejo", "Lo Prado", "Macul", "Maipú",
    "Ñuñoa", "Pedro Aguirre Cerda", "Peñalolén", "Providencia", "Pudahuel", "Quilicura",
    "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", "San Ramón",
    "Santiago", "Vitacura", "Puente Alto", "Pirque", "San José de Maipo",
    "Colina", "Lampa", "Tiltil", "San Bernardo", "Buin", "Calera de Tango", "Paine",
    "Melipilla", "María Pinto", "Curacaví", "Talagante", "El Monte", "Padre Hurtado", "Peñaflor"
]

# -------------------------
# Helpers de navegación
# -------------------------
def set_page(page_name: str):
    st.session_state.page = page_name
    # sincronizamos query param para que top button funcione coherente
    st.experimental_set_query_params(page=page_name)
    st.experimental_rerun()

def require_login(shortcut_to="login"):
    st.warning("Debes iniciar sesión para ver esta sección.")
    if st.button("Ir a Iniciar sesión"):
        set_page(shortcut_to)

# -------------------------
# Topbar + botón Inicio fijo arriba (usa query param ?page=inicio)
# -------------------------
st.markdown(
    """
    <style>
    .top-bar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 64px;
        background-color: #2E8B57;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px;
        font-weight: 700;
        z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .top-bar a { color: white; text-decoration: none; padding: 8px 16px; }
    .inicio-btn {
        position: fixed;
        top: 12px;
        right: 18px;
        background-color: #2E8B57;
        color: white;
        padding: 8px 12px;
        border-radius: 10px;
        font-weight: 700;
        border: none;
        font-size: 14px;
        cursor: pointer;
        z-index: 99999;
        box-shadow: 0 2px 6px rgba(0,0,0,0.18);
        text-decoration: none;
    }
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    </style>
    <div class="top-bar"><a href="?page=inicio">ConectaServicios</a></div>
    <form action="?page=inicio"><button class="inicio-btn" type="submit">🏠 Inicio</button></form>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Sidebar (navegación)
# -------------------------
pages_display = ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Chats", "Notificaciones"]
pages_map = {
    "Inicio": "inicio",
    "Iniciar sesión": "login",
    "Registrarse": "registro",
    "Perfil": "perfil",
    "Chats": "chats",
    "Notificaciones": "notificaciones"
}

# determinar display actual de forma segura
current_display = "Inicio"
for k, v in pages_map.items():
    if v == st.session_state.page:
        current_display = k
        break

with st.sidebar:
    st.markdown("### 🌐 Navegación")
    if st.session_state.user_id:
        u = db.get_user_by_id(st.session_state.user_id)
        st.markdown(f"**{u.get('nombre','Usuario')}**")
    else:
        st.markdown("**Invitado**")

    selection = st.radio("Ir a:", pages_display, index=pages_display.index(current_display))
    selected_page = pages_map.get(selection, "inicio")
    if selected_page != st.session_state.page:
        set_page(selected_page)

    st.markdown("---")
    if st.session_state.user_id:
        if st.button("🚪 Cerrar sesión"):
            st.session_state.user_id = 0
            st.session_state.user_name = ""
            st.success("Sesión cerrada")
            set_page("inicio")

# -------------------------
# Styles (botones grandes como antes)
# -------------------------
st.markdown(
    """
    <style>
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
        background-color: #276e47;
        transform: translateY(-1px);
    }
    .conecta-title { text-align: center; margin-bottom: 8px; }
    .chat-bubble { padding: 10px 12px; border-radius: 12px; margin: 6px 0; display: inline-block; max-width: 70%; word-wrap: break-word; }
    .chat-right { background: #DCF8C6; text-align: right; float: right; clear: both; }
    .chat-left { background: #F1F0F0; text-align: left; float: left; clear: both; }
    .chat-time { font-size: 10px; color: #666; margin-top: 4px; display:block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# PÁGINAS
# -------------------------

# ---------- INICIO (mantener exactamente los botones grandes) ----------
if st.session_state.page == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")

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
    st.info("Usa la barra lateral para navegar (Perfil, Chats, Notificaciones).")

# ---------- LOGIN ----------
elif st.session_state.page == "login":
    st.markdown('<h1 class="conecta-title">🔐 Iniciar sesión</h1>', unsafe_allow_html=True)
    with st.form("login_form"):
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        if st.form_submit_button("Entrar"):
            user_id = auth.login_user(email.strip(), password)
            if user_id:
                user = db.get_user_by_id(user_id)
                st.session_state.user_id = user_id
                st.session_state.user_name = user.get("nombre", "")
                st.success("Has iniciado sesión ✅")
                set_page("inicio")
            else:
                st.error("Correo o contraseña incorrectos.")

# ---------- REGISTRO ----------
elif st.session_state.page == "registro":
    st.markdown('<h1 class="conecta-title">📝 Registrarse</h1>', unsafe_allow_html=True)
    with st.form("register_form"):
        nombre = st.text_input("Nombre completo")
        email_r = st.text_input("Correo electrónico")
        password_r = st.text_input("Contraseña", type="password")
        comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago)
        bio_r = st.text_area("Sobre ti (opcional)")
        if st.form_submit_button("Crear cuenta"):
            if not nombre.strip() or not email_r.strip() or not password_r:
                st.warning("Completa los campos obligatorios (nombre, email, contraseña).")
            else:
                new_id = auth.register_user(nombre.strip(), email_r.strip(), password_r, bio_r, comuna_r)
                if new_id:
                    st.success("Cuenta creada correctamente. Ahora puedes iniciar sesión.")
                    set_page("login")
                else:
                    st.error("Ya existe un usuario con ese correo.")

# ---------- SUBCATEGORIA ----------
elif st.session_state.page == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("inicio")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento", "Cuidado nocturno"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Arreglo básico", "Electricidad", "Pintura", "Gasfitería"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Computación", "Arte", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Actividades recreativas", "Acompañamiento", "Transporte escolar"]
    }
    lista = opciones.get(st.session_state.categoria, [])
    for item in lista:
        if st.button(item):
            st.session_state.servicio = item
            set_page("ubicacion")

# ---------- UBICACION ----------
elif st.session_state.page == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", comunas_santiago)
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")

# ---------- RESULTADOS ----------
elif st.session_state.page == "resultados":
    servicio = st.session_state.get("servicio", "Servicio")
    ubic = st.session_state.get("ubicacion", "Ubicación")
    st.markdown(f'<h1 class="conecta-title">Resultados: {servicio} — {ubic}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("ubicacion")
    # resultados simulados
    resultados = [
        {"nombre": "Juan Pérez", "servicio": servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9734;", "edad": 28, "comunas": ["Providencia","Ñuñoa"]},
        {"nombre": "María Gómez", "servicio": servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9733;", "edad": 32, "comunas": ["Las Condes","Providencia"]},
        {"nombre": "Pedro Ramírez", "servicio": servicio, "valoracion": "&#9733;&#9733;&#9733;&#9734;&#9734;", "edad": 24, "comunas": ["Maipú","Santiago"]},
    ]
    comuna_actual = st.session_state.get("ubicacion", "").split(",")[0]
    mostrados = [r for r in resultados if comuna_actual in r.get("comunas", [])]
    if not mostrados:
        mostrados = resultados
    for r in mostrados:
        st.markdown(f"**{r['nombre']}** — {r['servicio']} — <span>{r['valoracion']}</span> — {r['edad']} años", unsafe_allow_html=True)
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil_publico")

# ---------- PERFIL PÚBLICO ----------
elif st.session_state.page == "perfil_publico":
    r = st.session_state.get("perfil_usuario", {"nombre": "Usuario", "edad": "-", "servicio": "-", "valoracion": "—"})
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("resultados")
    st.write(f"**Servicio:** {r.get('servicio','-')}")
    st.write(f"**Valoración:** {r.get('valoracion','-')}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio (simulación).")
    st.subheader("💬 Chat")
    mensaje = st.text_input("Escribe un mensaje...", key="profile_msg")
    if st.button("Enviar mensaje (perfil)"):
        if mensaje.strip():
            st.success("Mensaje enviado correctamente ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")

# ---------- CHATS ----------
elif st.session_state.page == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    if st.session_state.user_id == 0:
        require_login("login")
    else:
        # usuarios disponibles para chatear (DB)
        conn = db.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre FROM users WHERE id != ?", (st.session_state.user_id,))
        rows = cur.fetchall()
        conn.close()
        others = [dict(r) for r in rows]
        if not others:
            st.info("No hay otros usuarios registrados aún.")
        else:
            names = [o["nombre"] for o in others]
            selected = st.selectbox("Selecciona un usuario", names)
            receptor = next(o for o in others if o["nombre"] == selected)
            receptor_id = receptor["id"]
            st.subheader(f"Chat con {selected}")

            mensajes = db.get_messages_between(st.session_state.user_id, receptor_id)
            if mensajes:
                for m in mensajes:
                    autor = "Tú" if m["emisor_id"] == st.session_state.user_id else selected
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
                        st.experimental_rerun()
                    else:
                        st.warning("Escribe un mensaje antes de enviar.")

# ---------- NOTIFICACIONES ----------
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
                        st.experimental_rerun()
        else:
            st.info("No tienes notificaciones nuevas.")

# ---------- PERFIL (propio) ----------
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

            with st.form("edit_profile"):
                nuevo_nombre = st.text_input("Editar nombre", user['nombre'])
                nueva_bio = st.text_area("Editar bio", user['bio'] or "")
                idx = 0
                if user.get("comuna") in comunas_santiago:
                    idx = comunas_santiago.index(user.get("comuna")) + 1
                nueva_comuna = st.selectbox("Editar comuna", [""] + comunas_santiago, index=idx)
                if st.form_submit_button("Guardar cambios"):
                    db.update_user_profile(st.session_state.user_id, nuevo_nombre, nueva_bio, nueva_comuna)
                    st.success("Perfil actualizado correctamente")
                    st.experimental_rerun()

# fallback
else:
    set_page("inicio")
    st.experimental_rerun()
