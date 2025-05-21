import streamlit as st
import pandas as pd
from shared import get_connection

st.title("Mi cuenta")

if not st.session_state.get("logged_in", False):
    st.warning("Primero iniciá sesión en Inicio.")
elif st.session_state.usuario["tipo"] != "vecino":
    st.error("Solo vecinos pueden ver esta página.")
else:
    st.subheader(f"Hola, {st.session_state.usuario['nombre']}")
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""
        SELECT descripcion,categoria,s.estado,fecha_hora
        FROM Denuncia d
        JOIN Seguimiento s ON d.id_seguimiento=s.id_seguimiento
        WHERE d.id_usuario = %s
        ORDER BY fecha_hora DESC
    """, (st.session_state.usuario["id"],))
    rows = cur.fetchall(); cur.close()

    if rows:
        df = pd.DataFrame(rows,
             columns=["Descripción","Categoría","Estado","Fecha"])
        df.index = [""]*len(df)  # quita numeración
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aún no tenés denuncias.")
