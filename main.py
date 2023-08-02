import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import tkcalendar
import locale
from datetime import date, datetime, timedelta
import os
import openpyxl
from openpyxl.utils import get_column_letter

locale.setlocale(locale.LC_ALL, 'es_ES')

# Guardar archivo en Excel
def guardar_en_excel(banda, sala, abonado, fecha, horario, tiempo):
    archivo_excel = "calendario_bandas.xlsx"

    if not os.path.exists(archivo_excel):
        # Si el archivo no existe, creamos uno nuevo con las cabeceras
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Banda", "Sala", "Abonado", "Fecha", "Horario", "Tiempo"])
    else:
        # Si el archivo ya existe, abrimos el archivo existente
        wb = openpyxl.load_workbook(archivo_excel)
        ws = wb.active

    # Agregar una nueva fila con los datos
    nueva_fila = [banda, sala, abonado, fecha, horario, tiempo]
    ws.append(nueva_fila)

    # Guardar los cambios en el archivo
    wb.save(archivo_excel)

# Función para mostrar la pestaña "Otras Datos" cuando se hace clic en el botón
def mostrar_otras_tab():
    notebook.select(tab_datos)

root = tk.Tk()
root.title('CuzcoManager')

style = ttk.Style(root)
root.tk.call("source", "forest-light.tcl")
root.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-light")

listaSala_combo = ["Sala A", "Sala B", "Sala C", "Sala Z", "ESTUDIO"]

