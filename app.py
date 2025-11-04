import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="Conecta", page_icon="🤝", layout="wide")

# --- ESTADO POR DEFECTO ---
if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"
if "categoria" not in st.session_state:
    st.session_state.categoria = None


# --- CSS (botones uniformes + footer fijo) ---
st.markdown(
    """
    <style>
    /* Botones grandes uniformes */
    div.stButton > button {
        height: 80px;
        width: 200px;
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        margin: 5px 10px;
    }
    div.stButton > button:hover {
        background-color: #45a049;
    }

    /* Footer fijo */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 70px;
        background-color: #ffffff;
        display: flex;
        justify-content: space-around;
        align-items: center;
        border-top: 1px solid rgba(0,0,0,0.08);
        z-index: 1000;
        box-shadow: 0 -2px 6px rgba(0,0,0,0.06);
    }
    .footer button {
        background: none;
        border: none;
        font-size: 28px;
        cursor: pointer;
    }
    .footer button:hover {
        transform: scale(1.1);
    }

    /* deja espacio inferior para que el contenido no quede tapado por el footer */
    .main > div {
        margin-bottom: 90px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- Helpers ---
def volver(pagina):
    """Botón volver estándar"""
    if st.button("⬅️ Volver"):
        st.session_state.pagina = pagina
        st.rerun()


def render_footer():
    """Footer fijo con botones de navegación internos"""
    footer_html = """
    <div class="footer" id="footer"></div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

    # Creamos columnas invisibles para ubicar los 3 botones
    cols = st.columns(3)
    with cols[0]:
        if st.button("💬", key="footer_chat"):
