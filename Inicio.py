# Inicio.py
import streamlit as st
import pandas as pd
from datetime import datetime
from uuid import uuid4
import os
import pydeck as pdk
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import plotly.express as px

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
        ["Más antiguas primero","Más recientes primero"],
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
    categoria = st.selectbox("Categoría", ["Tránsito", "Obstrucción vía pública","Iluminación","Basura", "Señalización", "Delito", "Ruidos molestos", "Vandalismo", "Deterioro vial","Otro"])
    imagen = st.file_uploader("Subir imagen (opcional)", type=["jpg", "jpeg", "png"])

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

        # Geocodificación inversa
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {"lat": lat_sel, "lon": lon_sel, "format": "json"}
        headers = {"User-Agent": "MiReporteApp/1.0"}
        try:
            res = requests.get(url, params=params, headers=headers).json()
            calle_auto = res.get("address", {}).get("road")
            altura_auto = res.get("address", {}).get("house_number")
            if altura_auto:
                altura_auto = str(altura_auto)
            barrio_auto = res.get("address", {}).get("suburb") or res.get("address", {}).get("city_district")
        except:
            st.error("No se pudo obtener la dirección desde el mapa.")
    else:
        st.warning("📍 Marcá la ubicación en el mapa para completar la dirección.")
        return

    with col2:
        st.success(f"Ubicación marcada: {lat_sel:.5f}, {lon_sel:.5f}")
        st.markdown("### Ubicación del problema")

        st.text_input("Calle detectada automáticamente", value=calle_auto or "", disabled=True, key="calle_auto")
        calle = calle_auto

        altura_str = st.text_input("Altura (opcional)", value=altura_auto or "", key="altura_input")
       # Validación manual
        if altura_str.strip() == "":
            altura = None
        elif altura_str.strip().isdigit():
            altura = int(altura_str.strip())
        else:
            st.error("La altura debe contener solo números o dejarse vacía.")
            return  # corta el flujo sin intentar guardar nada

        opciones_barrios =  Barrios
        if barrio_auto in Barrios:
            idx_barrio = Barrios.index(barrio_auto) + 1
        else:
            idx_barrio = 0
        barrio = st.selectbox("Seleccione una localidad", opciones_barrios, index=idx_barrio, key="barrio_input")

        if st.button("Enviar Denuncia"):
            if not (descripcion and categoria and calle and barrio != "Seleccioná una localidad" and lat_sel and lon_sel):
                st.error("Completá todos los campos obligatorios y marcá la ubicación en el mapa.")
            else:
                conn = get_connection()
                cur = conn.cursor()

                cur.execute(
                    "INSERT INTO ubicacion (calle, altura, localidad, latitud, longitud) VALUES (%s, %s, %s, %s, %s) RETURNING id_ubicacion",
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






# --- Vista Autoridad: Dashboard y filtros sin heatmap ---
def ver_denuncias_autoridad():
    st.subheader("🕵️‍♂️ Panel de denuncias")
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT d.id_denuncia,
               u.nombre   AS denunciante,
               d.descripcion,
               d.categoria,
               ub.localidad,
               s.estado,
               d.fecha_hora
          FROM denuncia d 
          JOIN usuario u ON d.id_usuario    = u.id_usuario
          JOIN ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
          JOIN seguimiento s ON d.id_seguimiento = s.id_seguimiento
         ORDER BY d.fecha_hora DESC
        """,
        conn
    )
    df["fecha_hora"] = pd.to_datetime(df["fecha_hora"])

    # --- Filtros en la barra lateral ---
    st.sidebar.markdown("### Filtros")

    # Filtro por categoría
    cats = st.sidebar.multiselect(
        "Categorías",
        options=df["categoria"].unique(),
        default=list(df["categoria"].unique()),
        key="filtro_categoria_autoridad"
    )

    # Filtro por localidad
    localidades = sorted(df["localidad"].dropna().unique())

    

    localidades_sel = st.sidebar.multiselect(
        "Seleccioná una o más localidades",
        options=localidades,
        default=localidades,
        key="filtro_localidad_autoridad"
    )

    # Filtro por estado de la denuncia
    estados = sorted(df["estado"].dropna().unique())
    estados_sel = st.sidebar.multiselect(
        "Estados",
        options=estados,
        default=estados,
        key="filtro_estado_autoridad"
    )


    # Orden por fecha
    orden = st.sidebar.selectbox(
        "Ordenar por fecha",
        ["Más antiguas primero", "Más recientes primero"],
        key="orden_fecha_autoridad"
    )
    ascending = True if orden == "Más antiguas primero" else False

    # --- Aplicar filtros ---
    df_f = df[
        (df["categoria"].isin(cats)) &
        (df["localidad"].isin(localidades_sel)) & (df["estado"].isin(estados_sel))
    ].sort_values("fecha_hora", ascending=ascending)

    # Cargar imágenes vinculadas
    df_img = pd.read_sql("SELECT id_denuncia, url_imagen FROM imagen", conn)
    df_f = pd.merge(df_f, df_img, how="left", on="id_denuncia")

    # — Detalle de denuncias —
    st.markdown("#### 🚦 Detalle de denuncias")
    with st.expander("Mostrar/Ocultar", expanded=False):
        df_tab = df_f[["id_denuncia","denunciante","descripcion","categoria","estado","fecha_hora"]] \
            .rename(columns={
                "id_denuncia":"ID",
                "denunciante":"Denunciante",
                "descripcion":"Descripción",
                "categoria":"Categoría",
                "estado":"Estado",
                "fecha_hora":"Fecha" 
            })
        df_tab.index = [""] * len(df_tab) # esto es para que no se vea la numeración de la tabla. con los ID ya es suficiente.
        st.dataframe(df_tab, use_container_width=True, hide_index=True)
        if st.button("🔄 Actualizar tabla"):
            st.rerun()
    # --- Botones de ver imagen ---
    st.markdown("#### 📸 Ver imagen adjunta")

    id_img_input = st.number_input("Ingresá el ID de una denuncia",min_value=1, step=1, key="ver_img_id")

    if st.button("Mostrar imagen"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT url_imagen FROM imagen WHERE id_denuncia = %s",
            (id_img_input,)
        )
        r = cur.fetchone()
        cur.close()

        if r and r[0]:
            st.image(r[0], caption=f"Imagen asociada a la denuncia #{id_img_input}", use_container_width=True)
        else:
            st.info("📭 Esta denuncia no tiene una imagen adjunta.")


    # — Actualizar estado —
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
def ver_estadisticas():
    st.subheader("📊 Estadísticas de denuncias")

    conn = get_connection()
    df = pd.read_sql("""
        SELECT d.id_denuncia,
            d.categoria,
            ub.localidad,
            s.estado,
            d.fecha_hora
        FROM denuncia d
        JOIN ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
        JOIN seguimiento s ON d.id_seguimiento = s.id_seguimiento
    """, conn)
    conn.close()

    # Gráfico de barras por categoría
    st.markdown("#### Denuncias por categoría")

    cat_counts = df["categoria"].value_counts().rename_axis("Categoría").reset_index(name="Cantidad")

    categorias_colores = {
    "Tránsito": "#e74c3c",
    "Obstrucción vía pública": "#f39c12",
    "Iluminación": "#f1c40f",
    "Basura": "#2ecc71",
    "Señalización": "#3498db",
    "Delito": "#9b59b6",
    "Ruidos molestos": "#34495e",
    "Vandalismo": "#e67e22",
    "Deterioro vial": "#1abc9c",
    "Otro": "#7f8c8d"
    }

    fig = px.bar(
        cat_counts,
        x="Categoría",
        y="Cantidad",
        color="Categoría",  # Cada categoría tiene color distinto
        color_discrete_map= categorias_colores  # Paleta de colores suaves
    )
    fig.update_layout(
    yaxis=dict(
        tickmode="linear",  
        tick0=0,            
        dtick=1             
        )
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)

    # Gráfico de barras por localidad
    st.markdown("#### Denuncias por localidad y categoría")

    # Agrupar por localidad y categoría
    loc_cat_counts = df.groupby(["localidad", "categoria"]).size().reset_index(name="Cantidad")

    # Crear gráfico de barras apiladas
    fig = px.bar(
        loc_cat_counts,
        x="localidad",
        y="Cantidad",
        color="categoria",
        labels={"localidad": "Localidad", "categoria": "Categoría", "Cantidad": "Cantidad"},
        color_discrete_map=categorias_colores  # Paleta linda y suave
    )
    fig.update_layout(
    yaxis=dict(
        tickmode="linear",  
        tick0=0,            
        dtick=1             
        )
    )

    # Opcional: ordenar por cantidad total descendente
    fig.update_layout(
        xaxis={'categoryorder': 'total descending'},
        barmode='stack'
    )

    st.plotly_chart(fig)

    # Piechart según estado de la denuncia
    st.markdown("### Distribución porcentual por estado de las denuncias")
    st.plotly_chart(px.pie(df, names="estado"))


from folium.plugins import HeatMap
from streamlit_folium import st_folium
import folium

def ver_mapa_calor():
    st.subheader("🗺️ Mapa de calor de denuncias con actualización por zona visible")

    conn = get_connection()
    df = pd.read_sql("""
        SELECT d.id_denuncia, d.categoria, s.estado, d.id_seguimiento,
               ub.localidad, ub.latitud, ub.longitud
        FROM denuncia d
        JOIN ubicacion ub ON d.id_ubicacion = ub.id_ubicacion
        JOIN seguimiento s ON d.id_seguimiento = s.id_seguimiento
        WHERE ub.latitud IS NOT NULL AND ub.longitud IS NOT NULL
    """, conn)

    df = df[df["estado"].isin(["pendiente", "en curso"])]

    categorias = sorted(df["categoria"].dropna().unique())
    categorias_sel = st.sidebar.multiselect("Categorías", categorias, default=categorias)

    localidades = sorted(df["localidad"].dropna().unique())
    localidades_sel = st.sidebar.multiselect("Localidades", localidades, default=localidades)

    df_f = df[
        (df["categoria"].isin(categorias_sel)) &
        (df["localidad"].isin(localidades_sel))
    ]

    # Inicializar estado de zoom y centro del mapa
    if "map_center" not in st.session_state:
        st.session_state.map_center = [-34.45, -58.91]
    if "map_zoom" not in st.session_state:
        st.session_state.map_zoom = 12

    col1, col2 = st.columns([3, 2])

    with col1:
        # Mapa con centro y zoom desde el estado
        m = folium.Map(location=st.session_state.map_center, zoom_start=st.session_state.map_zoom)
        HeatMap(df_f[["latitud", "longitud"]].values.tolist(), radius=15).add_to(m)
        colores_categorias = {
            "Tránsito": "red",
            "Obstrucción vía pública": "orange",
            "Iluminación": "lightgray",
            "Basura": "green",
            "Señalización": "blue",
            "Delito": "purple",
            "Ruidos molestos": "gray",
            "Vandalismo": "darkred",
            "Deterioro vial": "cadetblue",
            "Otro": "black"
        }
        for _, row in df_f.iterrows():
            folium.Marker(
                location=[row["latitud"], row["longitud"]],
                popup=f"<b>Categoría:</b> {row['categoria']}<br><b>Estado:</b> {row['estado']}",
                icon=folium.Icon(color=colores_categorias.get(row["categoria"], "black"), icon="info-sign")
            ).add_to(m)

        map_output = st_folium(m, height=600, returned_objects=["bounds", "last_clicked"])

        # Si se hizo clic, actualizar centro y hacer zoom
        if map_output and "last_clicked" in map_output and map_output["last_clicked"]:
            click = map_output["last_clicked"]
            st.session_state.map_center = [click["lat"], click["lng"]]
            st.session_state.map_zoom = 16
            st.rerun()

        # Botón para volver a vista general
        if st.button("🔙 Volver al mapa general"):
            st.session_state.map_center = [-34.45, -58.91]
            st.session_state.map_zoom = 12
            st.rerun()

    with col2:
        st.markdown("### 🔄 Actualizar estado")
        nuevo_estado = st.selectbox("Seleccionar nuevo estado", ["pendiente", "en curso", "resuelto"])

        if map_output and "bounds" in map_output:
            bounds = map_output["bounds"]
            south = bounds["_southWest"]["lat"]
            west  = bounds["_southWest"]["lng"]
            north = bounds["_northEast"]["lat"]
            east  = bounds["_northEast"]["lng"]

            cur = conn.cursor()
            cur.execute("""
                SELECT COUNT(*)
                FROM denuncia d
                JOIN ubicacion u ON d.id_ubicacion = u.id_ubicacion
                WHERE u.latitud BETWEEN %s AND %s
                  AND u.longitud BETWEEN %s AND %s
                  AND d.categoria = ANY(%s)
                  AND u.localidad = ANY(%s)
            """, (
                south, north, west, east,
                categorias_sel,
                localidades_sel
            ))
            cantidad = cur.fetchone()[0]

            if cantidad > 0:
                st.info(f"Se actualizarán {cantidad} denuncias dentro del área visible del mapa.")
                if st.button("✅ Actualizar denuncias visibles"):
                    cur.execute("""
                        UPDATE seguimiento
                        SET estado = %s
                        WHERE id_seguimiento IN (
                            SELECT d.id_seguimiento
                            FROM denuncia d
                            JOIN ubicacion u ON d.id_ubicacion = u.id_ubicacion
                            WHERE u.latitud BETWEEN %s AND %s
                              AND u.longitud BETWEEN %s AND %s
                              AND d.categoria = ANY(%s)
                              AND u.localidad = ANY(%s)
                        )
                    """, (
                        nuevo_estado,
                        south, north, west, east,
                        categorias_sel,
                        localidades_sel
                    ))
                    conn.commit()
                    st.success("✅ Estado actualizado correctamente.")
            else:
                st.warning("No hay denuncias visibles con los filtros actuales.")
            cur.close()
        else:
            st.warning("📍 Mové, acercate o hacé clic en el mapa para seleccionar una zona.")
        st.markdown("### 🗂️ Referencia de categorías")

        colores_categorias = {
            "Tránsito": "red",
            "Obstrucción vía pública": "orange",
            "Iluminación": "lightgray",
            "Basura": "green",
            "Señalización": "blue",
            "Delito": "purple",
            "Ruidos molestos": "gray",
            "Vandalismo": "darkred",
            "Deterioro vial": "cadetblue",
            "Otro": "black"
        }

        for cat, color in colores_categorias.items():
            st.markdown(
                f"<div style='display: flex; align-items: center;'>"
                f"<div style='width: 15px; height: 15px; background-color: {color}; "
                f"margin-right: 8px; border: 1px solid #000;'></div>"
                f"{cat}</div>",
                unsafe_allow_html=True
            )
    conn.close()



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
            options=["Ver denuncias", "Ver estadísticas", "Mapa de calor"],
            icons=["clipboard-check", "bar-chart-line", "map"],
            default_index=0,
            orientation="vertical",
            key="menu_autoridad"
        )
        if choice == "Ver denuncias":
            ver_denuncias_autoridad()
        elif choice == "Mapa de calor":
            ver_mapa_calor()
        elif choice == "Ver estadísticas":
            ver_estadisticas()

else:
    pantalla_login()
    st.stop()
