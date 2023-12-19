from tkinter import ttk, simpledialog, messagebox
import tkinter as tk
from tkinter.font import Font
from .consumos import ConsumosWindow, AddConsumosWindow
from ..logic import recuperar_consumos, guardar_consumo, sustraer_consumo_gasto
from ..config import get_rutas

class BarComp(ttk.Frame):
    def __init__(self, parent, style, ruta_base_datos_consumos_listado):
        ttk.Frame.__init__(self, parent)
        self.selected_tab_index = None
        self.tab_consumption_treeviews_dictionary = {}
        self.style = style
        self.ruta_base_datos_consumos_listado = ruta_base_datos_consumos_listado

        self.button_bar_tab_frame = ttk.Frame(self)
        self.button_bar_tab_frame.pack(fill="x", expand=False)

        self.notebook_and_content_frame = ttk.Frame(self)
        self.notebook_and_content_frame.pack(fill="both", expand=True)

        self.button_add_tab = ttk.Button(self.button_bar_tab_frame, command=lambda: self.agregar_tab_nuevo(self.tab_consumption_treeviews_dictionary, self.selected_tab_index))
        self.button_add_tab.config(text='+', width=2)
        self.button_add_tab.pack(pady=(0,4), padx=(4,0), side=tk.RIGHT)

        self.button_remove_tab = ttk.Button(self.button_bar_tab_frame, command=lambda: self.remove_tab_nuevo())
        self.button_remove_tab.config(text='x', width=2)
        self.button_remove_tab.pack(pady=(0,4), padx=(4,0), side=tk.RIGHT)

        self.button_consumos = ttk.Button(self.button_bar_tab_frame, command=lambda: self.mostrar_consumos_window(style))
        self.button_consumos.config(text='Consumos', width=10)
        self.button_consumos.pack(pady=(0,4), padx=(0,4), side=tk.LEFT)

        self.notebook_bar = ttk.Notebook(self.notebook_and_content_frame)
        self.notebook_bar.pack(fill="both", expand=True)
        
        self.setup_notebook()

    def on_tab_selected(self, event):
        self.selected_tab_index = self.notebook_bar.index(self.notebook_bar.select())

    def setup_notebook(self):
        self.notebook_bar.bind("<<NotebookTabChanged>>", self.on_tab_selected)

    def agregar_tab_nuevo(self, tab_consumption_treeviews_dictionary, selected_index):

        nombre_nuevo_tab = simpledialog.askstring("Nuevo Tab", "¿A nombre de quien?: ")
        if nombre_nuevo_tab is None and not isinstance(nombre_nuevo_tab, str):
            messagebox.showwarning("Nombre inválido", "El nombre ingresado no es válido o está vacío.")
            return
        
        new_tabs_frame = ttk.Frame(self.notebook_bar)
        self.notebook_bar.add(new_tabs_frame, text=nombre_nuevo_tab)

        new_tabs_button_frame = ttk.Frame(new_tabs_frame)
        new_tabs_treeview_frame = ttk.Frame(new_tabs_frame)

        tab_index = self.notebook_bar.index("end") - 1

        self.tab_consumption_treeviews_dictionary[tab_index] = ttk.Treeview(new_tabs_treeview_frame, columns=("Producto", "Cantidad", "Precio", "Total"), show='headings')
        for col in ('Producto', 'Cantidad', 'Precio', 'Total'):
            self.tab_consumption_treeviews_dictionary[tab_index].heading(col, text=col, anchor=tk.CENTER)
            self.tab_consumption_treeviews_dictionary[tab_index].column(col, anchor=tk.CENTER)
            self.tab_consumption_treeviews_dictionary[tab_index].column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        selected_treeview = self.tab_consumption_treeviews_dictionary[tab_index]

        tabs_button_add_consumo = ttk.Button(new_tabs_button_frame, command=lambda: self.mostrar_agregar_consumos_window(selected_treeview))
        tabs_button_add_consumo.config(text='Agregar consumo')
        tabs_button_add_consumo.pack(pady=(1,5), padx=(0,5), fill='x')

        tabs_button_delete_consumo = ttk.Button(new_tabs_button_frame, command=lambda: self.delete_consumos_from_tab(selected_treeview))
        tabs_button_delete_consumo.config(text='Eliminar consumo')
        tabs_button_delete_consumo.pack(pady=(1,5), padx=(0,5), fill='x')

        tabs_button_delete_consumo.pack(side=tk.LEFT)
        tabs_button_add_consumo.pack(side=tk.LEFT)

        new_tabs_button_frame.pack(side=tk.TOP, fill="x", expand=False)
        new_tabs_treeview_frame.pack(side=tk.BOTTOM, fill="both", expand=True)
        self.tab_consumption_treeviews_dictionary[tab_index].pack(fill="both", expand=True)

    def remove_tab_nuevo(self):
        self.notebook_bar.forget(self.notebook_bar.select())

    def mostrar_consumos_window(self, style):
        consumos_window = ConsumosWindow(self, style, self.ruta_base_datos_consumos_listado)
        consumos_window.grab_set()
        consumos_window.focus_set()
        consumos_window.wait_window()

    def mostrar_agregar_consumos_window(self, selected_treeview):
        
        # Create a dialog to select the consumption type and quantity
        consumo_dialog = AddConsumosWindow(self, self.ruta_base_datos_consumos_listado, selected_treeview)
        consumo_dialog.grab_set()
        consumo_dialog.focus_set()
        consumo_dialog.wait_window()

    def delete_consumos_from_tab(self, selected_tabs_treeview):

        if selected_tabs_treeview is None:
            messagebox.showwarning("Error", "Seleccione un tab para eliminar los consumos.")
            return

        selected_items = selected_tabs_treeview.selection()
        if not selected_items:
            error = "Seleccione un consumo para eliminarlo de los gastos."
            return error
        
        valores = selected_tabs_treeview.item(selected_items)['values']
        if not valores:
            error = "No hay valores para eliminar"
            return error
        
        if not messagebox.askyesno("Eliminar consumo", "¿Está seguro que desea eliminar el consumo?"):
            return
        
        result = sustraer_consumo_gasto(self.ruta_base_datos_consumos_listado, valores)
        if result != 1:
            print("Hubo problema")
            error = "Error al eliminar el consumo de la base de datos."
            return error
        else:
            print("paso")
            selected_tabs_treeview.delete(selected_items)
            return

