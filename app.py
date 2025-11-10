# app.py
import streamlit as st
from datetime import datetime
import db, auth

# -------------------------
# CONFIGURACIÓN INICIAL
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# Inicializa la base de datos (crea tablas si no existen)
auth.init()

# -------------------------
# ESTADOS POR DEFECTO / SESIÓN
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

# autenticación
if "user_id" not in st.session_state:
    st.session_state.user_id = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# chat
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# -------------------------
# LISTA DE COMUNAS DE SANTIAGO
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
# FUNCIONES AUX
# -------------------------
def set_page(pagina_name):
    st.session_state.pagina = pagina_name
    # sincronizamos query param para que enlaces HTML funcionen
    st.experimental_set_query_params(pagina=pagina_name)
    st.experimental_rerun()

def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)

def render_topbar():
    top_html = """
    <div style="position:fixed; top:0; left:0; right:0; height:64px; background-color:#2E8B57; display:flex; align-items:center; justify-content:center; z-index:9999; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
        <a href="?pagina=inicio" style="color:white; font-weight:700; font-size:22px; text-decoration:none; padding:8px 16px;">ConectaServicios</a>
    </div>
    """
    st.markdown(top_html, unsafe_allow_html=True)

# botón fijo "Inicio" arriba-derecha (form que apunta a ?pagina=inicio)
st.markdown(
    """
    <style>
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
        transition: background-color 0.12s ease;
        text-decoration: none;
    }
    .inicio-btn:hover { background-color: #276e47; }
    </style>
    <form action="?pagina=inicio">
        <button class="inicio-btn" type="submit">🏠 Inicio</button>
    </form>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Si el usuario no está logueado -> mostrar login/registro y detener
# -------------------------
if st.session_state.user_id == 0:
    st.sidebar.title("Conecta 🤝")
    st.sidebar.markdown("**Inicia sesión o regístrate**")

    tab_login, tab_register = st.tabs(["Iniciar sesión", "Registrarse"])

    with tab_login:
        with st.form("login_form", clear_on_submit=False):
            email_l = st.text_input("Correo electrónico")
            password_l = st.text_input("Contraseña", type="password")
            btn = st.form_submit_button("Iniciar sesión")
            if btn:
                user_id = auth.login_user(email_l.strip(), password_l)
                if user_id:
                    user = db.get_user_by_id(user_id)
                    st.session_state.user_id = user_id
                    st.session_state.user_name = user["nombre"]
                    st.success("Has iniciado sesión ✅")
                    st.experimental_rerun()
                else:
                    st.error("Correo o contraseña incorrectos.")

    with tab_register:
        with st.form("register_form", clear_on_submit=False):
            nombre = st.text_input("Nombre completo")
            email_r = st.text_input("Correo electrónico")
            password_r = st.text_input("Contraseña", type="password")
            comuna_r = st.selectbox("Comuna (opcional)", [""] + comunas_santiago)
            bio_r = st.text_area("Sobre ti (opcional)")
            btnr = st.form_submit_button("Crear cuenta")
            if btnr:
                new_id = auth.register_user(nombre.strip(), email_r.strip(), password_r, bio_r, comuna_r)
                if new_id:
                    st.success("Cuenta creada correctamente. Ahora inicia sesión.")
                else:
                    st.error("Ya existe un usuario con ese correo.")
    st.stop()

# -------------------------
# RENDER TOPBAR (solo después de auth)
# -------------------------
render_topbar()

# -------------------------
# BARRA LATERAL DE NAVEGACIÓN
# -------------------------
with st.sidebar:
    st.markdown(f"### Hola, {st.session_state.user_name}")
    if st.button("🏠 Inicio"):
        set_page("inicio")
    if st.button("💬 Chats"):
        set_page("chats")
    if st.button("🔔 Notificaciones"):
        set_page("notificaciones")
    if st.button("👤 Mi Perfil"):
        set_page("perfil_usuario")
    st.markdown("---")
    if st.button("🚪 Cerrar sesión"):
        st.session_state.user_id = 0
        st.session_state.user_name = ""
        st.experimental_rerun()

# -------------------------
# STYLES (mantengo lo que ya tenías)
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
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    .conecta-title { text-align:center; margin-bottom:8px; }
    .chat-bubble { padding:10px 12px; border-radius:12px; margin:6px 0; display:inline-block; max-width:70%; word-wrap:break-word; }
    .chat-right { background:#DCF8C6; text-align:right; float:right; clear:both; }
    .chat-left { background:#F1F0F0; text-align:left; float:left; clear:both; }
    .chat-time { font-size:10px; color:#666; margin-top:4px; display:block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# PANTALLAS
# -------------------------

# ---------- INICIO ----------
if st.session_state.pagina == "inicio":
    st.markdown('<h1 class="conecta-title">🤝 Conecta</h1>', unsafe_allow_html=True)
    st.write("Encuentra personas que ofrecen los servicios que necesitas.")
    if st.button("Acerca de"):
        st.info("Conecta es una plataforma para unir personas que ofrecen y buscan servicios cotidianos.")
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
    st.info("Usa la barra lateral para navegar entre las secciones.")

# ---------- CHATS ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.markdown("---")
    # Si más adelante usamos DB para mensajes, sustituir por db.get_messages_between(...)
    if st.session_state.mensajes_chat:
        for msg in st.session_state.mensajes_chat:
            clase = "chat-right" if msg.get("autor") == "Tú" else "chat-left"
            texto = msg.get("texto", "")
            hora = msg.get("hora", "")
            st.markdown(f'<div class="chat-bubble {clase}">{texto}<span class="chat-time">{hora}</span></div>', unsafe_allow_html=True)
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")
    # Entrada controlada: al presionar Enter enviamos (local temporal)
    mensaje = st.text_input("Escribe un mensaje y presiona Enter para enviar:", key="msg_input")
    if mensaje and mensaje.strip() != "":
        hora = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": mensaje.strip(), "hora": hora})
        st.session_state.msg_input = ""
        st.experimental_rerun()

# ---------- NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    notifs = db.get_notifications(st.session_state.user_id)
    if notifs:
        for n in notifs:
            # mostramos la fecha y el mensaje
            fecha = n.get("fecha", "")[:10]
            st.write(f"🔸 {n.get('mensaje','')} ({fecha})")
    else:
        st.info("No tienes notificaciones nuevas.")

# ---------- PERFIL PROPIO (desde sidebar) ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    user = db.get_user_by_id(st.session_state.user_id)
    if not user:
        st.warning("No se encontró tu usuario.")
    else:
        st.write(f"**Nombre:** {user['nombre']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Comuna:** {user['comuna'] or '-'}")
        st.write(f"**Bio:** {user['bio'] or '-'}")
        with st.form("editar_perfil"):
            nuevo_nombre = st.text_input("Editar nombre", user['nombre'])
            nueva_bio = st.text_area("Editar bio", user['bio'] or "")
            # selectbox index safe
            idx = 0
            if user.get("comuna") in comunas_santiago:
                idx = comunas_santiago.index(user.get("comuna")) + 1
            nueva_comuna = st.selectbox("Editar comuna", [""] + comunas_santiago, index=idx)
            if st.form_submit_button("Guardar cambios"):
                db.update_user_profile(st.session_state.user_id, nuevo_nombre, nueva_bio, nueva_comuna)
                st.success("Perfil actualizado correctamente")
                st.experimental_rerun()

# ---------- SUBCATEGORIAS ----------
elif st.session_state.pagina == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    volver("inicio")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas", "Adiestramiento"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Electricidad", "Pintura"],
        "Clases": ["Matemáticas", "Inglés", "Música", "Programación"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Acompañamiento"]
    }
    seleccion = st.selectbox("Selecciona el servicio:", ["-- Elige --"] + opciones.get(st.session_state.categoria, []))
    if seleccion != "-- Elige --":
        st.session_state.servicio = seleccion
        set_page("ubicacion")

# ---------- UBICACIÓN ----------
elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")
    ciudad = st.selectbox("Ciudad:", ["Santiago"])
    comuna = st.selectbox("Comuna:", comunas_santiago)
    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")

# ---------- RESULTADOS ----------
elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio} — {st.session_state.ubicacion}</h1>', unsafe_allow_html=True)
    volver("ubicacion")
    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9734;"},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9733;"}
    ]
    for r in resultados:
        st.markdown(f'{r["nombre"]} — {r["servicio"]} — <span>{r["valoracion"]}</span>', unsafe_allow_html=True)
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")

# ---------- PERFIL (otro usuario mostrado desde resultados) ----------
elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario", "edad": "-", "servicio": "-", "valoracion": "—"}
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write(f"**Servicio:** {r.get('servicio','-')}")
    st.write(f"**Valoración:** {r.get('valoracion','-')}")
    st.write("**Descripción:** Persona confiable, con experiencia en el servicio (simulación).")
    st.subheader("💬 Chat")
    mensaje = st.text_input("Escribe un mensaje...", key="profile_msg")
    if st.button("Enviar mensaje (perfil)"):
        if mensaje.strip():
            # en el futuro guardar en DB y notificar
            st.success("Mensaje enviado correctamente ✅")
        else:
            st.warning("No puedes enviar un mensaje vacío.")
