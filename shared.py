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
    conn.close()
    return True, "Usuario registrado correctamente."

def verificar_usuario(email, contraseña):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_usuario, nombre, tipo_usuario FROM Usuario WHERE email = %s AND contraseña = %s", (email, contraseña))
        resultado = cur.fetchone()
        cur.close()
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"Error al verificar usuario: {e}")
        return None

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
