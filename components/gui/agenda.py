from datetime import datetime, timedelta

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

from ..logic import extraer_digito, sala_disponible, guardar_reserva, recuperar_datos_reservas, borrar_reserva_por_id

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
        self.agenda_tree_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.agenda_tree = ttk.Treeview(self.agenda_tree_frame)
        self.agenda_tree['columns'] = ('Banda', 'Sala', 'Horario', 'HR/s')

        self.agenda_tree.heading('#0', text='ID')
        self.agenda_tree.heading('Banda', text='Banda')
        self.agenda_tree.heading('Sala', text='Sala')
        self.agenda_tree.heading('Horario', text='Horario')
        self.agenda_tree.heading('HR/s', text='HR/s')
        self.agenda_tree.pack(fill="both", expand=True)
        self.mostrar_datos_agenda(data, selected_date)
        self.agenda_tree.column('#0', width=0, stretch=tk.NO)

        for col in ('Banda', 'Sala', 'Horario', 'HR/s'):
            self.agenda_tree.heading(col, text=col, anchor=tk.CENTER)
            self.agenda_tree.column(col, anchor=tk.CENTER)
            self.agenda_tree.column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        self.buttons_frame = ttk.Frame(self)
        self.buttons_frame.pack(fill="both", expand=True)

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

        self.button_add_entry = ttk.Button(self.buttons_frame, command=lambda: self.agregar_a_calendario(ruta_base_datos_reservas))
        self.button_add_entry.config(text='Agregar entrada')
        self.button_add_entry.pack(pady=5, padx=5, fill='x')

        self.separator_horizontal = ttk.Separator(self.buttons_frame, orient='horizontal')
        self.separator_horizontal.pack(pady=10, padx=5, fill='x')

        self.button_remove_entry = ttk.Button(self.buttons_frame, command=lambda: self.borrar_seleccionados(ruta_base_datos_reservas))
        self.button_remove_entry.config(text='Eliminar entrada')
        self.button_remove_entry.pack(pady=5, padx=5, fill='x')
    
    def agregar_a_calendario(self, ruta_base_datos_reservas):
        # Obtener los datos ingresados en los widgets
        banda = self.entry_name.get()
        sala = self.sala_combobox.get()
        fecha = self.selected_date
        horario = self.hour_spinbox.get()
        tiempo = self.time_combobox.get()

        # Validar que el nombre de la banda y la sala hayan sido ingresados
        if not banda or banda == "Nombre de la banda":
            messagebox.showerror("Error", "Por favor, ingresa el nombre de la banda.")
            return

        if not sala or sala == "Seleccionar SALA":
            messagebox.showerror("Error", "Por favor, selecciona una sala.")
            return

        if not horario or horario == "Horario":
            messagebox.showerror("Error", "Por favor, ingresa un horario.")
            return

        if not tiempo or tiempo == "Seleccionar tiempo":
            messagebox.showerror("Error", "Por favor, selecciona un tiempo.")
            return

        # Obtener las horas y minutos del tiempo seleccionado
        if "horas" in tiempo:
            tiempo = tiempo.replace(' horas', '')
        else:
            tiempo = tiempo.replace(' hora', '')

        # Calcular el horario de fin de la reserva
        digitoAux = extraer_digito(tiempo)
        minutos = digitoAux * 60
        hora_inicio_reserva = datetime.strptime(horario, "%H:%M")
        hora_fin_reserva = hora_inicio_reserva + timedelta(minutes=minutos)

        # Validar si la sala está disponible en el horario seleccionado
        if sala_disponible(sala, fecha, hora_inicio_reserva.strftime("%H:%M"), hora_fin_reserva.strftime("%H:%M"), ruta_base_datos_reservas):
            # Guardar los datos en el hoja de cálculo
            guardar_reserva(ruta_base_datos_reservas, banda, sala, fecha, hora_inicio_reserva, tiempo) #Problema con el almacenamiento del horario, sale como fecha

            # Finalmente, limpiar los widgets para el siguiente ingreso
            self.entry_name.delete(0, "end")
            self.sala_combobox.set("Seleccionar SALA")
            self.hour_spinbox.delete(0, "end")
            self.time_combobox.set("Seleccionar tiempo")  # Limpiar el combobox de tiempo

            # Después de agregar la entrada, cargar nuevamente los datos para actualizar el widget de lista
            self.mostrar_datos_agenda(recuperar_datos_reservas(ruta_base_datos_reservas), self.selected_date)

        else:
            messagebox.showerror("Error", "La sala no está disponible en el horario seleccionado.")
        
    def mostrar_datos_agenda(self, data, selected_date):
        self.agenda_tree.delete(*self.agenda_tree.get_children())

        matching_entries = [tupla for tupla in data if tupla[2] == (selected_date.strftime("%Y-%m-%d"))]
        
        for index, entrada in enumerate(matching_entries, start=1):
            values_to_insert = entrada[0:2] + entrada[3:6]
            self.agenda_tree.insert('', 'end', text=str(index), values=values_to_insert)
    
    def aplicar_grab_set(self):
        self.grab_set()
        self.focus_set()

    def borrar_seleccionados(self, ruta_base_datos_reservas):
        selected_items = self.agenda_tree.selection()
        if not selected_items:
            messagebox.showinfo("Advertencia", "Por favor, selecciona al menos una entrada para borrar.")
            return

        # Preguntar al usuario si realmente quiere borrar las entradas seleccionadas
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar las entradas seleccionadas?")
        if not confirmacion:
            return

        # Eliminar las reservas seleccionadas del TreeView y de la base de datos
        for item in selected_items:
            id_reserva = self.agenda_tree.item(item, 'values')[-1]
            print(id_reserva)
            
            self.agenda_tree.delete(item)  # Eliminar del TreeView
            borrar_reserva_por_id(id_reserva, ruta_base_datos_reservas)  # Eliminar de la base de datos