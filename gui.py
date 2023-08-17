import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import tkcalendar
import openpyxl
import os
from datetime import date, datetime, timedelta
from tkcalendar import Calendar, DateEntry
import logic
from logic import borrar_tab_actual_db
import sqlite3

consumos = {}

class AgendaTab(ttk.Frame):
    def __init__(self, master, tab_bar_instance, notebook, salas):
        super().__init__(master)
        self.tab_bar_instance = tab_bar_instance
        self.notebook = notebook
        self.data = []  # Variable para almacenar los datos cargados desde el archivo Excel

        self.master = master
        self.create_widgets(salas)

        # Conectar a la base de datos SQLite
        logic.crear_tabla_reservas()

    def create_widgets(self, salas):

        # Nombre de la banda
        self.name_entry = ttk.Entry(self)
        self.name_entry.insert(0, "Nombre de la banda")
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.delete('0', 'end'))
        self.name_entry.place(x=10, y=10, width=190)

        # Sala
        self.sala_combobox = ttk.Combobox(self, values=salas)
        self.sala_combobox.insert(0, "Seleccionar SALA")
        self.sala_combobox.place(x=10, y=50, width=190)

        # Fecha
        self.fechaReserva = tkcalendar.DateEntry(self, locale='es_ES', date_pattern='dd/MM/yyyy')
        self.fechaReserva.place(x=10, y=90, width=190)

        # Horario
        horarios = []
        for hora in range(24):
            horarios.extend(["{}:00".format(str(hora).zfill(2)), "{}:30".format(str(hora).zfill(2))])
        self.hora_spinbox = ttk.Spinbox(self, values=horarios)
        self.hora_spinbox.insert(0, "Horario")  # Texto de ejemplo en el Entry
        self.hora_spinbox.place(x=10, y=130, width=190)

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
        treeScroll.pack(side="right", fill="y", expand=True)
        treeFrame.columnconfigure(0, weight=1)

        # Frame para el TreeView
        cols = ("Banda", "Sala", "Fecha", "Horario", "HR/s", "Abonado")
        self.lista = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        # Configurar los encabezados de las columnas
        self.lista.heading("Banda", text="Banda", command=lambda: self.ordenar_por_columna("Banda"))
        self.lista.heading("Sala", text="Sala", command=lambda: self.ordenar_por_columna("Sala"))
        self.lista.heading("Fecha", text="Fecha", command=lambda: self.ordenar_por_columna("Fecha"))
        self.lista.heading("Horario", text="Horario", command=lambda: self.ordenar_por_columna("Horario"))
        self.lista.heading("HR/s", text="HR/s", command=lambda: self.ordenar_por_columna("HR/s"))
        self.lista.heading("Abonado", text="Abonado", command=lambda: self.ordenar_por_columna("Abonado"))

        self.lista.column("Banda", width=120, anchor = "center", stretch=False)
        self.lista.column("Sala", width=100, anchor = "center", stretch=False)
        self.lista.column("Fecha", width=75, anchor = "center", stretch=False)
        self.lista.column("Horario", width=50, anchor = "center", stretch=False)
        self.lista.column("HR/s", width=50, anchor = "center", stretch=False)
        self.lista.column("Abonado", width=55, anchor = "center", stretch=False)

        treeScroll.config(command=self.lista.yview)
        self.lista.pack(expand=True, fill="both")
        self.update()

    def agregar_a_calendario(self):
        # Obtener los datos ingresados en los widgets
        banda = self.name_entry.get()
        sala = self.sala_combobox.get()
        fecha = self.fechaReserva.get_date().strftime("%Y-%m-%d")
        horario = self.hora_spinbox.get()
        tiempo = self.tiempo_combobox.get()
        abonado = "Si" if self.varAux.get() else "No"

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
        digitoAux = logic.extraer_digito(tiempo)
        minutos = digitoAux * 60
        hora_inicio_reserva = datetime.strptime(horario, "%H:%M")
        hora_fin_reserva = hora_inicio_reserva + timedelta(minutes=minutos)

        print("Pre DEF, FIN RESERVA: ", hora_fin_reserva, "INI RESERVA: ", hora_inicio_reserva)

        # Validar si la sala está disponible en el horario seleccionado
        if logic.sala_disponible(sala, fecha, hora_inicio_reserva.strftime("%H:%M"), hora_fin_reserva.strftime("%H:%M")):
            # Guardar los datos en el hoja de cálculo
            logic.guardar_reserva(banda, sala, fecha, horario, tiempo, abonado)

            # Finalmente, limpiar los widgets para el siguiente ingreso
            self.name_entry.delete(0, "end")
            self.sala_combobox.set("Seleccionar SALA")
            self.varAux.set(False)
            self.fechaReserva.set_date(date.today())
            self.hora_spinbox.delete(0, "end")
            self.tiempo_combobox.set("Seleccionar tiempo")  # Limpiar el combobox de tiempo

            # Después de agregar la entrada, cargar nuevamente los datos para actualizar el widget de lista
            self.cargar_datos_en_listado()

        else:
            messagebox.showerror("Error", "La sala no está disponible en el horario seleccionado.")

    def borrar_seleccionados(self):
        selected_items = self.lista.selection()
        if not selected_items:
            messagebox.showinfo("Advertencia", "Por favor, selecciona al menos una entrada para borrar.")
            return

        # Preguntar al usuario si realmente quiere borrar las entradas seleccionadas
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar las entradas seleccionadas?")
        if not confirmacion:
            return

        # Eliminar las reservas seleccionadas del TreeView y de la base de datos
        for item in selected_items:
            values = self.lista.item(item, 'values')
            banda, sala, fecha, horario = values[0], values[1], values[2], values[3]
            
            self.lista.delete(item)  # Eliminar del TreeView
            logic.borrar_reserva_por_datos(banda, sala, fecha, horario)  # Eliminar de la base de datos

    def cargar_datos_en_listado(self, data=None):
        if data is None:
            data = logic.cargar_datos_bandas()
        
        # Limpiar el TreeView
        for item in self.lista.get_children():
            self.lista.delete(item)

        # Insertar los nuevos datos en el TreeView
        for row in data:
            # Omitir el primer elemento (ID) y agregar los demás elementos
            self.lista.insert("", "end", values=row[1:])  # Aquí omitimos el primer elemento (ID)

    def ordenar_por_columna(self, columna):
        # Obtener los datos actuales del TreeView
        data = [self.lista.item(item)['values'] for item in self.lista.get_children('')]

        # Obtener el índice de la columna
        columnas = ["Banda", "Sala", "Fecha", "Horario", "HR/s", "Abonado"]
        columna_index = columnas.index(columna)


        # Ordenar los datos en función de la columna seleccionada
        if columna_index == 3:  # Índices de las columnas de Horario
            data_ordenada = sorted(data, key=lambda x: datetime.strptime(x[columna_index], "%H:%M"))
        elif columna_index == 2:  # Índice de la columna de Fecha
            data_ordenada = sorted(data, key=lambda x: datetime.strptime(x[columna_index], "%Y-%m-%d"))
        else:
            data_ordenada = sorted(data, key=lambda x: x[columna_index])

        # Limpiar el TreeView
        for item in self.lista.get_children():
            self.lista.delete(item)

        # Insertar los datos ordenados en el TreeView
        for row in data_ordenada:
            self.lista.insert("", "end", values=row) # type: ignore

class CalendarioTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Crear calendario
        self.calendario = Calendar(self, locale='es_ES', showweeknumbers=False)
        self.calendario.pack(fill="both", expand=True)
        self.calendario.bind("<<CalendarSelected>>", self.on_calendar_click)
        self.actualizar_calendario()
        self._last_click_time = 0
        self._click_interval = 500  # Tiempo en milisegundos para considerar un doble clic

    def on_calendar_click(self, event):
        current_time = datetime.now().timestamp() * 1000
        elapsed_time = current_time - self._last_click_time
        self._last_click_time = current_time

        if elapsed_time < self._click_interval:
            self.mostrar_entradas(event)

    def actualizar_calendario(self):
        data = logic.cargar_datos_bandas()

        for event in self.calendario.get_calevents():
            self.calendario.calevent_remove(event)

        self.calendario.tag_config("marcada", background="lightblue")

        for tupla in data:
            fecha_str = tupla[3]
            fecha_dt = datetime.strptime(fecha_str, "%Y-%m-%d")

            self.calendario.calevent_create(
                fecha_dt,
                f"<span font='Arial 12'>{tupla[1]}</span>\n"
                f"Sala: {tupla[2]}\n"
                f"Fecha: {tupla[3]}\n"
                f"Horario: {tupla[4]}\n"
                f"HR/s: {tupla[5]}\n"
                f"Abonado: {tupla[6]}\n",
                "marcada",
            )

    def mostrar_entradas(self, event):
        selected_date = self.calendario.selection_get()
        if selected_date is not None:
            selected_date_str = selected_date.strftime("%Y-%m-%d")
            data = logic.cargar_datos_bandas()
            entradas_seleccionadas = [tupla for tupla in data if tupla[3] == selected_date_str]

            if entradas_seleccionadas:
                popup_content = "Entradas agendadas para {}:\n\n".format(selected_date_str)
                for entrada in entradas_seleccionadas:
                    popup_content += "Banda: {}\nSala: {}\nFecha: {}\nHorario: {}\nHR/s: {}\nAbonado: {}\n\n".format(
                        entrada[1], entrada[2], entrada[3], entrada[4], entrada[5], entrada[6]
                    )

                messagebox.showinfo("Entradas Agendadas", popup_content)
            else:
                messagebox.showinfo("Sin Entradas", "No hay entradas agendadas para {}".format(selected_date_str))

