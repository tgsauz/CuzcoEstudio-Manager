import sqlite3
import os
import uuid

from datetime import date, datetime, timedelta
from tkinter import messagebox

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
            banda_id INTEGER,
            nombre TEXT NOT NULL,
            FOREIGN KEY (banda_id) REFERENCES bandas(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deudas (
            miembro_id INTEGER,
            cantidad REAL NOT NULL,
            FOREIGN KEY (miembro_id) REFERENCES miembros(id)
        )
    ''')

    conexion.commit()   

def guardar_reserva(ruta_base_datos_reservas, banda, sala, fecha, horario, tiempo): #Agregar datos_a_guardar[]

    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()
    id = str(uuid.uuid4())

    cursor.execute('''
        INSERT INTO reservas (banda, sala, fecha, horario, tiempo, id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (banda, sala, fecha, horario, tiempo, id)) #Agregar datos_a_guardar[] = contenido de los datos

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
    cursor.execute("SELECT banda, sala, fecha, horario, tiempo FROM reservas")
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
    return int(tiempo[0])

##
def agregar_a_calendario(self, ruta_base_datos_reservas):
    # Obtener los datos ingresados en los widgets
    banda = self.entry_name.get()
    sala = self.sala_combobox.get()
    fecha = self.selected_date
    horario = self.hour_spinbox.get()
    tiempo = self.time_combobox.get()

    # Validar que el nombre de la banda y la sala hayan sido ingresados
    if not banda or banda == "Nombre de la banda":
        messagebox.showerror("Error", "Por favor, ingresa el nombre de la banda.")
        return

    if not sala or sala == "Seleccionar SALA":
        messagebox.showerror("Error", "Por favor, selecciona una sala.")
        return

    if not horario or horario == "Horario":
        messagebox.showerror("Error", "Por favor, ingresa un horario.")
        return

    if not tiempo or tiempo == "Seleccionar tiempo":
        messagebox.showerror("Error", "Por favor, selecciona un tiempo.")
        return

    # Obtener las horas y minutos del tiempo seleccionado
    if "horas" in tiempo:
        tiempo = tiempo.replace(' horas', '')
    else:
        tiempo = tiempo.replace(' hora', '')

    # Calcular el horario de fin de la reserva
    digitoAux = extraer_digito(tiempo)
    minutos = digitoAux * 60
    hora_inicio_reserva = datetime.strptime(horario, "%H:%M")
    hora_fin_reserva = hora_inicio_reserva + timedelta(minutes=minutos)

    print("Pre DEF, FIN RESERVA: ", hora_fin_reserva, "INI RESERVA: ", hora_inicio_reserva)

    # Validar si la sala está disponible en el horario seleccionado
    if sala_disponible(sala, fecha, hora_inicio_reserva.strftime("%H:%M"), hora_fin_reserva.strftime("%H:%M"), ruta_base_datos_reservas):
        # Guardar los datos en el hoja de cálculo
        guardar_reserva(ruta_base_datos_reservas, banda, sala, fecha, horario, tiempo)

        # Finalmente, limpiar los widgets para el siguiente ingreso
        self.entry_name.delete(0, "end")
        self.sala_combobox.set("Seleccionar SALA")
        self.hour_spinbox.delete(0, "end")
        self.time_combobox.set("Seleccionar tiempo")  # Limpiar el combobox de tiempo

        # Después de agregar la entrada, cargar nuevamente los datos para actualizar el widget de lista
        self.cargar_datos_en_listado()

    else:
        messagebox.showerror("Error", "La sala no está disponible en el horario seleccionado.")