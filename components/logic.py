import sqlite3
import uuid

from datetime import datetime, timedelta

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
            precio INTEGER NOT NULL,
            id INTEGER PRIMARY KEY AUTOINCREMENT
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

def borrar_consumo(ruta_base_datos_consumos_listado, valores):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM Consumos WHERE producto = ?", (valores[0],))
    conexion.commit()
    conexion.close()

    #Hay que agregar esta funcion a ConsummosWindow
    #IMPORTANTE
    #Es necesario que en caso de q haya 2 productos con el mismo nombre, borre el consumo seleccionado y no otro random

def recuperar_consumos(ruta_base_datos_consumos_listado):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute("SELECT producto, cantidad, precio FROM Consumos")
    data = cursor.fetchall()
    conexion.close()
    return data

def encontrar_consumo(ruta_base_datos_consumos_listado, producto, cantidad, precio):
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    cursor.execute("SELECT producto, cantidad, precio FROM Consumos WHERE producto = ?, cantidad = ?, precio = ?", (producto, cantidad, precio))
    data = cursor.fetchone()
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

def agregar_consumo_gasto(ruta_base_datos_consumos_listado, producto_name, cantidad):

    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()
    
    try:
        cursor.execute("SELECT producto, id FROM Consumos WHERE producto = ?", (producto_name,))
        resultado = cursor.fetchone()
        if not resultado[0]:
            error = f"El producto {producto_name} no existe en la base de datos."
            return error
        if not resultado[1] or resultado[1] == 0:
            error = f"No se posee stock del producto {producto_name} en la base de datos."
            return error
        
        cursor.execute("UPDATE Consumos SET cantidad = cantidad - ? WHERE id = ?", (cantidad, resultado[1]))
        conexion.commit()


    except Exception as e:
        print(f"Error al agregar el consumo: {e}")

    finally:
        conexion.close()

def sustraer_consumo_gasto(ruta_base_datos_consumos_listado, valores):


    print(valores)
    # Conectar a la base de datos
    conexion = sqlite3.connect(ruta_base_datos_consumos_listado)
    cursor = conexion.cursor()

    try:
        # Obtener el ID del consumo seleccionado
        cursor.execute("SELECT id FROM Consumos WHERE producto = ?", (valores[0],))
        resultado = cursor.fetchone()
        if not resultado:
            error = f"El producto {valores[0]} no existe en la base de datos."
            return error

        consumo_id = resultado[0]

        # Actualizar la cantidad en la base de datos
        cursor.execute("UPDATE Consumos SET cantidad = cantidad + ? WHERE id = ?", (valores[1], consumo_id))
        conexion.commit()

    except Exception as e:
        print(f"Error al eliminar el consumo: {e}")
        return 0

    finally:
        conexion.close()
        return 1
