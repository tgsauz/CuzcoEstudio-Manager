import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.font import Font

from ..logic import recuperar_consumos, guardar_consumo, agregar_consumo_gasto, encontrar_consumo, borrar_consumo


class ConsumosWindow(tk.Toplevel):
    def __init__(self, parent, style, ruta_base_datos_consumos_listado):
        super().__init__(parent)
        self.style = style
        self.title(f"Consumos")

        self.ruta_base_datos_consumos_listado = ruta_base_datos_consumos_listado

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

        self.spinbox_cantidad = ttk.Spinbox(self.consumos_button_frame, from_=1, to=25)
        self.spinbox_cantidad.insert(0, 'Cantidad')
        self.spinbox_cantidad.pack(pady=5, padx=5, fill='x')

        self.entry_add_precio = ttk.Entry(self.consumos_button_frame)
        self.entry_add_precio.insert(0, 'Precio')
        self.entry_add_precio.bind("<FocusIn>", lambda event: self.entry_add_precio.delete(0, "end") if self.entry_add_precio.get() == 'Precio' else None)
        self.entry_add_precio.pack(pady=5, padx=5, fill='x')

        self.button_add_consumo = ttk.Button(self.consumos_button_frame, command=lambda: self.agregar_consumo_listado())
        self.button_add_consumo.config(text='Agregar consumo')
        self.button_add_consumo.pack(pady=5, padx=5, fill='x')

        self.separator_horizontal1 = ttk.Separator(self.consumos_button_frame, orient='horizontal')
        self.separator_horizontal1.pack(pady=10, padx=5, fill='x')

        self.button_edit_consumo = ttk.Button(self.consumos_button_frame, command=lambda: self.editar_consumo_listado(self.consumos_treeview))
        self.button_edit_consumo.config(text='Editar consumo')
        self.button_edit_consumo.pack(pady=5, padx=5, fill='x')

        self.separator_horizontal2 = ttk.Separator(self.consumos_button_frame, orient='horizontal')
        self.separator_horizontal2.pack(pady=10, padx=5, fill='x')

        self.button_remove_consumo = ttk.Button(self.consumos_button_frame, command=lambda: self.eliminar_consumo_listado(self.consumos_treeview))
        self.button_remove_consumo.config(text='Eliminar consumo')
        self.button_remove_consumo.pack(pady=(5, 10), padx=5, fill='x')


        # Cargar datos de la base de datos al treeview
        consumos = recuperar_consumos(self.ruta_base_datos_consumos_listado)
        for consumo in consumos:
            self.consumos_treeview.insert("", tk.END, values=consumo)

    def agregar_consumo_listado(self):
        nombre = self.product_name.get()
        cantidad = self.spinbox_cantidad.get()
        precio = self.entry_add_precio.get()

        if not nombre or nombre == 'Nombre del consumo' or not cantidad or cantidad == 'Cantidad' or not precio or precio == 'Precio':
            messagebox.showwarning("Datos inválidos", "Ingrese todos los datos del consumo.")
            return

        self.consumos_treeview.insert("", tk.END, values=(nombre, cantidad, precio))
        guardar_consumo(self.ruta_base_datos_consumos_listado, nombre, cantidad, precio)
        
    def eliminar_consumo_listado(self, consumos_treeview):
        listitem_selected = consumos_treeview.selection()
        if not listitem_selected:
            messagebox.showwarning("Seleccion inválida", "Seleccione un consumo para eliminarlo.")
            return
        
        if not messagebox.askyesno("Eliminar consumo", "¿Está seguro que desea eliminar el consumo seleccionado?"):
            return
        
        for item in listitem_selected:
            self.data = consumos_treeview.item(item)['values']
            borrar_consumo(self.ruta_base_datos_consumos_listado, self.data)
            self.consumos_treeview.delete(item)
        

    def editar_consumo_listado(self, consumos_treeview):
        listitem_selected = consumos_treeview.selection()
        if not listitem_selected:
            messagebox.showwarning("Seleccion inválida", "Seleccione un consumo para editarlo.")
            return
        self.data = consumos_treeview.item(listitem_selected)['values']

        editing_window = EditConsumosWindow(self, self.data, self.ruta_base_datos_consumos_listado)
        editing_window.grab_set()
        editing_window.focus_set()
        editing_window.wait_window()

