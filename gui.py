import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
import openpyxl
import os
from datetime import date
from tkcalendar import Calendar
import logic

listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]

class AgendaTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.data = []  # Variable para almacenar los datos cargados desde el archivo Excel

        self.parent = parent
        self.create_widgets()

        # Conectar a la base de datos SQLite
        logic.crear_tabla_reservas()

    def create_widgets(self):

        # Nombre de la banda
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, "Nombre de la banda")
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.delete('0', 'end'))
        self.name_entry.place(x=10, y=10, width=190)

        # Sala
        self.sala_combobox = ttk.Combobox(self, values=listaSala_combo)
        self.sala_combobox.insert(0, "Seleccionar SALA")
        self.sala_combobox.place(x=10, y=50, width=190)

        # Fecha
        self.fechaReserva = tkcalendar.DateEntry(self, locale='es_ES', date_pattern='dd/MM/yyyy')
        self.fechaReserva.place(x=10, y=90, width=190)

        # Horario
        self.hora_entry = ttk.Entry(self)
        self.hora_entry.insert(0, "Horario")  # Texto de ejemplo en el Entry
        self.hora_entry.bind("<FocusIn>", lambda e: self.hora_entry.delete('0', 'end'))
        self.hora_entry.place(x=10, y=130, width=190)

        # Tiempo
        self.tiempo_combobox = ttk.Combobox(self, values=["1 hora", "2 horas", "3 horas", "4 horas"])
        self.tiempo_combobox.insert(0, "Seleccionar tiempo")
        self.tiempo_combobox.place(x=10, y=170, width=190)

        # Abonado
        self.varAux = tk.BooleanVar()
        checkbutton = ttk.Checkbutton(self, text="Abonado", variable=self.varAux)
        checkbutton.place(x=10, y=210)

        # Botón para insertar a calendario
        self.boton_agregar = ttk.Button(self, text="Agregar a calendario", command=self.agregar_a_calendario)
        self.boton_agregar.place(x=10, y=250, width=190)

        #Separador1
        separator1 = ttk.Separator(self)
        separator1.place(x=10, y=290, width=190)

        # Modo oscuro toggle
        self.style = ttk.Style(self)
        self.mode_switch = ttk.Checkbutton(
            self, text="Dia/Noche", style="Switch", command=self.toggle_mode)
        self.mode_switch.place(x=50, y=320)

        #Separador2
        separator2 = ttk.Separator(self)
        separator2.place(x=10, y=370, width=190)

        # Botón para borrar entradas seleccionadas
        self.boton_borrar = ttk.Button(self, text="Borrar seleccionados", command=self.borrar_seleccionados)
        self.boton_borrar.place(x=10, y=380, width=190)

        # Separador vertical usando Canvas
        canvas = tk.Canvas(self, width=1, height=402, bg="#CCCCCC", highlightthickness=0)
        canvas.place(x=220, y=10)

        # Frame para el treeview
        treeFrame = ttk.Frame(self)
        treeFrame.place(x=240, y=10, width=470, height=402)

        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")
        treeFrame.columnconfigure(0, weight=1)

        # Frame para el TreeView
        cols = ("ID","Banda", "Sala", "Fecha", "Horario", "Tiempo", "Abonado")
        self.lista = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        # Configurar los encabezados de las columnas
        self.lista.heading("Banda", text="Banda")
        self.lista.heading("Sala", text="Sala")
        self.lista.heading("Abonado", text="Abonado")
        self.lista.heading("Fecha", text="Fecha")
        self.lista.heading("Horario", text="Horario")
        self.lista.heading("Tiempo", text="Tiempo")

        self.lista.column("ID", width=0, anchor = "center", stretch=False)
        self.lista.column("Banda", width=120, anchor = "center", stretch=False)
        self.lista.column("Sala", width=100, anchor = "center", stretch=False)
        self.lista.column("Abonado", width=55, anchor = "center", stretch=False)
        self.lista.column("Fecha", width=75, anchor = "center", stretch=False)
        self.lista.column("Horario", width=50, anchor = "center", stretch=False)
        self.lista.column("Tiempo", width=50, anchor = "center", stretch=False)

        treeScroll.config(command=self.lista.yview)
        self.lista.pack(expand=True, fill="both")

        # Cargar datos al TreeView
        self.cargar_datos_en_listado()

    def agregar_a_calendario(self):
        # Obtener los datos ingresados en los widgets
        banda = self.name_entry.get()
        sala = self.sala_combobox.get()
        abonado = "Si" if self.varAux.get() else "No"
        fecha = self.fechaReserva.get_date()
        horario = self.hora_entry.get()
        tiempo = self.tiempo_combobox.get()

        # Validar que el nombre de la banda y la sala hayan sido ingresados
        if not banda:
            messagebox.showerror("Error", "Por favor, ingresa el nombre de la banda.")
            return

        if not sala:
            messagebox.showerror("Error", "Por favor, selecciona una sala.")
            return

        if not horario:
            messagebox.showerror("Error", "Por favor, ingresa un horario.")
            return

        if not tiempo:
            messagebox.showerror("Error", "Por favor, selecciona un tiempo.")
            return

        # Validar que todos los campos estén completos antes de agregar a la tabla
        if banda and sala and fecha and horario and tiempo:
            self.lista.insert("", "end", values=(banda, sala, fecha, horario, tiempo, abonado))

            # Guardar los datos en el hoja de cálculo
            id_banda = logic.guardar_reserva(sala, banda, fecha, horario, tiempo, abonado)

                # Insertar la reserva en el Treeview y mostrar el ID de la banda
            self.tree.insert("", "end", values=(id_banda, banda, sala, fecha, horario, tiempo, abonado))    

            # Finalmente, limpiar los widgets para el siguiente ingreso
            self.name_entry.delete(0, "end")
            self.sala_combobox.set("Seleccionar sala")
            self.varAux.set(False)
            self.fechaReserva.set_date(date.today())
            self.hora_entry.delete(0, "end")
            self.tiempo_combobox.set("Tiempo")  # Limpiar el combobox de tiempo

            # Después de agregar la entrada, cargar nuevamente los datos para actualizar el widget de lista
            self.cargar_datos_en_listado()

        else:
            # Mostrar un mensaje de error si falta algún campo
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def borrar_seleccionados(self):
        selected_items = self.lista.selection()
        if not selected_items:
            messagebox.showinfo("Advertencia", "Por favor, selecciona al menos una entrada para borrar.")
            return

        # Preguntar al usuario si realmente quiere borrar las entradas seleccionadas
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar las entradas seleccionadas?")
        if not confirmacion:
            return

        # Obtener las filas seleccionadas del TreeView
        selected_ids = [self.lista.item(item, 'values')[0] for item in selected_items]

        # Eliminar las filas seleccionadas del TreeView
        for item in selected_items:
            self.lista.delete(item)

        # Eliminar las filas correspondientes de la lista self.data
        self.data = [row for row in self.data if list(row) not in selected_ids]

        # Eliminar las reservas seleccionadas de la base de datos
        for id_reserva in selected_ids:
            logic.borrar_reserva(id_reserva)

    # Modo oscuro toggle
    def toggle_mode(self):
        if self.mode_switch.instate(["selected"]):
            self.style.theme_use("forest-dark")
        else:
            self.style.theme_use("forest-light")

    def cargar_datos_en_listado(self):
        data = logic.obtener_todas_reservas()
        for item in self.lista.get_children():
            self.lista.delete(item)
        # Insertamos los nuevos datos en el TreeView
        for row in data:
            print(row) # IMPORTANTE PARA TESTEAR
            self.lista.insert("", "end", values=row)

