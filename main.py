import tkinter as tk
from tkinter import ttk
from gui import AgendaTab, CalendarioTab, BandasTab, BarTab, WidgetStyleManager  # <--- Agrega ".gui" al inicio de la importación
import logic
import gui

listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]
interfaces_to_update = []

widget_manager = WidgetStyleManager()

def main():
    # Crear la ventana principal
    root = tk.Tk()
    root.geometry("750x500")
    root.title('CuzcoManager')

    #controller = AppController()

    style = ttk.Style(root)
    root.tk.call("source", "forest-light.tcl")
    root.tk.call("source", "forest-dark.tcl")
    style.theme_use("forest-light")
    current_theme = style

    # Crear tabla de reservas en la base de datos
    logic.crear_tabla_reservas()
    logic.crear_db_tabs

    # Crear el Notebook para las pestañas
    frame = ttk.Frame(root)
    frame.pack()
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_calendario = CalendarioTab(notebook, widget_manager)
    interfaces_to_update.append(tab_calendario)

    tab_bar = BarTab(notebook, listaSala_combo, style, widget_manager)
    interfaces_to_update.append(tab_bar)

    tab_agenda = AgendaTab(notebook, tab_bar, notebook, listaSala_combo, widget_manager)
    interfaces_to_update.append(tab_agenda)

    tab_bandas = BandasTab(notebook, widget_manager)
    interfaces_to_update.append(tab_bandas)

    notebook.add(tab_agenda, text="Agenda de bandas")
    notebook.add(tab_calendario, text="Calendario")
    notebook.add(tab_bar, text="Bar")
    notebook.add(tab_bandas, text="Bandas")

    widget_manager.add_widget(tab_agenda)
    widget_manager.add_widget(tab_bandas)
    widget_manager.add_widget(tab_bar)
    widget_manager.add_widget(tab_calendario)

    # Modo oscuro toggle
    mode_switch = ttk.Checkbutton(
        root, text="Dia/Noche", style="Switch", 
        command=lambda: gui.toggle_mode(widget_manager))
    mode_switch.place(x=640, y=7)

    # Cargar datos desde db
    tab_agenda.cargar_datos_en_listado()

    root.mainloop()

if __name__ == "__main__":
    main()