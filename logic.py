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

def borrar_reserva(id_reserva):
    try:
        # Configurar la conexión con la base de datos SQLite
        print(f"Borrando reserva con ID: {id_reserva}")
        conexion = sqlite3.connect("calendario.db")
        cursor = conexion.cursor()

        # Borrar la reserva de la base de datos
        cursor.execute('DELETE FROM reservas WHERE id = ?', (id_reserva,))

        # Guardar los cambios en la base de datos y cerrar la conexión
        conexion.commit()
        conexion.close()

    except sqlite3.Error as e:
        print("Error en la conexión o consulta SQL:", e)

# Cargar datos desde la base de datos
def cargar_datos():
    conn = sqlite3.connect("calendario.db")
    cursor = conn.cursor()

    # Obtener todos los datos de la tabla de bandas
    cursor.execute("SELECT id, banda, sala, fecha, horario, tiempo, abonado FROM reservas")
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
    ws.append(["Banda", "Sala", "Fecha", "Horario", "Tiempo", "Abonado" ])

    for fila in data:
        ws.append(fila)

    # Guardar el archivo Excel
    wb.save(archivo_excel)