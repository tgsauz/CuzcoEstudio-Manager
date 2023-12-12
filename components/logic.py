import sqlite3
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
            id TEXT NOT NULL
        )
    ''')

    # Cerrar la conexión con la base de datos
    conexion.close()

def crear_bandas_db(ruta_base_datos_bandas):

    conexion = sqlite3.connect(ruta_base_datos_bandas)
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bandas(
            banda_id TEXT NOT NULL,
            banda_name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Miembros (
            miembro_id TEXT NOT NULL,
            id_banda_miembro TEXT NOT NULL,
            nombre TEXT NOT NULL,
            dni TEXT NOT NULL,
            celular TEXT NOT NULL,
            FOREIGN KEY (id_banda_miembro) REFERENCES Bandas(banda_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Deudas (
            id_miembro_deuda TEXT NOT NULL,
            cantidad REAL NOT NULL,
            deuda_id INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY (id_miembro_deuda) REFERENCES Miembros(miembro_id)
        )
    ''')

    conexion.commit()
    conexion.close()

def crear_consumo_db(ruta_base_datos_consumos_listado):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Consumos (
            producto TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

def guardar_consumo(ruta_base_datos_consumos_listado, producto, cantidad, precio):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO Consumos (producto, cantidad, precio)
        VALUES (?, ?, ?)
    ''', (producto, cantidad, precio))
    conexion.commit()
    conexion.close()

def recuperar_consumos(ruta_base_datos_consumos_listado):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute("SELECT producto, cantidad, precio FROM Consumos")
    data = cursor.fetchall()
    conexion.close()
    return data

def guardar_reserva(ruta_base_datos_reservas, banda, sala, fecha, horario, tiempo):

    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()
    id = str(uuid.uuid4())
    horario_str = horario.strftime("%H:%M")

    cursor.execute('''
        INSERT INTO reservas (banda, sala, fecha, horario, tiempo, id)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (banda, sala, fecha, horario_str, tiempo, id))

    conexion.commit()
    conexion.close()

def borrar_reserva_por_id(id_reserva, ruta_base_datos_reservas):

    try:
        conexion = sqlite3.connect(ruta_base_datos_reservas)
        cursor = conexion.cursor()

        # Eliminar la reserva con los valores correspondientes
        cursor.execute('''
            DELETE FROM reservas
            WHERE id = ?
        ''', (id_reserva,))

        conexion.commit()
        conexion.close()

    except sqlite3.Error as error:
        print("Error al borrar la reserva:", error)

def recuperar_datos_reservas(ruta_base_datos_reservas):
    conexion = sqlite3.connect(ruta_base_datos_reservas)
    cursor = conexion.cursor()

    # Obtener todos los datos de la tabla de bandas
    cursor.execute("SELECT banda, sala, fecha, horario, tiempo, id FROM reservas")
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

            # Convertir las horas en formato datetime
            hora_inicio_dt = datetime.strptime(hora_inicio, '%H:%M')
            hora_fin_dt = datetime.strptime(hora_fin, '%H:%M')
            hora_inicio_db_dt = datetime.strptime(horario_db, '%H:%M')
            hora_fin_db_dt = hora_inicio_db_dt + timedelta(hours=int(tiempo_db))

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