# functions.py
import streamlit as st
from shared import get_connection
from datetime import datetime
from uuid import uuid4
import os
import pandas as pd

def vista_vecino():
    """Formulario de denuncia (imagen opcional)."""
    descripcion = st.text_area("Descripción del problema")
    categoria   = st.selectbox("Categoría", ["Baches","Alumbrado","Señalización","Otro"])
    imagen      = st.file_uploader("Subir imagen (opcional)", type=["jpg","jpeg","png"])
    calle       = st.text_input("Calle")
    altura      = st.number_input("Altura", min_value=0)
    barrio      = st.text_input("Barrio")

    if st.button("Enviar Denuncia"):
        if not (descripcion and categoria and calle and altura and barrio):
            st.error("Completá todos los campos (imagen opcional).")
            return

        conn = get_connection()
        cur  = conn.cursor()
        # 1) Ubicación
        cur.execute(
            "INSERT INTO Ubicacion (calle, altura, barrio) VALUES (%s,%s,%s) RETURNING id_ubicacion",
            (calle, altura, barrio)
        )
        id_ubicacion = cur.fetchone()[0]
        # 2) Seguimiento
        cur.execute(
            "INSERT INTO Seguimiento (id_usuario, estado) VALUES (%s,'pendiente') RETURNING id_seguimiento",
            (st.session_state.usuario["id"],)
        )
        id_seguimiento = cur.fetchone()[0]
        # 3) Denuncia
        ahora = datetime.now()
        cur.execute(
            """
            INSERT INTO Denuncia
              (id_usuario, id_ubicacion, categoria, descripcion, fecha_hora, id_seguimiento)
            VALUES (%s,%s,%s,%s,%s,%s) RETURNING id_denuncia
            """,
            (st.session_state.usuario["id"], id_ubicacion, categoria,
             descripcion, ahora, id_seguimiento)
        )
        id_denuncia = cur.fetchone()[0]
        # 4) Imagen (si subió)
        if imagen:
            img_id   = str(uuid4())
            img_path = f"imagenes/{img_id}.png"
            os.makedirs("imagenes", exist_ok=True)
            with open(img_path,"wb") as f: f.write(imagen.read())
            cur.execute(
                "INSERT INTO Imagen (id_denuncia, url_imagen, fecha_subida, descripcion) VALUES (%s,%s,%s,%s)",
                (id_denuncia, img_path, ahora, "Imagen de denuncia")
            )
        conn.commit()
        cur.close()
        st.success("Denuncia enviada correctamente.")

def vista_autoridad():
    """Tabla de denuncias + actualización de estado."""
    conn = get_connection()
    cur  = conn.cursor()
    cur.execute("""
        SELECT d.id_denuncia, u.nombre, d.descripcion, d.categoria,
               ub.calle, ub.altura, ub.barrio, s.estado
        FROM Denuncia d
        JOIN Usuario u ON d.id_usuario = u.id_usuario
        JOIN Ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
        JOIN Seguimiento s ON d.id_seguimiento = s.id_seguimiento
        ORDER BY d.id_denuncia DESC
    """)
    rows = cur.fetchall()
    cur.close()

    df = pd.DataFrame(rows,
        columns=["ID","Denunciante","Descripción","Categoría","Calle","Altura","Barrio","Estado"])
    st.dataframe(df, use_container_width=True)

    st.subheader("Actualizar estado de una denuncia")
    id_mod = st.number_input("ID de denuncia", min_value=1, step=1)
    nuevo  = st.selectbox("Nuevo estado", ["pendiente","en curso","resuelto"])
    if st.button("Actualizar estado"):
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute("SELECT id_seguimiento FROM Denuncia WHERE id_denuncia = %s", (id_mod,))
        res = cur.fetchone()
        if res:
            cur.execute("UPDATE Seguimiento SET estado = %s WHERE id_seguimiento = %s",
                        (nuevo, res[0]))
            conn.commit()
            st.success("Estado actualizado correctamente.")
        else:
            st.error("ID no encontrado.")
        cur.close()
