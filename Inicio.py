import streamlit as st
import psycopg2

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_HOST="aws-0-us-east-1.pooler.supabase.com"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="postgres.uedenhmdzpfseazxziyn"
DB_PASSWORD="HZe2$Ets+_ViteG"

# --- CONEXIÓN ---
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

# --- VERIFICAR USUARIO ---
def verificar_usuario(email, contraseña):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, nombre, tipo_usuario FROM Usuario WHERE email = %s AND contraseña = %s", (email, contraseña))
    resultado = cur.fetchone()
    cur.close()
    return resultado

# --- REGISTRAR USUARIO ---
def registrar_usuario(nombre, email, contraseña):
    conn = get_connection()
    cur = conn.cursor()

    # Verificar que el email no exista
    cur.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
    if cur.fetchone():
        return False, "Ya existe un usuario con ese email."

    # Insertar nuevo usuario como 'vecino'
    cur.execute("INSERT INTO Usuario (nombre, email, contraseña, tipo_usuario) VALUES (%s, %s, %s, 'vecino')", (nombre, email, contraseña))
    conn.commit()
    cur.close()
    return True, "Usuario registrado correctamente."

# --- ESTADO INICIAL ---
st.set_page_config(page_title="Mi Reporte", layout="centered")
st.title("Mi Reporte")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_view" not in st.session_state:
    st.session_state.current_view = "login"

# --- CALLBACKS ---
def go_to_register():
    st.session_state.current_view = "register"

def go_to_login():
    st.session_state.current_view = "login"

# --- VISTA: LOGIN ---
def login_view():
    st.subheader("Iniciar Sesión")

    email = st.text_input("Correo electrónico", key="login_email")
    password = st.text_input("Contraseña", type="password", key="login_password")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Ingresar"):
            usuario = verificar_usuario(email, password)
            if usuario:
                st.session_state.logged_in = True
                st.session_state.usuario = {
                    "id": usuario[0],
                    "nombre": usuario[1],
                    "tipo": usuario[2],
                    "email": email
                }
            else:
                st.error("Email o contraseña incorrectos.")
    with col2:
        st.button("Registrarse", on_click=go_to_register)

# --- VISTA: REGISTRO ---
def register_view():
    st.subheader("Registrarse")

    nombre = st.text_input("Nombre completo", key="reg_nombre")
    email = st.text_input("Correo electrónico", key="reg_email")
    password = st.text_input("Contraseña", type="password", key="reg_password")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Crear cuenta"):
            if nombre and email and password:
                exito, mensaje = registrar_usuario(nombre, email, password)
                if exito:
                    st.success(mensaje)
                    go_to_login()
                else:
                    st.error(mensaje)
            else:
                st.error("Completá todos los campos.")
    with col2:
        st.button("Volver", on_click=go_to_login)

# --- VISTA: USUARIO LOGUEADO ---
def logged_in_view():
    usuario = st.session_state.usuario
    st.success(f"¡Bienvenido {usuario['nombre']}! (tipo: {usuario['tipo']})")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        del st.session_state.usuario
        st.session_state.current_view = "login"

# --- RUTEO ---
if st.session_state.logged_in:
    logged_in_view()
elif st.session_state.current_view == "login":
    login_view()
elif st.session_state.current_view == "register":
    register_view()