class AgendaTab(ttk.Frame):
    def __init__(self):
        super().__init__()

        # Crear un frame para contener los widgets de la columna 1
        column1_frame = ttk.Frame(self)
        column1_frame.grid(row=0, column=0, padx=5, pady=(0, 5), sticky="nsew")

        #Nombre entry
        self.name_entry = ttk.Entry(column1_frame)
        self.name_entry.insert(0, "Nombre de la banda")
        self.name_entry.bind("<FocusIn>", lambda e: self.name_entry.delete('0', 'end'))
        self.name_entry.pack(fill="x", padx=5, pady=(10,5))

        #Sala entry
        self.sala_combobox = ttk.Combobox(column1_frame, values=listaSala_combo)
        self.sala_combobox.insert(0, "Seleccionar SALA")
        self.sala_combobox.pack(fill="x", padx=5, pady=(0,5))

        #EstaPago? Entry
        self.varAux = tk.BooleanVar()
        checkbutton = ttk.Checkbutton(column1_frame, text="Abonado", variable=self.varAux)
        checkbutton.pack(fill="x", padx=5, pady=(0,5))

        #Dia entry
        self.fechaReserva = tkcalendar.DateEntry(column1_frame, locale='es_ES', date_pattern='dd/MM/yyyy')
        self.fechaReserva.pack(fill="x", padx=5, pady=(0,5))

        #Widget Horario
        self.hora_entry = ttk.Entry(column1_frame)
        self.hora_entry.insert(0, "Horario")  # Texto de ejemplo en el Entry
        self.hora_entry.bind("<FocusIn>", lambda e: self.hora_entry.delete('0', 'end'))
        self.hora_entry.pack(fill="x", padx=5, pady=(0,5))

        # Crear el combobox para la columna "Tiempo"
        self.tiempo_combobox = ttk.Combobox(column1_frame, values=["1 hora", "2 horas", "3 horas", "4 horas"])
        self.tiempo_combobox.insert(0, "Seleccionar tiempo")
        self.tiempo_combobox.pack(fill="x", padx=5, pady=(0, 5))

        #Boton para insertar a calendario
        botonInsACalendario = ttk.Button(column1_frame, text="Agregar a calendario", command=self.agregar_a_calendario)
        botonInsACalendario.pack(fill="x", padx=5, pady=(0,5))

        #Separador1
        separator1 = ttk.Separator(column1_frame)
        separator1.pack(fill="x", padx=(10, 10), pady=10)

        #ModoGui
        self.mode_switch = ttk.Checkbutton(
            column1_frame, text="Dia/Noche", style="Switch", command=self.toggle_mode)
        self.mode_switch.pack(fill="x", padx=5, pady=10)

        #Separador2
        separator2 = ttk.Separator(column1_frame)
        separator2.pack(fill="x", padx=(10, 10), pady=10)

        # Botón para borrar entradas seleccionadas
        botonBorrar = ttk.Button(column1_frame, text="Borrar seleccionados", command=self.borrar_seleccionados)
        botonBorrar.pack(fill="x", padx=5, pady=(0,5))

        # Treeview para mostrar los datos
        treeFrame = ttk.Frame(self)
        treeFrame.grid(row=0, column=2, padx=10, pady=10, columnspan=1, sticky="nsew")
        treeScroll = ttk.Scrollbar(treeFrame)
        treeScroll.pack(side="right", fill="y")
        treeFrame.columnconfigure(0, weight=1)

        cols = ("Banda", "Sala", "Abonado", "Fecha", "Horario", "Tiempo")
        self.lista = ttk.Treeview(treeFrame, show="headings", yscrollcommand=treeScroll.set, columns=cols, height=13)

        # Configurar los encabezados de las columnas
        self.lista.heading("Banda", text="Banda")
        self.lista.heading("Sala", text="Sala")
        self.lista.heading("Abonado", text="Abonado")
        self.lista.heading("Fecha", text="Fecha")
        self.lista.heading("Horario", text="Horario")
        self.lista.heading("Tiempo", text="Tiempo")

        self.lista.column("Banda", width=120, anchor = "center", stretch=False)
        self.lista.column("Sala", width=100, anchor = "center", stretch=False)
        self.lista.column("Abonado", width=55, anchor = "center", stretch=False)
        self.lista.column("Fecha", width=75, anchor = "center", stretch=False)
        self.lista.column("Horario", width=50, anchor = "center", stretch=False)
        self.lista.column("Tiempo", width=50, anchor = "center", stretch=False)

        treeScroll.config(command=self.lista.yview)
        self.lista.pack(expand=True, fill="both")

        self.style = ttk.Style(self)

    def borrar_seleccionados(self):
        selected_items = self.lista.selection()
        if not selected_items:
            tk.messagebox.showinfo("Advertencia", "Por favor, selecciona al menos una entrada para borrar.")
            return

        # Preguntar al usuario si realmente quiere borrar las entradas seleccionadas
        confirmacion = tk.messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar las entradas seleccionadas?")
        if not confirmacion:
            return

        # Eliminar las entradas seleccionadas del widget de lista
        for item in selected_items:
            self.lista.delete(item)

        # Guardar los cambios en el archivo Excel
        archivo_excel = "calendario_bandas.xlsx"
        if os.path.exists(archivo_excel):
            wb = openpyxl.load_workbook(archivo_excel)
            ws = wb.active

            # Obtener los datos actuales del archivo Excel
            data = []
            for row in ws.iter_rows(values_only=True):
                data.append(row)

            # Eliminar las entradas seleccionadas de los datos
            new_data = [row for row in data if tuple(row) not in selected_items]

            # Borrar el contenido existente en el archivo Excel
            ws.delete_rows(2, ws.max_row)

            # Agregar los datos actualizados al archivo Excel
            for row in new_data:
                ws.append(row)

            # Guardar los cambios en el archivo
            wb.save(archivo_excel)

    # Agregar datos al calendario
    def agregar_a_calendario(self):
        # Obtener los datos ingresados en los widgets
        banda = self.name_entry.get()
        sala = self.sala_combobox.get()
        abonado = self.varAux.get()
        fecha = self.fechaReserva.get_date()
        horario = self.hora_entry.get()
        tiempo = self.tiempo_combobox.get()

        if self.varAux.get():
            abonado = "Sí"
        else:
            abonado = "No"

        # Validar que el nombre de la banda y la sala hayan sido ingresados
        if not banda or banda == "Nombre de la banda":
            tk.messagebox.showerror("Error", "Por favor, ingresa el nombre de la banda.")
            return

        if sala == "Seleccionar SALA":
            tk.messagebox.showerror("Error", "Por favor, selecciona una sala.")
            return
        
        if not horario or horario == "Horario":
            tk.messagebox.showerror("Error", "Por favor, ingrese un horario.")
            return

        if tiempo == "Seleccionar tiempo":
            tk.messagebox.showerror("Error", "Por favor, selecciona un tiempo.")
            return

        # Validar que todos los campos estén completos antes de agregar a la tabla
        if banda and sala and fecha and horario and tiempo:
            tab_agenda.lista.insert("", "end", values=(banda, sala, abonado, fecha, horario, tiempo))

            # Guardar los datos en el hoja de cálculo
            guardar_en_excel(banda, sala, abonado, fecha, horario, tiempo)

            # Finalmente, limpiar los widgets para el siguiente ingreso
            tab_agenda.name_entry.delete(0, "end")
            tab_agenda.sala_combobox.set("Seleccionar SALA")
            tab_agenda.varAux.set(False)
            tab_agenda.fechaReserva.set_date(date.today())
            tab_agenda.hora_entry.delete(0, "end")
            tab_agenda.tiempo_combobox.set("Seleccionar tiempo")  # Limpiar el combobox de tiempo
        else:
            # Mostrar un mensaje de error si falta algún campo
            tk.messagebox.showerror("Error", "Por favor, completa todos los campos.")

    # Modo oscuro toggle
    def toggle_mode(self):
        if self.mode_switch.instate(["selected"]):
            self.style.theme_use("forest-dark")
        else:
            self.style.theme_use("forest-light")

