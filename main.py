import tkinter as tk
from tkinter import ttk
import tkcalendar
import locale
from datetime import date
import os
import openpyxl
from openpyxl.utils import get_column_letter

locale.setlocale(locale.LC_ALL, 'es_ES')

#Agregar datos al calendario
def agregar_a_calendario():
    # Obtener los datos ingresados en los widgets
    banda = name_entry.get()
    sala = sala_combobox.get()
    abonado = varAux.get()
    fecha = fechaReserva.get_date()

    if varAux.get():
        abonado = "Sí"
    else:
        abonado = "No"

    # Validar que todos los campos estén completos antes de agregar a la tabla
    if banda and sala and fecha:
        lista.insert("", "end", values=(banda, sala, abonado, fecha))
        
        # Guardar los datos en la hoja de cálculo
        guardar_en_excel(banda, sala, abonado, fecha)

        # Finalmente, limpiar los widgets para el siguiente ingreso
        name_entry.delete(0, "end")
        sala_combobox.set("Seleccionar SALA")
        varAux.set(False)
        fechaReserva.set_date(date.today())

    else:
        # Mostrar un mensaje de error si falta algún campo
        tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")

#Modo oscuro toggle
def toggle_mode():
    if mode_switch.instate(["selected"]):
        style.theme_use("forest-light")
    else:
        style.theme_use("forest-dark")

    root.update()

#Guardar archivo en excell
def guardar_en_excel(banda, sala, abonado, fecha):
    archivo_excel = "calendario_bandas.xlsx"

    if not os.path.exists(archivo_excel):
        # Si el archivo no existe, creamos uno nuevo con las cabeceras
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Banda", "Sala", "Abonado", "Fecha"])
    else:
        # Si el archivo ya existe, abrimos el archivo existente
        wb = openpyxl.load_workbook(archivo_excel)
        ws = wb.active

    # Agregar una nueva fila con los datos
    nueva_fila = [banda, sala, abonado, fecha]
    ws.append(nueva_fila)

    # Guardar los cambios en el archivo
    wb.save(archivo_excel)

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
fechaReserva = tkcalendar.DateEntry(widgets_frame, locale='es_ES')
fechaReserva.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew")

#Boton para insertar a calendario
botonInsACalendario = ttk.Button(widgets_frame, text="Agregar a calendario", command=agregar_a_calendario)
botonInsACalendario.grid(row=4, column=0, padx=5, pady=(0, 5))

#Calendario

treeFrame = ttk.Frame(frame)
treeFrame.grid(row=0, column=1, pady=10)
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

cols = ("Banda", "Sala", "Abonado", "Fecha")
lista = ttk.Treeview(treeFrame, show="headings",
                        yscrollcommand=treeScroll.set, columns=cols, height=13)

# Configurar los encabezados de las columnas
lista.heading("Banda", text="Banda")
lista.heading("Sala", text="Sala")
lista.heading("Abonado", text="Abonado")
lista.heading("Fecha", text="Fecha")

lista.column("Banda", width=100)
lista.column("Sala", width=100)
lista.column("Abonado", width=100)
lista.column("Fecha", width=100)
lista.pack()
treeScroll.config(command=lista.yview)

#Separador
separator = ttk.Separator(widgets_frame)
separator.grid(row=5, column=0, padx=(20, 10), pady=10, sticky="ew")

#ModoGui
mode_switch = ttk.Checkbutton(
    widgets_frame, text="Dia/Noche", style="Switch", command=toggle_mode)
mode_switch.grid(row=6, column=0, padx=5, pady=10, sticky="nsew")

#CargadodeDatos


root.mainloop()
