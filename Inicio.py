# Inicio.py
import streamlit as st
import pandas as pd
from datetime import datetime
from uuid import uuid4
import os
import pydeck as pdk

from shared import get_connection, verificar_usuario, registrar_usuario
from streamlit_option_menu import option_menu


CALLES_PILAR = [
    "11 de Septiembre", "25 de Mayo", "3 de Febrero", "9 de Julio", "A Lincoln", "A Vattuone", "Aconcagua",
    "Agustin Alvarez", "Agustoni", "Alberdi", "Alte G Brown", "Alte H Garcia Mansilla", "Americo Vespucio",
    "Ana Maria Mogas", "Antartida Argentina", "Antonio Bermudez", "Antonio Freixas", "Antonio Vieyra",
    "Apolinario Lubo", "Araoz de Lamadrid", "Argerich", "Armando Ferreyra", "Arrecifes", "Arturo Beruti",
    "Azcuenaga", "Azul", "Balcarce", "Basilio Musladini", "Bdier Gral J Zapiola", "Bdier J M de Rosas",
    "Beato Marcelino Champagnat", "Bergantin Balcarce", "Bergantin Congreso", "Bergantin Independ",
    "Bergantin Republica", "Bernardino Rivadavia", "Bogota", "Bolivia", "Bragado", "Brasil", "Buenos Aires",
    "Callao", "Camarones", "Camilo Costa", "Canada", "Cañonera Tortuga", "Cañuelas", "Caracas", "Carhue",
    "Carlos Calvo", "Carmen de Areco", "Casacuberta", "Catamarca", "Chacabuco", "Chaco", "Chascomus", "Chile",
    "Chivilcoy", "Chubut", "Cmte Luis Piedrabuena", "Cnel Baltazar Cardenas", "Cnel M Chilavert",
    "Cnel Pedro J Diaz", "Colombia", "Conrado Nale Roxlo", "Corbeta Belfast", "Corbeta Cefiro",
    "Corbeta Rosales", "Corbeta Uruguay", "Cordoba", "Costa Rica", "Cristian Rauch", "Cristobal Colon",
    "Crucero Gral Belgrano", "Cuarenta Leguas", "Cuba", "Daireaux", "Dardo Rocha", "De la Visitacion",
    "Dolores", "Domingo F Sarmiento", "Domingo French", "Dr A Alsina", "Dr Alejandro Korn",
    "Dr Bernardo Houssay", "Dr Ignacio Pirovano", "Dr Jose Ingenieros", "Dr Juan Jose Paso", "Dr Luis Agote",
    "Dr Luis Belaustegui", "Dr Luis Pasteur", "Dr Osvaldo Eguia", "Dr Pedro Narciso Arata", "Dr Pelagio B Luna",
    "Dr Penna", "Dr Ricardo Levenne", "Dr Romulo s Naon", "Dr Velez Sarsfield", "Ecuador", "El Boyero",
    "El Cardenal", "El Ceibo", "El Chingolo", "El Colibri", "El Hornero", "El Jilguero", "El Lucero",
    "El Mirlo", "El Ñandu", "El Peteribi", "El Petrel", "El Rincon", "El Tordo", "El Zorzal", "Ensenada",
    "Ernesto Nazarre", "Ernesto Tornquist", "Escobar", "Estados Unidos", "Estanislao Lopez",
    "Estanislao Zeballos", "Esteban de Luca", "Esteban Echeverria", "Eva Peron", "Evaristo Carriego",
    "Exaltacion de la Cruz", "Feliciano Chiclana", "Felix de Olazabal", "Fermin Gamboa", "Fgta Hercules",
    "Fgta Heroina", "Fgta la Argentina", "Fgta Pte Sarmiento", "Fitz Roy", "Florentino Ameghino", "Formosa",
    "Fortez", "Fragata Trinidad", "Francisco de Laprida", "Francisco Lauria", "Francisco Pizarro",
    "Fray Luis Beltran", "Gaboto", "Gdero Baigorria", "George Washington", "Goleta Constitucion",
    "Goleta Juliet", "Goleta Rio", "Goleta Sarandi", "Gral Francisco Ramirez", "Gral Guemes",
    "Gral Jose G Artigas", "Gral Jose M Bustillo", "Gral Jose Maria Paz", "Gral Juan Jose Viamonte",
    "Gral Juan M de Pueyrredon", "Gral las Heras", "Gral M Soler", "Gral Manuel Belgrano",
    "Gral Mariano Acha", "Gral Mariano Necochea", "Gral O Higgins", "Gral San Martin", "Gral Simon Bolivar",
    "Gral Tomas Guido", "Gregorio de Laferrere", "Guatemala", "Haiti", "Hernan Cortez", "Hernandarias",
    "Hernando de Magallanes", "Hilario Ascasubi", "Hipolito Bouchard", "Honduras", "Honorio Leguizamon",
    "Independencia", "Ing Guillermo Marconi", "Isla de los Estados", "Isla Lennox", "Isla Nueva",
    "Isla Picton", "Islas Malvinas", "Ituzaingo", "J de Garay", "Joaquin V Gonzalez", "Jorge Manfredi",
    "Jose C Paz", "Jose Garibaldi", "Jose Hernandez", "Jose Marmol", "Juan Bautista Justo",
    "Juan Diaz de Solis", "Juan Domingo Peron", "Juan Hipolito Vieytes", "Juan Jose Castelli",
    "Juan Sanguinetti", "Jujuy", "Junin", "La Carreta", "La Garza", "La Gaviota", "La Golondrina",
    "La Martineta", "La Paz", "La Perdiz", "La Rioja", "La Tapera", "La Tijereta", "La Torcaza",
    "Lago Alumine", "Lago Argentino", "Lago Cardiel", "Lago Clhue Huapi", "Lago Fagnano", "Lago Lacar",
    "Lago Mascardi", "Lago Nahuel Huapi", "Lago Traful", "Lago Viedma", "Laguna Chascomus",
    "Laguna de Monte", "Lanin", "Las Alondras", "Las Glicinas", "Las Lomas", "Las Madreselvas",
    "Las Margaritas", "Las Palomas", "Las Piedras", "Las Rosas", "Las Truchas", "Las Violetas",
    "Leopoldo Lugones", "Lisandro de la Torre", "Lizaso", "Loberia", "Lobos", "Lorenzo Lopez", "Los Alamos",
    "Los Arrayanes", "Los Claveles", "Los Gorriones", "Los Jazmines", "Los Lirios", "Los Naranjos",
    "Los Nomeolvides", "Los Patos", "Los Sauces", "Los Teros", "Los Tulipanes", "Lucio V Mansilla",
    "Luis Bataglia", "Luis Lagomarsino", "Lujan", "Magdalena", "Maipu", "Manantial", "Manuel Buide",
    "Manuel de Sarratea", "Manuel Martignone", "Manuel Martitegui", "Marcos Juarez", "Maria Cabezas",
    "Mariano Acosta", "Martin Coronado", "Martin de Gainza", "Medanos", "Mendoza", "Mercedario", "Mercedes",
    "Mexico", "Miguel Cane", "Miguel de Unamuno", "Misiones", "Mons Miguel de Andrea", "Montevideo",
    "Moreno", "Navarro", "Neuquen", "Nicaragua", "Olavarria", "Olegario V Andrade", "Oliverio Girondo",
    "Ottawa", "Pampa", "Panama", "Panamericana", "Paraguay", "Parana", "Patagones", "Patricias Argentinas",
    "Pbto Silvio Braschi", "Pedro B Palacios", "Pedro Cabral", "Pedro de Mendoza", "Pedro Lagrave",
    "Pergamino", "Peru", "Pigue", "Pilar", "Posadas", "Pres Gral J A Roca", "Pte H Yrigoyen", "Pte J D Peron",
    "Pte M T de Alvear", "Puan", "R Saenz Peña", "Rastreador Fournier", "Ricardo Guiraldes", "Ricardo Rojas",
    "Rio de Janeiro", "Rio Negro", "Rio Primero", "Rio Segundo", "Rio Tercero", "Rn 8", "Roberto Arlt",
    "Ruta 25", "Ruta 8", "Ruta Prov 25", "Ruta Prov 28", "Ruta Prov. 34", "Saladillo", "Saliquelo", "Salta",
    "San Jorge", "San Lorenzo", "San Luis", "San Pedro", "San Salvador", "Santa Agueda", "Santa Fe",
    "Santa Maria", "Santiago de Liniers", "Santiago del Estero", "Santo Domingo", "Saravi", "Sebastian Elcano",
    "Sgto Juan B Cabral", "Suipacha", "T M de Anchorena", "Tandil", "Tierra del Fuego", "Tomas Marquez",
    "Tratado del Pilar", "Tres Arroyos", "Tronador", "Tucuman", "Tupungato", "Uriburu", "Urquiza", "Uruguay",
    "Vasco Da Gama", "Vedia", "Venancio Castro", "Venezuela", "Viamonte", "Victor V Vergani",
    "Virrey Joaquin del Pino", "Virrey Loreto", "Vuelta de Obligado", "Yapeyu"
]

