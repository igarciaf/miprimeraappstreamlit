import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi primer chat", page_icon="💬", layout="centered")

# --- ESTILOS ---
st.markdown("""
    <style>
    .chat-bubble {
        border-radius: 15px;
        padding: 10px 15px;
        margin-bottom: 8px;
        max-width: 80%;
        word-wrap: break-word;
    }
    .user-msg {
        background-color: #DCF8C6;
        align-self: flex-end;
    }
    .bot-msg {
        background-color: #EAEAEA;
        align-self: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 5px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- INICIALIZAR ESTADO ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "msg_input" not in st.session_state:
    st.session_state.msg_input = ""

# --- FUNCIÓN PARA AGREGAR MENSAJE ---
def enviar_mensaje():
    msg = st.session_state.msg_input.strip()
    if msg:
        # Agregamos el mensaje del usuario
        st.session_state.chat_history.append(("Tú", msg))

        # Simulamos respuesta del "bot"
        respuesta = f"Entiendo que dijiste: {msg}"
        st.session_state.chat_history.append(("Bot", respuesta))

    # Limpiamos campo de entrada de forma segura
    st.session_state.msg_input = ""

# --- MOSTRAR CHAT ---
st.title("💬 Chat de prueba")

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for sender, text in st.session_state.chat_history:
    clase = "user-msg" if sender == "Tú" else "bot-msg"
    st.markdown(f'<div class="chat-bubble {clase}"><b>{sender}:</b> {text}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- CAMPO DE ENTRADA ---
st.text_input("Escribe tu mensaje:", key="msg_input", on_change=enviar_mensaje)

# --- OPCIONAL: LIMPIAR CHAT ---
if st.button("🗑️ Limpiar chat"):
    st.session_state.chat_history = []
    st.session_state.msg_input = ""
