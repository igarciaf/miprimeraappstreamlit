# app.py
import streamlit as st
import db
import auth

# Inicializar DB directamente (así no dependemos de auth.init())
db.init_db()

st.set_page_config(page_title="ConectaApp", page_icon="🤝", layout="wide")

# estados iniciales
if "page" not in st.session_state:
    st.session_state.page = "Inicio"
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "selected_user_id" not in st.session_state:
    st.session_state.selected_user_id = None

def go_to(page):
    st.session_state.page = page

# Sidebar
with st.sidebar:
    st.title("ConectaApp")
    if st.session_state.user_id:
        user = db.get_user_by_id(st.session_state.user_id)
        st.subheader(f"👋 Hola, {user['nombre']}")
        if st.button("Inicio"):
            go_to("Inicio")
        if st.button("Perfil"):
            go_to("Perfil")
        if st.button("Chat"):
            go_to("Chat")
        if st.button("Notificaciones"):
            go_to("Notificaciones")
        if st.button("Agregar servicio"):
            go_to("Agregar servicio")
        if st.button("Cerrar sesión"):
            st.session_state.user_id = None
            go_to("Inicio")
    else:
        if st.button("Iniciar sesión"):
            go_to("Iniciar sesión")
        if st.button("Registrarse"):
            go_to("Registrarse")

# Páginas
if st.session_state.page == "Inicio":
    st.title("🔎 Busca servicios o ayuda en tu zona")
    search = st.text_input("¿Qué servicio necesitas?")
    if st.button("Buscar"):
        if search.strip():
            resultados = db.search_users_by_service(search)
            if resultados:
                st.success(f"Usuarios que ofrecen '{search}':")
                for r in resultados:
                    st.write(f"👤 {r['nombre']} — 📍 {r['comuna']} — 💬 {r['servicios'] or ''}")
                    if st.button(f"Chatear con {r['nombre']}", key=f"chat_{r['id']}"):
                        st.session_state.selected_user_id = r["id"]
                        go_to("Chat")
            else:
                st.warning("No se encontraron resultados.")
        else:
            st.warning("Por favor escribe algo para buscar.")

elif st.session_state.page == "Registrarse":
    st.header("📝 Crear cuenta")
    nombre = st.text_input("Nombre completo")
    email = st.text_input("Correo electrónico")
    comuna = st.text_input("Comuna")
    servicios = st.text_input("Servicios que puedes ofrecer (separados por comas)")
    bio = st.text_area("Cuéntanos un poco sobre ti")
    password = st.text_input("Contraseña", type="password")

    if st.button("Registrarme"):
        user_id = auth.register_user(nombre, email, password, bio, comuna, servicios)
        if user_id:
            st.success("Usuario registrado con éxito. Ahora puedes iniciar sesión.")
            go_to("Iniciar sesión")
        else:
            st.error("El correo ya está en uso o faltan datos.")

elif st.session_state.page == "Iniciar sesión":
    st.header("🔐 Iniciar sesión")
    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        user_id = auth.login_user(email, password)
        if user_id:
            st.session_state.user_id = user_id
            st.success("Inicio de sesión correcto")
            go_to("Inicio")
        else:
            st.error("Credenciales incorrectas.")

elif st.session_state.page == "Perfil":
    if not st.session_state.user_id:
        st.warning("Inicia sesión para ver tu perfil.")
    else:
        user = db.get_user_by_id(st.session_state.user_id)
        st.header(f"👤 Perfil de {user['nombre']}")
        st.write(f"📧 {user['email']}")
        st.write(f"📍 {user['comuna']}")
        st.write(f"🛠️ Servicios: {user['servicios'] or 'No especificado'}")
        st.write(f"💬 Bio: {user['bio'] or 'Sin descripción'}")

elif st.session_state.page == "Agregar servicio":
    if not st.session_state.user_id:
        st.warning("Inicia sesión para agregar servicios.")
    else:
        user = db.get_user_by_id(st.session_state.user_id)
        st.header("🛠️ Agregar o modificar servicios que ofreces")
        servicios_actuales = user["servicios"] or ""
        nuevos_servicios = st.text_input("Lista de servicios (separados por comas):", value=servicios_actuales)
        if st.button("Guardar cambios"):
            db.update_user_profile(user["id"], servicios=nuevos_servicios)
            st.success("Servicios actualizados con éxito.")
            go_to("Perfil")

elif st.session_state.page == "Chat":
    st.header("💬 Chat")
    if not st.session_state.user_id:
        st.warning("Inicia sesión para usar el chat.")
    else:
        if st.session_state.selected_user_id:
            receiver = db.get_user_by_id(st.session_state.selected_user_id)
            st.subheader(f"Chat con {receiver['nombre']}")
            msgs = db.get_messages_between(st.session_state.user_id, st.session_state.selected_user_id)
            for m in msgs:
                who = "Tú" if m["emisor_id"] == st.session_state.user_id else receiver["nombre"]
                st.write(f"**{who}:** {m['contenido']}")
            new_msg = st.text_input("Escribe tu mensaje", key="chat_new")
            if st.button("Enviar"):
                if new_msg.strip():
                    db.add_message(st.session_state.user_id, st.session_state.selected_user_id, new_msg.strip())
                    db.add_notification(st.session_state.selected_user_id, "mensaje", f"Nuevo mensaje de {db.get_user_by_id(st.session_state.user_id)['nombre']}")
                    st.success("Mensaje enviado")
                    # refrescar
                    go_to("Chat")
                else:
                    st.warning("Escribe algo antes de enviar.")
        else:
            st.info("Selecciona un usuario desde Inicio para chatear o ve a la sección 'Chats' (más adelante añadiremos lista).")

elif st.session_state.page == "Notificaciones":
    st.header("🔔 Notificaciones")
    if not st.session_state.user_id:
        st.warning("Inicia sesión para ver notificaciones.")
    else:
        nots = db.get_notifications(st.session_state.user_id)
        if nots:
            for n in nots:
                estado = "Leído" if n.get("leido") else "Nuevo"
                st.write(f"- {n.get('mensaje')} ({n.get('fecha')}) — {estado}")
                if not n.get("leido"):
                    if st.button(f"Marcar leído {n['id']}"):
                        db.mark_notification_read(n['id'])
                        go_to("Notificaciones")
        else:
            st.info("No tienes notificaciones.")

else:
    go_to("Inicio")
