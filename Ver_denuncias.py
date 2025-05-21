import streamlit as st
from functions import connect_to_supabase, execute_query

# Ensure the user is logged in
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("Por favor, inicia sesión para acceder a esta página.")
    st.stop()

# Display a welcome message
usuario = st.session_state.get("usuario", {})
st.title(f"Bienvenido, {usuario.get('nombre', 'Usuario')}")

# Connect to the Supabase database
conn = connect_to_supabase()
if not conn:
    st.error("No se pudo conectar a la base de datos.")
    st.stop()

# Query to fetch the current user's data
user_email = usuario.get("email")  # Assuming the email is stored in session state
if not user_email:
    st.error("No se encontró el correo electrónico del usuario en la sesión.")
    st.stop()

query = "SELECT * FROM Usuario WHERE email = %s"
try:
    # Execute the query
    result = execute_query(query, conn=conn, is_select=True, params=(user_email,))
    if result.empty:
        st.warning("No se encontraron datos para el usuario actual.")
    else:
        st.subheader("Tus datos:")
        st.dataframe(result)  # Display the data in a table format
except Exception as e:
    st.error(f"Error al obtener los datos del usuario: {e}")


user_id = usuario.get("id")  # Assuming the email is stored in session state
query = "SELECT * FROM denuncias WHERE id_usuario = %s"
try:
    # Execute the query
    result = execute_query(query, conn=conn, is_select=True, params=(user_id,))
    if result.empty:
        st.warning("No se encontraron datos para el usuario actual.")
    else:
        st.subheader("Tus datos:")
        st.dataframe(result)  # Display the data in a table format
except Exception as e:
    st.error(f"Error al obtener los datos del usuario: {e}")

