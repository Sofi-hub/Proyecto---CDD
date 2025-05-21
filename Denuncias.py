import streamlit as st
from functions import vista_autoridad

st.title("Ver denuncias")

if not st.session_state.get("logged_in", False):
    st.warning("Primero iniciá sesión en Inicio.")
elif st.session_state.usuario["tipo"] != "autoridad":
    st.error("Solo autoridades pueden ver esta página.")
else:
    vista_autoridad()
