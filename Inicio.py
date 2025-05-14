import streamlit as st

# --- Configuración de la página ---
st.set_page_config(
    page_title="Mi Reporte - Login",
    page_icon="📝",
    layout="centered"
)

st.title("Mi Reporte")

# --- Inicialización de estado ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_view" not in st.session_state:
    st.session_state.current_view = "login"

# --- Callbacks ---
def go_to_register():
    st.session_state.current_view = "register"

def go_to_login():
    st.session_state.current_view = "login"

def do_login(email, password):
    if email and password:
        st.session_state.logged_in = True
        st.session_state.username = email
    else:
        st.session_state.login_error = True

def do_register(new_email, new_username, new_password):
    if new_email and new_username and new_password:
        st.session_state.current_view = "login"
        st.session_state.registration_success = True
    else:
        st.session_state.register_error = True

# --- Vista: login ---
def login_view():
    st.subheader("Iniciar Sesión")

    email = st.text_input("Correo electrónico")
    password = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Ingresar"):
            do_login(email, password)

    with col2:
        st.button("Registrarse", on_click=go_to_register)

    if st.session_state.get("login_error"):
        st.error("Completá ambos campos.")
        st.session_state.login_error = False

# --- Vista: registro ---
def register_view():
    st.subheader("Crear Cuenta")

    new_email = st.text_input("Correo electrónico", key="new_email")
    new_username = st.text_input("Nombre de usuario", key="new_username")
    new_password = st.text_input("Contraseña", type="password", key="new_password")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("Crear cuenta"):
            do_register(new_email, new_username, new_password)
    with col2:
        st.button("Volver", on_click=go_to_login)

    if st.session_state.get("register_error"):
        st.error("Completá todos los campos.")
        st.session_state.register_error = False

# --- Vista: logged in ---
def logged_in_view():
    st.success(f"¡Bienvenido, {st.session_state.get('username')}!")
    st.info("Usá la barra lateral para navegar.")

    if st.button("Cerrar Sesión"):
        st.session_state.logged_in = False
        st.session_state.current_view = "login"
        del st.session_state["username"]

# --- Ruteo principal ---
if st.session_state.logged_in:
    logged_in_view()
elif st.session_state.current_view == "login":
    login_view()
elif st.session_state.current_view == "register":
    register_view()

# Mensaje de éxito al volver del registro
if st.session_state.get("registration_success"):
    st.success("Cuenta creada exitosamente. Iniciá sesión.")
    st.session_state.registration_success = False