Barrios = ["Zelaya","Villa Rosa","Luis Lagomarsino","Del Viso","Manuel Alberti","La Lonja","Presidente Derqui","Villa Astolfi","Manzone","Pilar",
    "Pilar Sur","San Francisco","Champagnat","Fátima","Manzanares"]


# --- Configuración de la app ---
st.set_page_config(page_title="Mi Reporte", layout="wide")

# --- Inicialización de session_state ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "view" not in st.session_state:
    st.session_state.view = "login"
if "usuario" not in st.session_state:
    st.session_state.usuario = None

# --- Función de Login / Registro ---
# --- Función principal de login / registro ---
def pantalla_login():
    st.title("Mi Reporte")

    if st.session_state.view == "login":
        st.subheader("🔐 Iniciar sesión")
        email = st.text_input("Correo electrónico", key="login_email")
        pwd = st.text_input("Contraseña", type="password", key="login_pwd")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Ingresar"):
                usuario = verificar_usuario(email, pwd)
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
        with col2:
            if st.button("Registrarse"):
                st.session_state.view = "register"
                st.rerun()

    elif st.session_state.view == "register":
        st.subheader("📝 Registrarse")
        nombre = st.text_input("Nombre completo", key="reg_nombre")
        email = st.text_input("Correo electrónico", key="reg_email")
        pwd = st.text_input("Contraseña", type="password", key="reg_pwd")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("Crear cuenta"):
                if nombre and email and pwd:
                    ok, msg = registrar_usuario(nombre, email, pwd)
                    if ok:
                        st.success(msg)
                        st.session_state.view = "login"
                        st.rerun()
                    else:
                        st.error(msg)
                else:
                    st.error("Completá todos los campos.")
        with col2:
            if st.button("Volver"):
                st.session_state.view = "login"
                st.rerun()


