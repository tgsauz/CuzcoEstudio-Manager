import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkcalendar
import locale
from datetime import date, datetime, timedelta
import os
import openpyxl
from openpyxl.utils import get_column_letter

locale.setlocale(locale.LC_ALL, 'es_ES')

def get_available_time_slots():
    current_time = datetime.now()
    end_of_day = current_time.replace(hour=23, minute=59)

    time_slots = []
    while current_time < end_of_day:
        time_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=30)

        # Saltar al próximo horario en punto si no está ya en punto
        if current_time.minute != 0:
            current_time += timedelta(minutes=(60 - current_time.minute))

    return time_slots

# Agregar datos al calendario
def agregar_a_calendario():
    # Obtener los datos ingresados en los widgets
    banda = name_entry.get()
    sala = sala_combobox.get()
    abonado = varAux.get()
    fecha = fechaReserva.get_date()
    horario = hora_entry.get()  # Obtener el horario ingresado por el usuario

    if varAux.get():
        abonado = "Sí"
    else:
        abonado = "No"

    # Validar que el nombre de la banda y la sala hayan sido ingresados
    if not banda or banda == "Nombre de la banda":
        tk.messagebox.showerror("Error", "Por favor, ingresa el nombre de la banda.")
        return

    if sala == "Seleccionar SALA":
        tk.messagebox.showerror("Error", "Por favor, selecciona una sala.")
        return
    
    if not horario or horario == "Horario":
        tk.messagebox.showerror("Error", "Por favor, ingrese un horario.")
        return

    # Validar que todos los campos estén completos antes de agregar a la tabla
    if banda and sala and fecha and horario:
        lista.insert("", "end", values=(banda, sala, abonado, fecha, horario))

        # Guardar los datos en la hoja de cálculo
        guardar_en_excel(banda, sala, abonado, fecha, horario)

        # Finalmente, limpiar los widgets para el siguiente ingreso
        name_entry.delete(0, "end")
        sala_combobox.set("Seleccionar SALA")
        varAux.set(False)
        fechaReserva.set_date(date.today())
        hora_entry.delete(0, "end")  # Limpiar el Entry de horario

    else:
        # Mostrar un mensaje de error si falta algún campo (aunque las validaciones anteriores ya deberían cubrir esto)
        tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")

# Modo oscuro toggle
def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-dark")
    else:
        style.theme_use("forest-light")

    root.update()

# Guardar archivo en Excel
def guardar_en_excel(banda, sala, abonado, fecha, horario):
    archivo_excel = "calendario_bandas.xlsx"

    if not os.path.exists(archivo_excel):
        # Si el archivo no existe, creamos uno nuevo con las cabeceras
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Banda", "Sala", "Abonado", "Fecha", "Horario"])
    else:
        # Si el archivo ya existe, abrimos el archivo existente
        wb = openpyxl.load_workbook(archivo_excel)
        ws = wb.active

    # Agregar una nueva fila con los datos
    nueva_fila = [banda, sala, abonado, fecha, horario]
    ws.append(nueva_fila)

    # Guardar los cambios en el archivo
    wb.save(archivo_excel)

# Función para cargar datos desde el archivo Excel y mostrarlos en el widget de listado
def cargar_datos_en_listado():
    archivo_excel = "calendario_bandas.xlsx"

    if not os.path.exists(archivo_excel):
        # Si el archivo no existe, no hay datos para cargar
        return []

    # Abrir el archivo Excel y obtener la hoja activa
    wb = openpyxl.load_workbook(archivo_excel)
    ws = wb.active

    # Leer los datos de cada fila y almacenarlos en una lista
    data = []
    for row in ws.iter_rows(values_only=True):
        banda, sala, abonado, fecha, horario = row
        data.append((banda, sala, abonado, fecha, horario))

    # Limpiar el contenido actual del widget de listado
    lista.delete(*lista.get_children())

    # Insertar los datos en el widget de listado
    for row in data:
        lista.insert("", "end", values=row)

root = tk.Tk()
root.title('CuzcoManager')


style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-light")


listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Agendar Banda")
widgets_frame.grid(row=0, column =0, padx=20, pady=10)

#Nombre entry
name_entry = ttk.Entry(widgets_frame)
name_entry.insert(0, "Nombre de la banda")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

#Sala entry
sala_combobox = ttk.Combobox(widgets_frame, values=listaSala_combo)
sala_combobox.insert(0, "Seleccionar SALA")
#sala_combobox.bind("<FocusIn>", lambda e: sala_combobox.delete('0', 'end'))
sala_combobox.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

#EstaPago? Entry
varAux = tk.BooleanVar()
checkbutton = ttk.Checkbutton(widgets_frame, text="Abonado", variable=varAux)
checkbutton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

#Dia entry
fechaReserva = tkcalendar.DateEntry(widgets_frame, locale='es_ES', date_pattern='dd/MM/yyyy')
fechaReserva.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew")

#Widget Horario
hora_entry = ttk.Entry(widgets_frame)
hora_entry.insert(0, "Horario")  # Texto de ejemplo en el Entry
hora_entry.bind("<FocusIn>", lambda e: hora_entry.delete('0', 'end'))
hora_entry.grid(row=4, column=0, padx=5, pady=(0, 5), sticky="ew")

#Boton para insertar a calendario
botonInsACalendario = ttk.Button(widgets_frame, text="Agregar a calendario", command=agregar_a_calendario)
botonInsACalendario.grid(row=5, column=0, padx=5, pady=(0, 5))

#Calendario

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Banda", "Sala", "Abonado", "Fecha", "Horario")
lista = ttk.Treeview(treeFrame, show="headings",
                        yscrollcommand=treeScroll.set, columns=cols, height=13)

# Configurar los encabezados de las columnas
lista.heading("Banda", text="Banda")
lista.heading("Sala", text="Sala")
lista.heading("Abonado", text="Abonado")
lista.heading("Fecha", text="Fecha")
lista.heading("Horario", text="Horario")

lista.column("Banda", width=100)
lista.column("Sala", width=100)
lista.column("Abonado", width=50)
lista.column("Fecha", width=100)
lista.column("Horario", width=50)
lista.pack()
treeScroll.config(command=lista.yview)

#Separador
separator = ttk.Separator(widgets_frame)
separator.grid(row=6, column=0, padx=(20, 10), pady=10, sticky="ew")

#ModoGui
mode_switch = ttk.Checkbutton(
    widgets_frame, text="Dia/Noche", style="Switch", command=toggle_mode)
mode_switch.grid(row=7, column=0, padx=5, pady=10, sticky="nsew")

#CargadodeDatos
cargar_datos_en_listado()

root.mainloop()
