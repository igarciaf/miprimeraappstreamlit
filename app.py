# app.py
import streamlit as st
from datetime import datetime

# -------------------------
# CONFIGURACIÓN DE PÁGINA
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Si la URL trae ?pagina=... la respetamos
# -------------------------
query_params = st.experimental_get_query_params()
if "pagina" in query_params:
    st.session_state.pagina = query_params["pagina"][0]

# -------------------------
# ESTADOS POR DEFECTO (seguros)
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

# historial de mensajes (lista de dicts: {"autor": "...", "texto": "...", "hora": "HH:MM"})
if "mensajes_chat" not in st.session_state:
    st.session_state.mensajes_chat = []

# campo controlado para el input del chat
if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# -------------------------
# CSS (hover más oscuro, footer fijo por HTML, estilos chat)
# -------------------------
st.markdown(
    """
    <style>
    /* botones uniformes */
    div.stButton > button {
        height: 76px;
        width: 200px;
        background-color: #2E8B57;
        color: white;
        border-radius: 12px;
        font-size: 17px;
        margin: 6px 8px;
        border: none;
        transition: background-color 0.15s ease, transform 0.12s ease;
    }
    div.stButton > button:hover {
        background-color: #276e47; /* un verde más oscuro para mejor contraste */
        transform: translateY(-1px);
    }

    /* top bar fija */
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
    .top-bar a:hover { opacity: 0.95; cursor: pointer; }

    /* footer fijo (HTML) */
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
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .conecta-footer a div { font-size:11px; margin-top:4px; }
    .conecta-footer a:hover { background-color: rgba(0,0,0,0.03); cursor: pointer; }

    /* espacio para que el contenido no quede oculto */
    .main > div {
        margin-top: 90px;
        margin-bottom: 100px;
    }
    .conecta-title { text-align: center; margin-bottom: 8px; }

    /* chat bubbles */
    .chat-bubble { padding: 10px 12px; border-radius: 12px; margin: 6px 0; display: inline-block; max-width: 70%; word-wrap: break-word; }
    .chat-right { background: #DCF8C6; text-align: right; float: right; clear: both; }
    .chat-left { background: #F1F0F0; text-align: left; float: left; clear: both; }
    .chat-time { font-size: 10px; color: #666; margin-top: 4px; display:block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# FUNCIONES DE NAVEGACIÓN (seguras)
# -------------------------
def set_page(pagina_name):
    """
    Actualiza el estado y la URL (query param).
    No usamos experimental_rerun para evitar errores en entornos donde no esté disponible.
    El comportamiento de navegación funciona porque al inicio leemos query_params.
    """
    st.session_state.pagina = pagina_name
    st.experimental_set_query_params(pagina=pagina_name)

def volver(pagina_destino="inicio"):
    if st.button("⬅️ Volver"):
        set_page(pagina_destino)

def render_topbar():
    top_html = """
    <div class="top-bar">
        <a href="?pagina=inicio">ConectaServicios</a>
        <a class="top-btn" style="position:absolute; right:16px; top:14px; background:rgba(255,255,255,0.12); color:white; border:1px solid rgba(255,255,255,0.18); padding:6px 12px; border-radius:8px; font-size:14px; text-decoration:none;" href="?pagina=inicio">Inicio</a>
    </div>
    """
    st.markdown(top_html, unsafe_allow_html=True)

def render_footer_html():
    # Footer como HTML con enlaces que cambian ?pagina=... en la misma ventana (no abre pestañas)
    footer_html = """
    <div class="conecta-footer">
        <a href="?pagina=chats" title="Chats">💬<div>Chats</div></a>
        <a href="?pagina=notificaciones" title="Notificaciones">🔔<div>Notifs</div></a>
        <a href="?pagina=perfil_usuario" title="Mi perfil">👤<div>Perfil</div></a>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# -------------------------
# FUNCION PARA ENVIAR MENSAJE (callback para text_input)
# -------------------------
def send_chat_message():
    texto = st.session_state.get("msg_input", "").strip()
    if texto:
        hora = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Tú", "texto": texto, "hora": hora})
        # respuesta automática de prueba (opcional)
        hora2 = datetime.now().strftime("%H:%M")
        st.session_state.mensajes_chat.append({"autor": "Otro", "texto": "Gracias, te respondo pronto 👍", "hora": hora2})
    # limpiar el campo desde el callback (seguro)
    st.session_state.msg_input = ""

# -------------------------
# RENDER TOPBAR
# -------------------------
render_topbar()

# -------------------------
# PANTALLAS (igual que tu estructura original)
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
    render_footer_html()

# ---------- CHATS ----------
elif st.session_state.pagina == "chats":
    st.markdown('<h1 class="conecta-title">💬 Chats</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.markdown("---")

    # Mostrar mensajes previos (si existen)
    if st.session_state.mensajes_chat:
        for msg in st.session_state.mensajes_chat:
            clase = "chat-right" if msg.get("autor") == "Tú" else "chat-left"
            texto = msg.get("texto", "")
            hora = msg.get("hora", "")
            st.markdown(
                f'<div class="chat-bubble {clase}">{texto}<span class="chat-time">{hora}</span></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No hay mensajes todavía. Escribe algo para comenzar la conversación 👇")

    # Campo controlado: al presionar Enter se ejecuta send_chat_message
    st.text_input(
        "Escribe un mensaje y presiona Enter para enviar:",
        key="msg_input",
        on_change=send_chat_message
    )

    render_footer_html()

# ---------- NOTIFICACIONES ----------
elif st.session_state.pagina == "notificaciones":
    st.markdown('<h1 class="conecta-title">🔔 Notificaciones</h1>', unsafe_allow_html=True)
    volver("inicio")
    # por ahora mostramos estático, luego podemos enlazar a st.session_state.notificaciones
    st.write("✅ Tu perfil fue visitado por @usuario123")
    st.write("💬 Tienes una nueva reseña en tu último trabajo")
    # uso de entidades HTML para evitar caracteres especiales en el código fuente
    st.markdown("⭐ Valoración promedio: &#9733;&#9733;&#9733;&#9733;&#9734; (4.0)", unsafe_allow_html=True)
    render_footer_html()

# ---------- PERFIL (otros perfiles & propio) ----------
elif st.session_state.pagina == "perfil":
    r = st.session_state.perfil_usuario or {"nombre": "Usuario"}
    # aquí también uso entidades para mostrar estrellas sin insertar caracteres especiales fuera de strings
    st.markdown(f'<h1 class="conecta-title">👤 Perfil de {r["nombre"]}</h1>', unsafe_allow_html=True)
    volver("resultados")
    st.write("**Descripción:** Persona confiable (simulación).")
    st.markdown("**Valoraciones:** &#9733;&#9733;&#9733;&#9733;&#9734; (4.0)", unsafe_allow_html=True)
    # chat dentro de perfil (opcional)
    mensaje_key = f"msg_profile_{r.get('nombre','')}"
    st.text_input("💬 Envía un mensaje:", key=mensaje_key, on_change=lambda: None)
    render_footer_html()

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
    render_footer_html()

# ---------- UBICACIÓN (aquí agregué TODAS las comunas de Santiago) ----------
elif st.session_state.pagina == "ubicacion":
    st.markdown('<h1 class="conecta-title">📍 Selecciona tu ubicación</h1>', unsafe_allow_html=True)
    volver("subcategoria")

    ciudad = st.selectbox("Ciudad:", ["Santiago"])

    # --- lista completa de comunas de la Región Metropolitana (Santiago) ---
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

    comuna = st.selectbox("Comuna:", comunas_santiago)

    if st.button("Buscar resultados"):
        st.session_state.ubicacion = f"{comuna}, {ciudad}"
        set_page("resultados")
    render_footer_html()

# ---------- RESULTADOS ----------
elif st.session_state.pagina == "resultados":
    st.markdown(f'<h1 class="conecta-title">Resultados: {st.session_state.servicio} — {st.session_state.ubicacion}</h1>', unsafe_allow_html=True)
    volver("ubicacion")
    resultados = [
        {"nombre": "Juan Pérez", "servicio": st.session_state.servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9734;"},
        {"nombre": "María Gómez", "servicio": st.session_state.servicio, "valoracion": "&#9733;&#9733;&#9733;&#9733;&#9733;"}
    ]
    for r in resultados:
        # mostramos valoración usando safe HTML
        st.markdown(f'{r["nombre"]} — {r["servicio"]} — <span>{r["valoracion"]}</span>', unsafe_allow_html=True)
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil")
    render_footer_html()

# ---------- PERFIL PROPIO (desde footer) ----------
elif st.session_state.pagina == "perfil_usuario":
    st.markdown('<h1 class="conecta-title">👤 Mi Perfil</h1>', unsafe_allow_html=True)
    volver("inicio")
    st.write("**Nombre:** Ignacio")
    st.write("**Edad:**  XX")
    st.write("**Servicios ofrecidos:** Paseo de perros, Cuidado por horas (ejemplo)")
    st.markdown("**Valoración promedio:** &#9733;&#9733;&#9733;&#9733;&#9734; (4.0)", unsafe_allow_html=True)
    render_footer_html()
