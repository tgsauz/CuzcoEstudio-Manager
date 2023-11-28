import sqlite3
import os
import uuid

from datetime import datetime, timedelta

class Banda:
    def __init__(self, nombre):
        self.nombre = nombre
        self.miembros = []
        self.deudas = {}

    def agregar_miembro(self, miembro):
        self.miembros.append(miembro)

    def registrar_deuda(self, miembro, cantidad):
        self.deudas[miembro] = cantidad

    def __str__(self):
        return f"Banda: {self.nombre}, Miembros: {', '.join(self.miembros)}, Deudas: {self.deudas}"

def crear_tabla_reservas(ruta_base_datos_reservas):
    # Configurar la conexión con la base de datos SQLite
    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()

    # Crear la tabla de reservas si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            banda TEXT NOT NULL,
            sala TEXT NOT NULL,
            fecha TEXT NOT NULL,
            horario TEXT NOT NULL,
            tiempo TEXT NOT NULL,
            id TEXT PRIMARY KEY
        )
    ''')

    # Cerrar la conexión con la base de datos
    conexion.close()

def crear_bandas_db(ruta_base_datos_bandas):
    conexion = sqlite3.connect(ruta_base_datos_bandas)
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS miembros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            banda_id INTEGER,
            nombre TEXT NOT NULL,
            FOREIGN KEY (banda_id) REFERENCES bandas(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deudas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            miembro_id INTEGER,
            cantidad REAL NOT NULL,
            FOREIGN KEY (miembro_id) REFERENCES miembros(id)
        )
    ''')

    conexion.commit()   

def guardar_reserva(ruta_base_datos_reservas): #Agregar datos_a_guardar[]

    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()
    id = str(uuid.uuid4())

    cursor.execute('''
        INSERT INTO reservas (banda, sala, fecha, horario, tiempo, id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (id)) #Agregar datos_a_guardar[] = contenido de los datos

    conexion.commit()
    conexion.close()

    # Retornar el ID de la banda
    # return cursor.lastrowid

def borrar_reserva_por_datos(id, ruta_base_datos_reservas):

    try:
        conexion = sqlite3.connect(ruta_base_datos_reservas)
        cursor = conexion.cursor()

        # Eliminar la reserva con los valores correspondientes
        cursor.execute('''
            DELETE FROM reservas
            WHERE id = ?
        ''', (id))

        conexion.commit()
        conexion.close()

    except sqlite3.Error as error:
        print("Error al borrar la reserva:", error)

# Cargar datos desde la base de datos
def cargar_datos_reservas(ruta_base_datos_reservas):
    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()

    # Obtener todos los datos de la tabla de bandas
    cursor.execute("SELECT id, banda, sala, fecha, horario, tiempo FROM reservas")
    data = cursor.fetchall()

    conexion.close()
    return data

def sala_disponible(sala, fecha, hora_inicio, hora_fin, ruta_base_datos_reservas):
    try:

        conexion = sqlite3.connect(ruta_base_datos_reservas)
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