class BandasTab(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.detalles_frame = ttk.Frame(self)
        self.detalles_frame.pack(fill="both", expand=True)
        
        self.listbox_bandas = tk.Listbox(self.detalles_frame, selectmode=tk.SINGLE)
        self.listbox_bandas.pack(fill=tk.BOTH, expand=True)

        data = logic.cargar_datos_bandas()

        self.listbox_bandas.delete(0, tk.END)

        # Insertar los nuevos datos en el TreeView
        for row in data:
            # Omitir el primer elemento (ID) y agregar los demás elementos
            self.listbox_bandas.insert(tk.END, row[1:])  # Aquí omitimos el primer elemento (ID)

class BarTab(tk.Frame):
    def __init__(self, master, salas):
        super().__init__(master)

        self.master = master
        self.salas = salas + ["Nuevo Individuo"]
        self.closed_tabs = []  # Lista para almacenar los índices de los tabs cerrados

        self.frame_widgets_bar = tk.Frame(self)
        self.frame_widgets_bar.pack(side="top", fill="x", padx=10, pady=10)

        # Agregar botón para abrir un nuevo tab para un individuo
        self.nuevo_tab_combobox = ttk.Combobox(self.frame_widgets_bar, values=self.salas)
        self.nuevo_tab_combobox.insert(0, "Seleccionar opcion")
        self.nuevo_tab_combobox.pack(side="left", pady=(10, 0))

        self.confirmar_boton = ttk.Button(self.frame_widgets_bar, text="Agregar nueva hoja", command=self.agregar_tab_widget)
        self.confirmar_boton.pack(side="left", padx=10, pady=(10, 0))

        self.notebook_frame_bar = tk.Frame(self)
        self.notebook_frame_bar.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # Crear el Notebook para las pestañas de salas
        self.sala_notebook = ttk.Notebook(self.notebook_frame_bar)
        self.sala_notebook.pack(fill="both", expand=True)

        # Crear pestañas de salas
        self.salas_tabs = {}  # Diccionario para almacenar las instancias de SalaTab

        self.frame_widgets_bar.configure(bg="white")


        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        logic.crear_db_tabs()

    def get_frame_widgets(self):
        return self.frame_widgets_bar

    def borrar_tab_sala(self, nombre):  # Definir la función de borrado
        if nombre in self.salas_tabs:
            del self.salas_tabs[nombre]
            self.sala_notebook.forget(self.sala_notebook.index("current"))

            conn = sqlite3.connect("tabs_database.db")
            cursor = conn.cursor()

            # Eliminar de la base de datos
            cursor.execute("DELETE FROM tabs WHERE tab_name = ?", (nombre,))
            conn.commit()

            conn.close()

    def agregar_tab_widget(self):
        opcion = self.nuevo_tab_combobox.get()
        if opcion == "Nuevo Individuo":
            self.abrir_tab_individuo()
        else:
            self.abrir_tab_sala()

    def abrir_tab_individuo(self):
        nombre_individuo = simpledialog.askstring("Nuevo Individuo", "Ingrese el nombre del individuo:")
        if nombre_individuo:
            tab_individuo = SalaTab(self.sala_notebook, nombre_individuo, self.borrar_tab_sala)
            self.sala_notebook.add(tab_individuo, text=nombre_individuo)
            self.salas_tabs[nombre_individuo] = tab_individuo

    def abrir_tab_sala(self):
        sala = self.nuevo_tab_combobox.get()
        if sala:
            tab_sala = SalaTab(self.sala_notebook, sala, self.borrar_tab_sala)
            tab_id = logic.guardar_tab_en_db(sala)
            tab_sala.delete_callback = self.borrar_tab_sala  # Asignar la función de borrado al atributo
            self.sala_notebook.add(tab_sala, text=sala)
            self.salas_tabs[sala] = tab_sala
        
class SalaTab(tk.Frame):
    def __init__(self, master, nombre, delete_callback):
        super().__init__(master)

        self.tab_id = None
        self.consumos = consumos
        self.nombre = nombre
        self.delete_callback = delete_callback


        print("Creando SalaTab con nombre:", nombre)

        self.frame_listbox_sala = tk.Frame(self)
        self.frame_listbox_sala.pack(side="left", fill="y", padx=10, pady=10)

        self.frame_widgets_sala = tk.Frame(self)
        self.frame_widgets_sala.pack(side="right", fill="y", padx=10, pady=10)

        self.lista_consumos = tk.Listbox(self.frame_listbox_sala, width=70)
        self.lista_consumos.pack(fill="both", padx=10, pady=10)

        # Botón para agregar consumo
        self.agregar_button = tk.Button(self.frame_widgets_sala, text="Agregar Consumo", command=self.agregar_consumo_popup)
        self.agregar_button.pack(fill="both", padx=10, pady=10)

        self.calcular_button = tk.Button(self.frame_widgets_sala, text="Calcular Total", command=self.calcular_total)
        self.calcular_button.pack(fill="both", padx=10, pady=10)

        cruz_cierre = tk.Label(self.frame_widgets_sala, text="x", padx=5, cursor="hand2")
        cruz_cierre.bind("<Button-1>", self.borrar_tab_actual)
        cruz_cierre.pack(fill="both", padx=10, pady=10)

    def agregar_consumo_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Agregar Consumo")
        popup.geometry("200x200")

        # Etiqueta y entrada para el nombre del consumo
        nombre_label = tk.Label(popup, text="Nombre del Consumo:")
        nombre_label.pack(padx=10, pady=(10, 0))
        nombre_consumo = tk.Entry(popup)
        nombre_consumo.pack(padx=10, pady=(0, 10))

        # Etiqueta y entrada para el precio del consumo
        precio_label = tk.Label(popup, text="Precio del Consumo:")
        precio_label.pack(padx=10, pady=(10, 0))
        precio_consumo = tk.Entry(popup)
        precio_consumo.pack(padx=10, pady=(0, 10))

        # Botón para confirmar la adición del consumo
        confirm_button = tk.Button(popup, text="Agregar", command=lambda: self.confirmar_agregar_consumo(popup, nombre_consumo.get(), precio_consumo.get()))
        confirm_button.pack(padx=10, pady=20)

    def confirmar_agregar_consumo(self, popup, nombre_consumo, precio_consumo):
        nombre_consumo = simpledialog.askstring("Agregar Consumo", "Ingresa el nombre del consumo:")
        if nombre_consumo:
            precio_consumo = simpledialog.askinteger("Agregar Consumo", "Ingresa el precio del consumo:")
            if precio_consumo is not None:
                self.agregar_consumo(nombre_consumo, precio_consumo)

    def agregar_consumo(self, nombre, precio):
        self.consumos[nombre] = precio
        self.actualizar_lista_consumos()

    def actualizar_precio(self, nombre, precio):
        if nombre in self.consumos:
            self.consumos[nombre] = precio

    def eliminar_consumo(self, nombre):
        if nombre in self.consumos:
            del self.consumos[nombre]

    def actualizar_lista_consumos(self):
        self.lista_consumos.delete(0, tk.END)
        for nombre, precio in self.consumos.items():
            self.lista_consumos.insert(tk.END, f"{nombre}: {precio:.2f}")

    def calcular_total(self):
        total = sum(self.consumos.values())
        messagebox.showinfo("Total de Consumos", f"El total de consumos es: {total:.2f}")

    def borrar_tab_actual(self, event):
        print("Intentando borrar el tab con nombre:", self.nombre)
        self.delete_callback(self.nombre)  # Llamar a la función de borrado desde el callback
        logic.borrar_tab_actual_db(self.tab_id)  # Llamar a la función en logic.py


