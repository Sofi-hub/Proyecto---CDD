# shared.py
import psycopg2
import streamlit as st
from datetime import datetime
from uuid import uuid4
import os

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_HOST = "aws-0-us-east-1.pooler.supabase.com"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres.uedenhmdzpfseazxziyn"
DB_PASSWORD = "HZe2$Ets+_ViteG"

def get_connection():
    if "db_conn" in st.session_state:
        try:
            st.session_state.db_conn.cursor()
            return st.session_state.db_conn
        except psycopg2.InterfaceError:
            del st.session_state.db_conn

    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    st.session_state.db_conn = conn
    return conn

def registrar_usuario(nombre, email, contraseña):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Usuario WHERE email = %s", (email,))
    if cur.fetchone():
        cur.close()
        return False, "Ya existe un usuario con ese email."

    cur.execute("""
        INSERT INTO Usuario (nombre, email, contraseña, tipo_usuario)
        VALUES (%s, %s, %s, 'vecino')
    """, (nombre, email, contraseña))
    conn.commit()
    cur.close()
    return True, "Usuario registrado correctamente."

def verificar_usuario(email, contraseña):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nombre, tipo_usuario FROM Usuario WHERE email = %s AND contraseña = %s", (email, contraseña))
        resultado = cur.fetchone()
        cur.close()
        return resultado
    except Exception as e:
        st.error(f"Error al verificar usuario: {e}")
        return None
