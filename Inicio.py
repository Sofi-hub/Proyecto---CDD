# Inicio.py
import streamlit as st
import pandas as pd
from datetime import datetime
from uuid import uuid4
import os
import pydeck as pdk

from shared import get_connection, verificar_usuario, registrar_usuario
from streamlit_option_menu import option_menu

# --- Configuración de la app ---
st.set_page_config(page_title="Mi Reporte", layout="wide")

# --- Inicialización de session_state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None

<<<<<<< HEAD
# --- Función de Login / Registro ---
def pantalla_login():
    st.title("Mi Reporte")
    if st.session_state.view == "login":
        st.subheader("🔐 Iniciar sesión")
        email = st.text_input("Correo electrónico", key="in_email")
        pwd   = st.text_input("Contraseña", type="password", key="in_pwd")
        col1, col2 = st.columns([2,1])
        with col1:
            if st.button("Ingresar"):
                res = verificar_usuario(email, pwd)
                if res:
                    st.session_state.logged_in = True
                    st.session_state.usuario = {
                        "id": res[0],
                        "nombre": res[1],
                        "tipo": res[2]
                    }
                    st.rerun()
=======
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
>>>>>>> 5e2096c807d45faa2d42a30bf6a20e9eb22beef6
                else:
                    st.error("Email o contraseña incorrectos.")
        with col2:
            if st.button("Registrarse"):
                st.session_state.view = "register"

    else:  # registro
        st.subheader("📝 Registrarse")
        nombre = st.text_input("Nombre completo", key="reg_name")
        email  = st.text_input("Correo electrónico", key="reg_email")
        pwd    = st.text_input("Contraseña", type="password", key="reg_pwd")
        col1, col2 = st.columns([2,1])
        with col1:
            if st.button("Crear cuenta"):
                if nombre and email and pwd:
                    ok, msg = registrar_usuario(nombre, email, pwd)
                    if ok:
                        st.success(msg)
                        st.session_state.view = "login"
                    else:
                        st.error(msg)
                else:
                    st.error("Completá todos los campos.")
        with col2:
            if st.button("Volver"):
                st.session_state.view = "login"

