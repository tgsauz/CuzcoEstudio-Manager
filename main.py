import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import openpyxl
import os
from datetime import date
from tkcalendar import Calendar
from gui import AgendaTab, CalendarioTab, BandasTab, BarTab  # <--- Agrega ".gui" al inicio de la importación
import logic

listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]

#class AppController:
#    def __init__(self):
#        self.frames = {}
#
#    def add_frame(self, frame_name, frame_instance):
#        self.frames[frame_name] = frame_instance
#
#    def show_frame(self, frame_name):
#        frame = self.frames.get(frame_name)
#        if frame:
#            frame.tkraise()



def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("750x475")
    root.title('CuzcoManager')

    #controller = AppController()

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

    tab_calendario = CalendarioTab(notebook)
    tab_bar = BarTab(notebook, listaSala_combo)
    tab_agenda = AgendaTab(notebook, tab_bar, notebook, listaSala_combo)
    tab_bandas = BandasTab(notebook)

    tab_bar.configure(bg="white")

    tab_agenda.tab_bar_instance = tab_bar

    notebook.add(tab_agenda, text="Agenda de bandas")
    notebook.add(tab_calendario, text="Calendario")
    notebook.add(tab_bar, text="Bar")
    notebook.add(tab_bandas, text="Bandas")

    # Modo oscuro toggle
    style = ttk.Style(frame)
    mode_switch = ttk.Checkbutton(
        root, text="Dia/Noche", style="Switch",
        command=lambda: logic.toggle_mode(mode_switch, style, tab_bar))
    mode_switch.place(x=640, y=7)

    # Cargar datos desde db
    tab_agenda.cargar_datos_en_listado()

    root.mainloop()

if __name__ == "__main__":
    main()