# --- CALLBACKS ---
def go_to_register():
    st.session_state.current_view = "register"

def go_to_login():
    st.session_state.current_view = "login"


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
    import requests
    from streamlit_folium import st_folium
    import folium

    st.subheader("📢 Publicar nueva denuncia")

    descripcion = st.text_area("Descripción del problema")
    categoria = st.selectbox("Categoría", ["Tránsito", "Basura", "Señalización", "Delito", "Otro"])
    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "jpeg", "png"])

    # --- Inicializar valores en session_state si no existen
    for campo in ["calle_auto", "altura_auto", "barrio_auto"]:
        if campo not in st.session_state:
            st.session_state[campo] = None

    # --- Función de reverse geocoding
    def reverse_geocode_osm(lat, lon):
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat, "lon": lon, "format": "json"}
        headers = {"User-Agent": "MiReporteApp/1.0"}
        try:
            res = requests.get(url, params=params, headers=headers).json()
            calle = res.get("address", {}).get("road")
            altura = res.get("address", {}).get("house_number")
            barrio = res.get("address", {}).get("suburb") or res.get("address", {}).get("city_district")
            return calle, altura, barrio
        except:
            return None, None, None

    # --- Mapa
    st.markdown("### 📍 Marcar ubicación y completar dirección")

    col1, col2 = st.columns([2, 3])

    with col1:
        m = folium.Map(location=[-34.45, -58.91], zoom_start=13)
        m.add_child(folium.LatLngPopup())
        output = st_folium(m, height=350)

    lat_sel, lon_sel = None, None
    calle_auto, altura_auto, barrio_auto = None, None, None

    if output["last_clicked"]:
        lat_sel = output["last_clicked"]["lat"]
        lon_sel = output["last_clicked"]["lng"]
        st.success(f"Ubicación marcada: {lat_sel:.5f}, {lon_sel:.5f}")

        calle_auto, altura_auto, barrio_auto = reverse_geocode_osm(lat_sel, lon_sel)
        if altura_auto:
            altura_auto = str(altura_auto)
    else:
        st.warning("📍 Marcá la ubicación en el mapa para completar la dirección.")
        return

    with col2:
        st.markdown("### 📝 Ubicación del problema")
        st.text_input("Calle detectada automáticamente", value=calle_auto or "", disabled=True)
        calle = calle_auto
        altura_str = st.text_input("Altura", value=altura_auto or "")
        opciones_barrios = ["Seleccioná una localidad"] + Barrios
        if barrio_auto in Barrios:
            idx_barrio = Barrios.index(barrio_auto) + 1
        else:
            idx_barrio = 0
        barrio = st.selectbox("Localidad", opciones_barrios, index=idx_barrio)

    # --- Enviar
    if st.button("Enviar Denuncia"):
        if not (descripcion and categoria and calle and barrio != "Seleccioná una localidad" and altura is not None and lat_sel and lon_sel):
            st.error("Completá todos los campos obligatorios y marcá la ubicación en el mapa.")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO ubicacion (calle, altura, barrio, latitud, longitud) VALUES (%s, %s, %s, %s, %s) RETURNING id_ubicacion",
            (calle, altura, barrio, lat_sel, lon_sel)
        )
        id_ub = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO seguimiento (id_usuario, estado) VALUES (%s, 'pendiente') RETURNING id_seguimiento",
            (st.session_state.usuario["id"],)
        )
        id_seg = cur.fetchone()[0]

        now = datetime.now()
        cur.execute(
            """
            INSERT INTO denuncia (id_usuario, id_ubicacion, categoria, descripcion, fecha_hora, id_seguimiento)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_denuncia
            """,
            (st.session_state.usuario["id"], id_ub, categoria, descripcion, now, id_seg)
        )
        id_den = cur.fetchone()[0]

        if imagen:
            img_id = str(uuid4())
            img_path = f"imagenes/{img_id}.png"
            os.makedirs("imagenes", exist_ok=True)
            with open(img_path, "wb") as f:
                f.write(imagen.read())
            cur.execute(
                """
                INSERT INTO imagen (id_denuncia, url_imagen, fecha_subida, descripcion)
                VALUES (%s, %s, %s, %s)
                """,
                (id_den, img_path, now, "Imagen de denuncia")
            )

        conn.commit()
        cur.close()
        st.success("✅ Denuncia enviada correctamente.")
        st.session_state.calle_auto = None
        st.session_state.altura_auto = None
        st.session_state.barrio_auto = None




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