# --- Vista Vecino: Mis denuncias con filtros ---
def mostrar_mi_cuenta():
    st.subheader("📋 Mis denuncias")

    # 1) Cargo los datos
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT descripcion, categoria, fecha_hora
          FROM Denuncia
         WHERE id_usuario = %(uid)s
         ORDER BY fecha_hora DESC
        """,
        conn,
        params={"uid": st.session_state.usuario["id"]}
    )
    if df.empty:
        st.info("Aún no tenés denuncias.")
        return

    # 2) Convierto fecha y ajusto columnas
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])
    df = df.rename(columns={"descripcion":"Descripción","categoria":"Categoría","fecha_hora":"Fecha"})

    # 3) Filtro por categoría
    cats = st.sidebar.multiselect(
        "Filtrar por categoría",
        options=df["Categoría"].unique(),
        default=list(df["Categoría"].unique()),
        key="filtro_cat_vecino"
    )
    df = df[df["Categoría"].isin(cats)]

    # 4) Ordenar por fecha
    orden = st.sidebar.selectbox(
        "Ordenar por fecha",
        ["Más recientes primero","Más antiguas primero"],
        key="orden_fecha_vecino"
    )
    ascending = True if orden == "Más antiguas primero" else False
    df = df.sort_values("Fecha", ascending=ascending)

    # 5) Muestro la tabla sin índice
    df.index = [""] * len(df)
    st.dataframe(df, use_container_width=True)


# --- Vista Vecino: Publicar denuncia ---
def publicar_denuncia():
    st.subheader("📢 Publicar nueva denuncia")
    descripcion = st.text_area("Descripción del problema")
    categoria   = st.selectbox("Categoría", ["Tránsito","Basura","Señalización","Delito","Otro"])
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
        # Ubicación
        cur.execute(
            "INSERT INTO Ubicacion (calle, altura, barrio) VALUES (%s,%s,%s) RETURNING id_ubicacion",
            (calle, altura, barrio)
        )
        id_ub = cur.fetchone()[0]
        # Seguimiento
        cur.execute(
            "INSERT INTO Seguimiento (id_usuario, estado) VALUES (%s,'pendiente') RETURNING id_seguimiento",
            (st.session_state.usuario["id"],)
        )
        id_seg = cur.fetchone()[0]
        # Denuncia
        now = datetime.now()
        cur.execute(
            """
            INSERT INTO Denuncia
              (id_usuario, id_ubicacion, categoria, descripcion, fecha_hora, id_seguimiento)
            VALUES (%s,%s,%s,%s,%s,%s) RETURNING id_denuncia
            """,
            (st.session_state.usuario["id"], id_ub, categoria, descripcion, now, id_seg)
        )
        id_den = cur.fetchone()[0]
        # Imagen opcional
        if imagen:
            img_id   = str(uuid4())
            img_path = f"imagenes/{img_id}.png"
            os.makedirs("imagenes", exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(imagen.read())
            cur.execute(
                """
                INSERT INTO Imagen (id_denuncia, url_imagen, fecha_subida, descripcion)
                VALUES (%s,%s,%s,%s)
                """,
                (id_den, img_path, now, "Imagen de denuncia")
            )
        conn.commit()
        cur.close()
        st.success("Denuncia enviada correctamente.")

# --- Vista Autoridad: Dashboard y filtros sin heatmap ---
def ver_denuncias_autoridad():
    st.subheader("🕵️‍♂️ Panel de denuncias (Autoridad)")
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT d.id_denuncia,
               u.nombre   AS denunciante,
               d.descripcion,
               d.categoria,
               ub.barrio,
               s.estado,
               d.fecha_hora
          FROM Denuncia d
          JOIN Usuario u ON d.id_usuario    = u.id_usuario
          JOIN Ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
          JOIN Seguimiento s ON d.id_seguimiento = s.id_seguimiento
         ORDER BY d.fecha_hora DESC
        """,
        conn
    )
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])

    # — SOLO FILTRO POR CATEGORÍA —
    st.sidebar.markdown("### Filtro (Autoridad)")
    cats = st.sidebar.multiselect(
        "Categorías",
        options=df["categoria"].unique(),
        default=list(df["categoria"].unique()),
        key="f_auth_cat"
    )
    df_f = df[df["categoria"].isin(cats)]

    # — ORDEN POR FECHA ASC/DESC —
    orden = st.sidebar.selectbox(
        "Ordenar por fecha",
        ["Más recientes primero", "Más antiguas primero"],
        key="f_auth_orden"
    )
    ascending = True if orden == "Más antiguas primero" else False
    df_f = df_f.sort_values("fecha_hora", ascending=ascending)

    # — Gráfico de barras por categoría —
    st.markdown("#### 📊 Denuncias por categoría")
    counts_cat = df_f["categoria"] \
        .value_counts() \
        .rename_axis("Categoría") \
        .reset_index(name="Cantidad")
    st.bar_chart(counts_cat.set_index("Categoría"))

    # — Gráfico de barras por barrio —
    st.markdown("#### 🗺️ Denuncias por barrio")
    counts_bar = df_f["barrio"] \
        .value_counts() \
        .rename_axis("Barrio") \
        .reset_index(name="Cantidad")
    st.bar_chart(counts_bar.set_index("Barrio"))

    # — Detalle y actualización de estado —
    st.markdown("#### 🚦 Detalle de denuncias")
    df_tab = df_f[["id_denuncia","denunciante","descripcion","categoria","estado","fecha_hora"]] \
        .rename(columns={
            "id_denuncia":"ID",
            "denunciante":"Denunciante",
            "descripcion":"Descripción",
            "categoria":"Categoría",
            "estado":"Estado",
            "fecha_hora":"Fecha"
        })
    st.dataframe(df_tab, use_container_width=True)

    st.subheader("Actualizar estado")
    id_mod = st.number_input("ID denuncia", int(df_tab["ID"].min()), step=1, key="upd_id")
    nuevo  = st.selectbox("Nuevo estado", ["pendiente","en curso","resuelto"], key="upd_est")
    if st.button("Actualizar estado"):
        cur = conn.cursor()
        cur.execute("SELECT id_seguimiento FROM Denuncia WHERE id_denuncia = %s", (id_mod,))
        r = cur.fetchone()
        if r:
            cur.execute("UPDATE Seguimiento SET estado = %s WHERE id_seguimiento = %s", (nuevo, r[0]))
            conn.commit()
            st.success("Estado actualizado correctamente.")
        else:
            st.error("ID no encontrado.")
        cur.close()


# --- Flujo principal ---
if st.session_state.logged_in:
    # Header y logout
    st.title("Mi Reporte")
    st.success(f"¡Bienvenido {st.session_state.usuario['nombre']}!")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.rerun()

    # Menú vertical
    tipo = st.session_state.usuario["tipo"]
    if tipo == "vecino":
        choice = option_menu(
            menu_title=None,
            options=["Mi Cuenta","Publicar denuncia"],
            icons=["clipboard-data","cloud-upload"],
            default_index=0,
            orientation="vertical",
            key="menu_vecino"
        )
        if choice == "Mi Cuenta":
            mostrar_mi_cuenta()
        else:
            publicar_denuncia()
    else:  # autoridad
        choice = option_menu(
            menu_title=None,
            options=["Ver denuncias"],
            icons=["clipboard-check"],
            default_index=0,
            orientation="vertical",
            key="menu_autoridad"
        )
        if choice == "Ver denuncias":
            ver_denuncias_autoridad()

else:
    pantalla_login()
    st.stop()