# Crear el Notebook para las pestañas
frame = ttk.Frame(root)
frame.pack()
notebook = ttk.Notebook(frame)
notebook.grid(row=0, column=0, padx=20, pady=10, columnspan=2, sticky="nsew")

# Pestaña Actual
tab_agenda = AgendaTab()
notebook.add(tab_agenda, text="Agenda de bandas")

# Pestaña Otras Datos
tab_datos = ttk.Frame(notebook)
notebook.add(tab_datos, text="Otras Datos")

# Función para cargar datos desde el archivo Excel y mostrarlos en el widget de listado
def cargar_datos_en_listado(tab):
    archivo_excel = "calendario_bandas.xlsx"

    if not os.path.exists(archivo_excel):
        # Si el archivo no existe, no hay datos para cargar
        return []

    # Abrir el archivo Excel y obtener la hoja activa
    wb = openpyxl.load_workbook(archivo_excel)
    ws = wb.active

    # Leer los datos de cada fila y almacenarlos en una lista
    data = []
    for row in ws.iter_rows(values_only=True):
        # Verificar que la fila tenga al menos cinco elementos (banda, sala, abonado, fecha y horario)
        if len(row) >= 5:
            banda, sala, abonado, fecha, horario, tiempo = row
            # Verificar si todas las celdas necesarias contienen información
            if banda and sala and abonado and fecha and horario:
                # Verificar si la fecha es válida antes de formatearla
                if fecha:
                    fecha_formateada = fecha.strftime('%d/%m/%Y')
                else:
                    fecha_formateada = ""
                data.append((banda, sala, abonado, fecha_formateada, horario, tiempo))

    # Limpiar el contenido actual del widget de listado en la pestaña específica
    tab.lista.delete(*tab.lista.get_children())

    # Insertar los datos en el widget de listado en la pestaña específica
    for row in data:
        tab.lista.insert("", "end", values=row)

#CargadodeDatos
cargar_datos_en_listado(tab_agenda)

root.mainloop()
