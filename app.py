import streamlit as st

# Título de la app
st.title("¡Mi primera app!")

# Texto simple
st.write("Hola, soy Ignacio y esta es mi primera aplicación con Streamlit.")

# Un input interactivo
nombre = st.text_input("¿Cómo te llamas?")
edad = st.number_input("¿Cuántos años tienes?", min_value=0, max_value=120)
opcion = st.selectbox("Elige una opción", ["Hombre", "Mujer", "Prefiero no decirlo"])

# Respuesta condicional
if nombre:
    st.write(f"¡Hola, {nombre}! Bienvenido/a a mi app")

# Un botón
# Botón de registro
if st.button("Presiona aquí"):
    if not nombre.strip():  # Si no se ingresó nombre
        st.error("No puedes registrarte sin ingresar tu nombre.")
    else:
        st.balloons()  # Animación de globos
        st.success("¡Registrado correctamente!")

