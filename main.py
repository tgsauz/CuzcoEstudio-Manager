import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from datetime import date

root = tk.Tk()
root.title('CuzcoManager')


style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")


listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]

frame = ttk.Frame(root)
frame.pack()

widgets_frame = ttk.LabelFrame(frame, text="Agregar Banda")
widgets_frame.grid(row=0, column =0, padx=20, pady=10)

#Nombre entry
name_entry = ttk.Entry(widgets_frame)
name_entry.insert(0, "Nombre de la banda")
name_entry.bind("<FocusIn>", lambda e: name_entry.delete('0', 'end'))
name_entry.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="ew")

#Sala entry
sala_combobox = ttk.Combobox(widgets_frame, values=listaSala_combo)
sala_combobox.insert(0, "Seleccionar SALA")
sala_combobox.bind("<FocusIn>", lambda e: sala_combobox.delete('0', 'end'))
sala_combobox.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")

#EstaPago? Entry
varAux = tk.BooleanVar()
checkbutton = ttk.Checkbutton(widgets_frame, text="Abonado", variable=varAux)
checkbutton.grid(row=2, column=0, padx=5, pady=(0, 5), sticky="nsew")

#Dia entry
fechaReserva = tb.DateEntry(widgets_frame)
fechaReserva.grid(row=3, column=0, padx=5, pady=(0, 5), sticky="nsew")

#Boton para insertar a calendario
botonInsACalendario = ttk.Button(widgets_frame, text="Agregar a calendario")
botonInsACalendario.grid(row=4, column=0, padx=5, pady=(0, 5),)



root.mainloop()
