import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] == False

if st.session_state['logged_in']:
    st.text('Hola')