class AddConsumosWindow(tk.Toplevel):
    def __init__(self, parent, ruta_base_datos_consumos_listado, selected_treeview):
        super().__init__(parent)
        self.title(f"Agregar consumo")


        #consumos_filtered filtra los consumos que tienen cantidad 0 para asegurar que no se puedan vender consumos sin stock.
        consumos = recuperar_consumos(ruta_base_datos_consumos_listado)
        consumos_filtered = [consumo for consumo in consumos if consumo[1] > 0]

        self.consumos_askdialog_frame = ttk.Frame(self)
        self.consumos_askdialog_frame.pack(fill="both", expand=True)

        self.consumos_combobox_listado = ttk.Combobox(self.consumos_askdialog_frame, values=consumos_filtered)
        self.consumos_combobox_listado.insert(0, "Seleccionar consumo")
        self.consumos_combobox_listado.pack(pady=5, padx=5, fill='x')

        self.consumos_spinbox_listado = ttk.Spinbox(self.consumos_askdialog_frame, from_=1, to=50)
        self.consumos_spinbox_listado.insert(0, 'Cantidad')
        self.consumos_spinbox_listado.pack(pady=5, padx=5, fill='x')

        self.consumos_aceptar_button = ttk.Button(self.consumos_askdialog_frame, command=lambda: self.agregar_consumo_al_tab(ruta_base_datos_consumos_listado, selected_treeview))
        self.consumos_aceptar_button.config(text='Aceptar')
        self.consumos_aceptar_button.pack(pady=5, padx=5, fill='x')

        self.consumo_cancelar_button = ttk.Button(self.consumos_askdialog_frame, command=lambda: self.destroy())
        self.consumo_cancelar_button.config(text='Cancelar')
        self.consumo_cancelar_button.pack(pady=5, padx=5, fill='x')

    def agregar_consumo_al_tab(self, ruta_base_datos_consumos_listado, selected_treeview):
        nombre = self.consumos_combobox_listado.get()
        start = nombre.find('{') + 1  # Add 1 to exclude the brace itself
        end = nombre.find('}')
        nombre_inside_braces = nombre[start:end]

        cantidad = int(self.consumos_spinbox_listado.get())
        print(nombre_inside_braces, cantidad)
        
        if not nombre_inside_braces or nombre_inside_braces == 'Nombre del consumo' or not cantidad or cantidad == 'Cantidad':
            messagebox.showwarning("Datos inválidos", "Ingrese todos los datos del consumo.")
            return
        
        agregar_consumo_gasto(ruta_base_datos_consumos_listado, nombre_inside_braces, cantidad)
        selected_treeview.insert("", tk.END, values=(nombre_inside_braces, cantidad))

        self.destroy()

#WIP (Work in progress)   
class EditConsumosWindow(tk.Toplevel):
    def __init__(self, parent, data, ruta_base_datos_consumos_listado):
        super().__init__(parent)
        self.title(f"Editar consumo")

        self.consumos_edit_frame = ttk.Frame(self)
        self.consumos_edit_frame.pack(fill="both", expand=True)

        self.consumos_entry_listado_edit = ttk.Entry(self.consumos_edit_frame)
        self.consumos_entry_listado_edit.insert(0, data[0])
        self.consumos_entry_listado_edit.pack(pady=5, padx=5, fill='x')

        self.consumos_spinbox_listado = ttk.Spinbox(self.consumos_edit_frame, from_=1, to=50)
        self.consumos_spinbox_listado.insert(0, data[1])
        self.consumos_spinbox_listado.pack(pady=5, padx=5, fill='x')

        self.consumo_entry_precio = ttk.Entry(self.consumos_edit_frame)
        self.consumo_entry_precio.insert(0, data[2])
        self.consumo_entry_precio.pack(pady=5, padx=5, fill='x')

        self.consumos_aceptar_button = ttk.Button(self.consumos_edit_frame, command=lambda: self.guardar_consumo_editado(data, ruta_base_datos_consumos_listado))
        self.consumos_aceptar_button.config(text='Aceptar')
        self.consumos_aceptar_button.pack(pady=5, padx=5, fill='x')

        self.consumo_cancelar_button = ttk.Button(self.consumos_edit_frame, command=lambda: self.destroy())
        self.consumo_cancelar_button.config(text='Cancelar')
        self.consumo_cancelar_button.pack(pady=5, padx=5, fill='x')

    def guardar_consumo_editado(self, data, ruta_base_datos_consumos_listado):
        nombre = self.consumos_entry_listado_edit.get()
        cantidad = self.consumos_spinbox_listado.get()
        precio = self.consumo_entry_precio.get()

        pass
        