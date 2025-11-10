# app.py
import streamlit as st
from datetime import datetime
import db
import auth

# -------------------------
# Inicializar DB
# -------------------------
auth.init()

# -------------------------
# Configuración
# -------------------------
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# -------------------------
# Compatibilidad rerun
# -------------------------
def rerun_safe():
    """Usa st.rerun() si existe, de lo contrario st.experimental_rerun()."""
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# -------------------------
# Leer parámetros
# -------------------------
qp = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
if "page" in qp:
    st.session_state.page = qp["page"][0]

# -------------------------
# Estados
# -------------------------
defaults = {
    "page": "inicio",
    "user_id": 0,
    "user_name": "",
    "categoria": None,
    "servicio": None,
    "ubicacion": None,
    "perfil_usuario": None,
    "mensajes_chat": []
}
for k, v in defaults.items():
    st.session_state.setdefault(k, v)

# -------------------------
# Comunas
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
# Navegación
# -------------------------
def set_page(page_name: str):
    st.session_state.page = page_name
    if hasattr(st, "query_params"):
        st.query_params["page"] = page_name
    else:
        st.experimental_set_query_params(page=page_name)
    rerun_safe()

def require_login(shortcut_to="login"):
    st.warning("Debes iniciar sesión para ver esta sección.")
    if st.button("Ir a Iniciar sesión"):
        set_page(shortcut_to)

# -------------------------
# Topbar
# -------------------------
st.markdown("""
    <style>
    .top-bar {
        position: fixed; top: 0; left: 0; right: 0;
        height: 64px; background-color: #2E8B57; color: white;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; font-weight: 700; z-index: 9999;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    .top-bar a { color: white; text-decoration: none; padding: 8px 16px; }
    .inicio-btn {
        position: fixed; top: 12px; right: 18px;
        background-color: #2E8B57; color: white;
        padding: 8px 12px; border-radius: 10px;
        font-weight: 700; border: none; font-size: 14px;
        cursor: pointer; z-index: 99999; box-shadow: 0 2px 6px rgba(0,0,0,0.18);
    }
    .main > div { margin-top: 90px; margin-bottom: 40px; }
    </style>
    <div class="top-bar"><a href="?page=inicio">ConectaServicios</a></div>
    <form action="?page=inicio"><button class="inicio-btn" type="submit">🏠 Inicio</button></form>
""", unsafe_allow_html=True)

# -------------------------
# Sidebar
# -------------------------
pages_display = ["Inicio", "Iniciar sesión", "Registrarse", "Perfil", "Chats", "Notificaciones"]
pages_map = {p: p.lower().split()[0] for p in pages_display}

current_display = next((k for k, v in pages_map.items() if v == st.session_state.page), "Inicio")

with st.sidebar:
    st.markdown("### 🌐 Navegación")
    st.markdown(f"**{st.session_state.user_name or 'Invitado'}**")
    selection = st.radio("Ir a:", pages_display, index=pages_display.index(current_display))
    selected_page = pages_map.get(selection, "inicio")
    if selected_page != st.session_state.page:
        set_page(selected_page)
    st.markdown("---")
    if st.session_state.user_id and st.button("🚪 Cerrar sesión"):
        st.session_state.user_id = 0
        st.session_state.user_name = ""
        set_page("inicio")

# -------------------------
# Estilos
# -------------------------
st.markdown("""
    <style>
    div.stButton > button {
        height: 76px; width: 200px;
        background-color: #2E8B57; color: white;
        border-radius: 12px; font-size: 17px;
        margin: 6px 8px; border: none;
    }
    div.stButton > button:hover {
        background-color: #276e47; transform: translateY(-1px);
    }
    .conecta-title { text-align: center; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

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

# SUBCATEGORÍA
elif st.session_state.page == "subcategoria":
    st.markdown(f'<h1 class="conecta-title">Categoría: {st.session_state.categoria}</h1>', unsafe_allow_html=True)
    if st.button("⬅️ Volver al inicio"):
        set_page("inicio")
    opciones = {
        "Mascotas": ["Pasear perros", "Cuidar gatos", "Aseo de mascotas"],
        "Hogar": ["Limpieza general", "Cuidado de jardín", "Electricidad"],
        "Clases": ["Matemáticas", "Inglés", "Música"],
        "Niños": ["Cuidado por horas", "Apoyo escolar", "Acompañamiento"]
    }
    for item in opciones.get(st.session_state.categoria, []):
        if st.button(item):
            st.session_state.servicio = item
            set_page("ubicacion")

# UBICACIÓN
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
    resultados = [
        {"nombre": "Juan Pérez", "servicio": servicio, "valoracion": "⭐⭐⭐⭐☆"},
        {"nombre": "María Gómez", "servicio": servicio, "valoracion": "⭐⭐⭐⭐⭐"},
    ]
    for r in resultados:
        st.markdown(f"**{r['nombre']}** — {r['servicio']} — {r['valoracion']}")
        if st.button(f"Ver perfil de {r['nombre']}"):
            st.session_state.perfil_usuario = r
            set_page("perfil_publico")

# PERFIL PÚBLICO
elif st.session_state.page == "perfil_publico":
    r = st.session_state.get("perfil_usuario", {})
    st.markdown(f"<h1>👤 {r.get('nombre','Usuario')}</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Volver"):
        set_page("resultados")
    st.write(f"Servicio: {r.get('servicio','')}")
    st.write(f"Valoración: {r.get('valoracion','')}")

# PERFIL PROPIO
elif st.session_state.page == "perfil":
    st.markdown("<h1>👤 Mi perfil</h1>", unsafe_allow_html=True)
    if st.session_state.user_id == 0:
        require_login()
    else:
        st.write("Tu información se muestra aquí.")
