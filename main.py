import os

import sys
sys.path.append('../components/')

from components.gui.calendar import CalendarioComp
from components.logic import crear_tabla_reservas, crear_bandas_db
from components.config import set_rutas, get_rutas

import tkinter as tk
from tkinter import ttk

calendario_comp = CalendarioComp

# Crear la ventana principal
root = tk.Tk()
root.geometry("750x500")
root.title('CuzcoManager')

current_directory = os.path.dirname(os.path.abspath(__file__))
archivo_tcl_light = os.path.join(current_directory, "styles", "forest-light.tcl")
archivo_tcl_dark = os.path.join(current_directory, "styles", "forest-dark.tcl")

style = ttk.Style(root)

root.tk.call("source", (os.path.join(current_directory, "styles", "forest-dark.tcl")))

root.tk.call("source", (os.path.join(current_directory, "styles", "forest-light.tcl")))

style.theme_use("forest-light")

ruta_carpeta_data = os.path.join(current_directory, 'components', 'data')
if not os.path.exists(ruta_carpeta_data):
    os.makedirs(ruta_carpeta_data)

ruta_base_datos_reservas = os.path.join(ruta_carpeta_data, 'calendario_reservas.db')
ruta_base_datos_bandas = os.path.join(ruta_carpeta_data, 'bandas_info.db')

set_rutas(ruta_base_datos_reservas, ruta_base_datos_bandas)

crear_tabla_reservas(ruta_base_datos_reservas)
crear_bandas_db(ruta_base_datos_bandas)

calendario_frame = calendario_comp(root, style)
calendario_frame.pack(fill="both", expand=True)

root.mainloop()