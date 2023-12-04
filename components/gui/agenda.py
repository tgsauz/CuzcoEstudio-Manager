import tkinter as tk
from tkinter import ttk
from tkinter.font import Font

from ..logic import agregar_a_calendario

class AgendaWindow(tk.Toplevel):
    def __init__(self, parent, selected_date, data, style, ruta_base_datos_reservas):
        super().__init__(parent)
        self.ruta_base_datos_reservas = ruta_base_datos_reservas
        self.style = style
        self.entry_form = None
        self.title(f"Reservas del dia: {selected_date.strftime('%d-%m-%Y')}")
        
        self.selected_date = selected_date

        #TreeForm
        self.agenda_tree_frame = ttk.Frame(self)
        self.agenda_tree_frame.pack(side=tk.LEFT, fill="both", expand=True, pady=5, padx=5)

        self.agenda_tree = ttk.Treeview(self.agenda_tree_frame)
        self.agenda_tree['columns'] = ('Banda', 'Sala', 'Horario', 'HR/s')

        self.agenda_tree.heading('#0', text='ID')
        self.agenda_tree.heading('Banda', text='Banda')
        self.agenda_tree.heading('Sala', text='Sala')
        self.agenda_tree.heading('Horario', text='Horario')
        self.agenda_tree.heading('HR/s', text='HR/s')
        self.agenda_tree.pack(fill="both", expand=True)
        self.mostrar_datos_agenda(data)
        self.agenda_tree.column('#0', width=0, stretch=tk.NO)

        for col in ('Banda', 'Sala', 'Horario', 'HR/s'):
            self.agenda_tree.heading(col, text=col, anchor=tk.CENTER)
            self.agenda_tree.column(col, anchor=tk.CENTER)
            self.agenda_tree.column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="both", expand=True, pady=1, padx=1)

        #Botones
        self.entry_name = ttk.Entry(self.buttons_frame)
        self.entry_name.insert(0, 'Nombre de la banda')
        self.entry_name.bind("<FocusIn>", lambda event: self.entry_name.delete(0, "end") if self.entry_name.get() == 'Nombre de la banda' else None)
        self.entry_name.pack(pady=5, padx=5, fill='x')

        salas = ['Sala A', 'Sala B', 'Sala C', 'Sala Z', 'Estudio']
        self.sala_combobox = ttk.Combobox(self.buttons_frame, values=salas)
        self.sala_combobox.insert(0, "Seleccionar SALA")
        self.sala_combobox.pack(pady=5, padx=5, fill='x')

        horarios = []
        for hora in range(24):
            horarios.extend(["{}:00".format(str(hora).zfill(2)), "{}:30".format(str(hora).zfill(2))])
        self.hour_spinbox = ttk.Spinbox(self.buttons_frame, values=horarios)
        self.hour_spinbox.insert(0, "Horario")  # Texto de ejemplo en el Entry
        self.hour_spinbox.pack(pady=5, padx=5, fill='x')

        self.time_combobox = ttk.Combobox(self.buttons_frame, values=["1 hora", "2 horas", "3 horas", "4 horas"])
        self.time_combobox.insert(0, "Seleccionar tiempo")
        self.time_combobox.pack(pady=5, padx=5, fill='x')

        self.button_add_entry = ttk.Button(self.buttons_frame, command=lambda: agregar_a_calendario(self, ruta_base_datos_reservas))
        self.button_add_entry.config(text='Agregar entrada')
        self.button_add_entry.pack(pady=5, padx=5, fill='x')

        self.separator_horizontal = ttk.Separator(self.buttons_frame, orient='horizontal', style='Horizontal.TSeparator')
        self.separator_horizontal.pack(pady=10, padx=5, fill='x')

        self.button_remove_entry = ttk.Button(self.buttons_frame)
        self.button_remove_entry.config(text='Eliminar entrada')
        self.button_remove_entry.pack(pady=5, padx=5, fill='x')

    def mostrar_datos_agenda(self, data):
        print(data)
        for index, entrada in enumerate(data, start=1):
            self.agenda_tree.insert('', 'end', text=str(index), values=entrada[0:5])
    
    def aplicar_grab_set(self):
        self.grab_set()
        self.focus_set()