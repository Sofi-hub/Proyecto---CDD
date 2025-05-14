import streamlit as st
from shared import get_connection, verificar_usuario, registrar_usuario
import pandas as pd
from datetime import datetime
from uuid import uuid4
import os

st.set_page_config(page_title="Mi Reporte", layout="centered")
st.title("Mi Reporte")

# --- Estado inicial ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_view" not in st.session_state:
    st.session_state.current_view = "login"

# --- FUNCIONES DE INTERFAZ ---
def menu_vecino():
    opciones = ["Publicar denuncia", "Mi cuenta"]
    seleccion = st.sidebar.radio("Menú", opciones)

    if seleccion == "Publicar denuncia":
        vista_vecino()
    elif seleccion == "Mi cuenta":
        st.subheader("Mi cuenta")
        st.info(f"Usuario: {st.session_state.usuario['nombre']}")

def menu_autoridad():
    opciones = ["Ver denuncias", "Mi cuenta"]
    seleccion = st.sidebar.radio("Menú", opciones)

    if seleccion == "Ver denuncias":
        vista_autoridad()
    elif seleccion == "Mi cuenta":
        st.subheader("Mi cuenta")
        st.info(f"Usuario: {st.session_state.usuario['nombre']}")

# --- VISTAS ESPECÍFICAS ---
def vista_vecino():
    st.subheader("Publicar nueva denuncia")

    descripcion = st.text_area("Descripción del problema")
    categoria = st.selectbox("Categoría", ["Baches", "Alumbrado", "Señalización", "Otro"])
    imagen = st.file_uploader("Subir imagen", type=["jpg", "jpeg", "png"])
    calle = st.text_input("Calle")
    altura = st.number_input("Altura", min_value=0)
    barrio = st.text_input("Barrio")

    if st.button("Enviar Denuncia"):
        if not (descripcion and categoria and imagen and calle and altura and barrio):
            st.error("Completá todos los campos.")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Ubicacion (calle, altura, barrio)
            VALUES (%s, %s, %s)
            RETURNING id_ubicacion
        """, (calle, altura, barrio))
        id_ubicacion = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO Seguimiento (id_usuario, estado)
            VALUES (%s, 'pendiente')
            RETURNING id_seguimiento
        """, (st.session_state.usuario["id"],))
        id_seguimiento = cur.fetchone()[0]

        fecha = datetime.now()
        cur.execute("""
            INSERT INTO Denuncia (id_usuario, id_ubicacion, categoria, descripcion, fecha_hora, id_seguimiento)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_denuncia
        """, (
            st.session_state.usuario["id"],
            id_ubicacion,
            categoria,
            descripcion,
            fecha,
            id_seguimiento
        ))
        id_denuncia = cur.fetchone()[0]

        img_id = str(uuid4())
        img_path = f"imagenes/{img_id}.png"
        os.makedirs("imagenes", exist_ok=True)
        with open(img_path, "wb") as f:
            f.write(imagen.read())

        cur.execute("""
            INSERT INTO Imagen (id_denuncia, url_imagen, fecha_subida, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (
            id_denuncia,
            img_path,
            fecha,
            "Imagen de denuncia"
        ))

        conn.commit()
        cur.close()
        st.success("Denuncia enviada correctamente.")

def vista_autoridad():
    st.subheader("Panel de denuncias")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.id_denuncia, u.nombre AS denunciante, d.descripcion, d.categoria,
               ub.calle, ub.altura, ub.barrio, s.estado
        FROM Denuncia d
        JOIN Usuario u ON d.id_usuario = u.id_usuario
        JOIN Ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
        JOIN Seguimiento s ON d.id_seguimiento = s.id_seguimiento
        ORDER BY d.id_denuncia DESC
    """)
    rows = cur.fetchall()
    columnas = ["ID", "Denunciante", "Descripción", "Categoría", "Calle", "Altura", "Barrio", "Estado"]
    df = pd.DataFrame(rows, columns=columnas)
    st.dataframe(df, use_container_width=True)

    st.subheader("Actualizar estado de una denuncia")
    id_modificar = st.number_input("ID de denuncia", min_value=1, step=1)
    nuevo_estado = st.selectbox("Nuevo estado", ["pendiente", "en curso", "resuelto"])

    if st.button("Actualizar estado"):
        cur.execute("SELECT id_seguimiento FROM Denuncia WHERE id_denuncia = %s", (id_modificar,))
        seguimiento = cur.fetchone()
        if seguimiento:
            id_seguimiento = seguimiento[0]
            cur.execute("UPDATE Seguimiento SET estado = %s WHERE id_seguimiento = %s", (nuevo_estado, id_seguimiento))
            conn.commit()
            st.success("Estado actualizado correctamente.")
        else:
            st.error("Denuncia no encontrada.")
    cur.close()

# --- INTERFAZ PRINCIPAL ---
if st.session_state.logged_in:
    st.success(f"¡Bienvenido {st.session_state.usuario['nombre']}!")

    if st.button("Cerrar sesión"):
        st.session_state.logged_in = False
        del st.session_state.usuario
        st.session_state.current_view = "login"
        if "db_conn" in st.session_state:
            try:
                st.session_state.db_conn.close()
            except:
                pass
            del st.session_state.db_conn
        st.rerun()


    tipo = st.session_state.usuario["tipo"]
    if tipo == "vecino":
        menu_vecino()
    elif tipo == "autoridad":
        menu_autoridad()
    else:
        st.error("Tipo de usuario no reconocido.")
else:
    if st.session_state.current_view == "login":
        st.subheader("Iniciar Sesión")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
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
                st.rerun()

            else:
                st.error("Email o contraseña incorrectos.")
        if st.button("Registrarse"):
            st.session_state.current_view = "register"
    elif st.session_state.current_view == "register":
        st.subheader("Registrarse")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        password = st.text_input("Contraseña", type="password")
        if st.button("Crear cuenta"):
            if nombre and email and password:
                exito, mensaje = registrar_usuario(nombre, email, password)
                if exito:
                    st.success(mensaje)
                    st.session_state.current_view = "login"
                else:
                    st.error(mensaje)
            else:
                st.error("Completá todos los campos.")
        if st.button("Volver"):
            st.session_state.current_view = "login"
