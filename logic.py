import sqlite3
from datetime import datetime
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
            sala TEXT NOT NULL,
            banda TEXT NOT NULL,
            fecha TEXT NOT NULL,
            horario TEXT NOT NULL,
            tiempo TEXT NOT NULL,
            abonado TEXT NOT NULL
        )
    ''')

    # Cerrar la conexión con la base de datos
    conexion.close()

def guardar_reserva(banda, sala, fecha, horario, tiempo, abonado):
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect("calendario.db")
    cursor = conexion.cursor()

    # Insertar la reserva en la base de datos
    cursor.execute('''
        INSERT INTO reservas (banda, sala, fecha, horario, tiempo, abonado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (banda, sala, fecha, horario, tiempo, abonado))

    # Obtener el ID de la banda recién insertada
    id_banda = cursor.lastrowid

    # Guardar los cambios en la base de datos y cerrar la conexión
    conexion.commit()
    conexion.close()

    # Retornar el ID de la banda
    return id_banda

def obtener_todas_reservas():
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect("calendario.db")
    cursor = conexion.cursor()

    # Obtener todas las reservas de la base de datos
    cursor.execute('SELECT * FROM reservas')
    reservas = cursor.fetchall()

    # Cerrar la conexión con la base de datos
    conexion.close()

    return reservas

def borrar_reserva(id_reserva):
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect("calendario.db")
    cursor = conexion.cursor()

    # Borrar la reserva de la base de datos
    cursor.execute('DELETE FROM reservas WHERE id = ?', (id_reserva,))

    # Guardar los cambios en la base de datos y cerrar la conexión
    conexion.commit()
    conexion.close()

# Función para guardar los datos en la base de datos
def guardar_en_db(banda, sala, abonado, fecha, horario, tiempo):
    conn = sqlite3.connect("calendario.db")
    cursor = conn.cursor()

    # Insertar los datos en la tabla de reservas
    cursor.execute("INSERT INTO reservas (banda, sala, fecha, horario, tiempo, abonado) VALUES (?, ?, ?, ?, ?, ?)",
                   (banda, sala, fecha, horario, tiempo, abonado))

    conn.commit()
    conn.close()

# Cargar datos desde la base de datos
def cargar_datos():
    conn = sqlite3.connect("calendario.db")
    cursor = conn.cursor()

    # Obtener todos los datos de la tabla de bandas
    cursor.execute("SELECT banda, sala, abonado, fecha, horario, tiempo FROM reservas")
    data = cursor.fetchall()

    conn.close()
    return data

# Validar la fecha ingresada
def validar_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False
    
def exportar_a_excel(archivo_excel):
    # Obtener los datos desde la base de datos
    data = cargar_datos()

    if not data:
        return

    if not archivo_excel.endswith('.xlsx'):
        archivo_excel += '.xlsx'

    # Crear el archivo Excel y agregar los datos
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Banda", "Sala", "Abonado", "Fecha", "Horario", "Tiempo"])

    for fila in data:
        ws.append(fila)

    # Guardar el archivo Excel
    wb.save(archivo_excel)