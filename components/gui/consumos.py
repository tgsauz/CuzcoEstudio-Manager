import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.font import Font

from ..logic import recuperar_consumos, guardar_consumo
from ..config import get_rutas


class ConsumosWindow(tk.Toplevel):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style
        self.title(f"Consumos")

        _, _, self.ruta_base_datos_consumos_listado = get_rutas()

        self.consumos_tree_frame = ttk.Frame(self)
        self.consumos_tree_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.consumos_treeview = ttk.Treeview(self.consumos_tree_frame, columns=('Producto', 'Cantidad', 'Precio') ,show='headings')

        for col in ('Producto', 'Cantidad', 'Precio'):
            self.consumos_treeview.heading(col, text=col, anchor=tk.CENTER)
            self.consumos_treeview.column(col, anchor=tk.CENTER)
            self.consumos_treeview.column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        self.consumos_treeview.pack(fill="both", expand=True)

        self.consumos_button_frame = ttk.Frame(self)
        self.consumos_button_frame.pack(fill="both", expand=True)

        #Entries
        self.product_name = ttk.Entry(self.consumos_button_frame)
        self.product_name.insert(0, 'Nombre del consumo')
        self.product_name.bind("<FocusIn>", lambda event: self.product_name.delete(0, "end") if self.product_name.get() == 'Nombre del consumo' else None)
        self.product_name.pack(pady=5, padx=5, fill='x')

        self.spinbox_cantidad = ttk.Spinbox(self.consumos_button_frame, from_=1, to=50)
        self.spinbox_cantidad.insert(0, 'Cantidad')
        self.spinbox_cantidad.pack(pady=5, padx=5, fill='x')

        self.entry_add_precio = ttk.Entry(self.consumos_button_frame)
        self.entry_add_precio.insert(0, 'Precio')
        self.entry_add_precio.bind("<FocusIn>", lambda event: self.entry_add_precio.delete(0, "end") if self.entry_add_precio.get() == 'Precio' else None)
        self.entry_add_precio.pack(pady=5, padx=5, fill='x')

        self.button_add_consumo = ttk.Button(self.consumos_button_frame, command=lambda: self.agregar_consumo())
        self.button_add_consumo.config(text='Agregar consumo')
        self.button_add_consumo.pack(pady=5, padx=5, fill='x')

        self.separator_horizontal = ttk.Separator(self.consumos_button_frame, orient='horizontal')
        self.separator_horizontal.pack(pady=10, padx=5, fill='x')

        self.button_remove_consumo = ttk.Button(self.consumos_button_frame, command=lambda: self.eliminar_consumo())
        self.button_remove_consumo.config(text='Eliminar consumo')
        self.button_remove_consumo.pack(pady=5, padx=5, fill='x')

    def agregar_consumo(self):
        nombre = self.product_name.get()
        cantidad = self.spinbox_cantidad.get()
        precio = self.entry_add_precio.get()

        if not nombre or nombre == 'Nombre del consumo' or not cantidad or cantidad == 'Cantidad' or not precio or precio == 'Precio':
            messagebox.showwarning("Datos inválidos", "Ingrese todos los datos del consumo.")
            return

        self.consumos_treeview.insert("", tk.END, values=(nombre, cantidad, precio))
        guardar_consumo(self.ruta_base_datos_consumos_listado, nombre, cantidad, precio)
        

    def eliminar_consumo(self):
        selected_item = self.consumos_treeview.selection()

        if not selected_item:
            messagebox.showwarning("Seleccion inválida", "Seleccione un consumo para eliminarlo.")
            return
        
        if not messagebox.askyesno("Eliminar consumo", "¿Está seguro que desea eliminar el consumo seleccionado?"):
            return
        
        for item in selected_item:
            self.consumos_treeview.delete(item)
