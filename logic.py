import sqlite3
from datetime import datetime, timedelta
import os
import openpyxl

def crear_tabla_reservas():
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect("calendario.db")
    cursor = conexion.cursor()

    # Crear la tabla de reservas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banda TEXT NOT NULL,
            sala TEXT NOT NULL,
            fecha TEXT NOT NULL,
            horario TEXT NOT NULL,
            tiempo TEXT NOT NULL,
            abonado TEXT NOT NULL
        )
    ''')

    # Cerrar la conexión con la base de datos
    conexion.close()

def crear_db_tabs():
    conn = sqlite3.connect("tabs_database.db")
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tabs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tab_name TEXT
        )
    """)

    # Crear tabla para consumiciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consumiciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tab_id INTEGER,
            nombre TEXT,
            precio REAL
        )
    """)

    conn.commit()

def guardar_tab_en_db(tab_name):
    conn = sqlite3.connect("tabs_database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO tabs (tab_name) VALUES (?)", (tab_name,))
    conn.commit()

    tab_id = cursor.lastrowid  # Obtener el último ID insertado
    conn.close()

    return tab_id

def guardar_en_consumision_db(tab_id, nombre_consumo, precio_consumo):
    if tab_id is not None:
        conn = sqlite3.connect("tabs_database.db")
        cursor = conn.cursor()

        # Guardar la consumición en la tabla de consumiciones
        cursor.execute("INSERT INTO consumiciones (tab_id, nombre, precio) VALUES (?, ?, ?)",
                       (tab_id, nombre_consumo, precio_consumo))
        conn.commit()

        conn.close()

def borrar_tab_actual_db(tab_id):
    if tab_id is not None:
        # Borrar consumiciones asociadas a este tab de la tabla de consumiciones
        conn = sqlite3.connect("tabs_database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM consumiciones WHERE tab_id = ?", (tab_id,))
        conn.commit()
        conn.close()

def recuperar_tab_de_db(nombre_tab):
    conn = sqlite3.connect("tabs_database.db")
    cursor = conn.cursor()

    # Recuperar consumiciones de la base de datos
    cursor.execute("SELECT nombre, precio FROM consumiciones WHERE tab_id = ?", (nombre_tab,))
    consumiciones = cursor.fetchall()

    conn.close()
    return consumiciones

def toggle_mode(mode_switch, style, tab_bar):
    frame_widgets = tab_bar.get_frame_widgets()
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-dark")
        tab_bar.configure(bg="#313131")
        frame_widgets.configure(bg="#313131")
    else:
        style.theme_use("forest-light")
        tab_bar.configure(bg="white")
        frame_widgets.configure(bg="white")
        

def guardar_reserva(banda, sala, fecha, horario, tiempo, abonado):
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect("calendario.db")
    cursor = conexion.cursor()

    # Insertar la reserva en la base de datos
    cursor.execute('''
        INSERT INTO reservas (banda, sala, fecha, horario, tiempo, abonado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (banda, sala, fecha, horario, tiempo, abonado))

    # Guardar los cambios en la base de datos y cerrar la conexión
    conexion.commit()
    conexion.close()

    # Retornar el ID de la banda
    return cursor.lastrowid

def borrar_reserva_por_datos(banda, sala, fecha, horario):
    try:
        # Configurar la conexión con la base de datos SQLite
        conexion = sqlite3.connect("calendario.db")
        cursor = conexion.cursor()

        # Eliminar la reserva con los valores correspondientes
        cursor.execute('''
            DELETE FROM reservas
            WHERE banda = ? AND sala = ? AND fecha = ? AND horario = ?
        ''', (banda, sala, fecha, horario))

        conexion.commit()
        conexion.close()
    except sqlite3.Error as error:
        print("Error al borrar la reserva:", error)

# Cargar datos desde la base de datos
def cargar_datos_bandas():
    conn = sqlite3.connect("calendario.db")
    cursor = conn.cursor()

    # Obtener todos los datos de la tabla de bandas
    cursor.execute("SELECT id, banda, sala, fecha, horario, tiempo, abonado FROM reservas")
    data = cursor.fetchall()

    conn.close()
    return data

def sala_disponible(sala, fecha, hora_inicio, hora_fin):
    try:
        # Obtener el horario y el tiempo de la base de datos
        conexion = sqlite3.connect("calendario.db")
        cursor = conexion.cursor()
        cursor.execute('SELECT horario, tiempo FROM reservas WHERE sala = ? AND fecha = ?', (sala, fecha))
        datos_reserva = cursor.fetchall()
        conexion.close()

        for horario_db, tiempo_db in datos_reserva:

            print("++++++++++++: ", horario_db, tiempo_db)
            

            # Convertir las horas en formato datetime
            hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M')
            hora_fin_dt = datetime.strptime(hora_fin, '%H:%M')
            hora_inicio_db_dt = datetime.strptime(horario_db, '%H:%M')
            hora_fin_db_dt = hora_inicio_db_dt + timedelta(hours=int(tiempo_db))

            print("------------: ", hora_inicio_db_dt, hora_fin_db_dt)

            # Comprobar si hay superposición de horarios
            if (hora_inicio_dt >= hora_inicio_db_dt and hora_inicio_dt < hora_fin_db_dt) or \
               (hora_inicio_dt < hora_inicio_db_dt and hora_fin_dt > hora_inicio_db_dt):
                return False # Hay superposición con al menos una reserva
        else:
            return True  # No hay reservas previas en esa sala y fecha

    except sqlite3.Error as e:
        print("Error en la conexión o consulta SQL:", e)
        return False

def extraer_digito(tiempo):

    primer_caracter = tiempo[0]
    numero = int(primer_caracter)
    return numero