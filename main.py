import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openpyxl
import os
from datetime import date
from tkcalendar import Calendar
from gui import AgendaTab  # <--- Agrega ".gui" al inicio de la importación
import logic

tab_agenda = None

# Función para cargar datos desde el archivo Excel y mostrarlos en el widget de listado
def cargar_datos_en_listado(tab_agenda):
    data = logic.cargar_datos()
    tab_agenda.cargar_datos_en_listado()

# Función para guardar los datos ingresados por el usuario en el archivo Excel
def guardar_datos_en_excel(banda, sala, abonado, fecha, horario, tiempo):
    logic.guardar_en_excel(banda, sala, abonado, fecha, horario, tiempo)

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("750x475")
    root.title('CuzcoManager')

    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-light")

    # Crear tabla de reservas en la base de datos
    logic.crear_tabla_reservas()

    # Crear el Notebook para las pestañas
    frame = ttk.Frame(root)
    frame.pack()
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Pestaña Actual
    tab_agenda = AgendaTab(notebook)
    notebook.add(tab_agenda, text="Agenda de bandas")

    # Pestaña Otras Datos
    tab_datos = ttk.Frame(notebook)
    notebook.add(tab_datos, text="Otros Datos")

    # Cargar datos desde el archivo Excel y mostrarlos en el widget de listado
    cargar_datos_en_listado(tab_agenda)

    root.mainloop()

if __name__ == "__main__":
    main()