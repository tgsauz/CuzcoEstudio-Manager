import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.font import Font


from ..logic import recuperar_consumos, guardar_consumo, agregar_consumo_gasto, editar_consumo, borrar_consumo


class ConsumosWindow(tk.Toplevel):
    def __init__(self, parent, style, ruta_base_datos_consumos_listado):
        super().__init__(parent)
        self.style = style
        self.title(f"Consumos")

        self.ruta_base_datos_consumos_listado = ruta_base_datos_consumos_listado

        self.consumos_tree_frame = ttk.Frame(self)
        self.consumos_tree_frame.pack(side=tk.LEFT, fill="both", expand=True)

        self.consumos_treeview = ttk.Treeview(self.consumos_tree_frame, columns=('Producto', 'Cantidad', 'Precio'), show='headings')

        for col in ('Producto', 'Cantidad', 'Precio'):
            self.consumos_treeview.heading(col, text=col, anchor=tk.CENTER)
            self.consumos_treeview.column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        self.consumos_treeview.heading('#0', text='ID')
        self.consumos_treeview.column('#0', width=0, stretch=tk.NO)

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

        self.entry_add_precio_venta = ttk.Entry(self.consumos_button_frame)
        self.entry_add_precio_venta.insert(0, 'Valor a vender')
        self.entry_add_precio_venta.bind("<FocusIn>", lambda event: self.entry_add_precio_venta.delete(0, "end") if self.entry_add_precio_venta.get() == 'Valor a comprar' else None)
        self.entry_add_precio_venta.pack(pady=5, padx=5, fill='x')

        self.entry_add_precio_compra = ttk.Entry(self.consumos_button_frame)
        self.entry_add_precio_compra.insert(0, 'Valor de compra')
        self.entry_add_precio_compra.bind("<FocusIn>", lambda event: self.entry_add_precio_compra.delete(0, "end") if self.entry_add_precio_compra.get() == 'Valor de compra' else None)
        self.entry_add_precio_compra.pack(pady=5, padx=5, fill='x')

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
        self.update_treeview()

    def agregar_consumo_listado(self):
        nombre = self.product_name.get()
        cantidad = self.spinbox_cantidad.get()
        precio = self.entry_add_precio_venta.get()

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

        editing_window = EditConsumosWindow(self, self.data, self.ruta_base_datos_consumos_listado, self)
        editing_window.grab_set()
        editing_window.focus_set()
        editing_window.wait_window()

    def update_treeview(self):
        for i in self.consumos_treeview.get_children():
            self.consumos_treeview.delete(i)

        consumos = recuperar_consumos(self.ruta_base_datos_consumos_listado)

        for consumo in consumos:
            self.consumos_treeview.insert('', 'end', text=consumo[0], values=consumo)

class AddConsumosWindow(tk.Toplevel):
    def __init__(self, parent, ruta_base_datos_consumos_listado, selected_treeview):
        super().__init__(parent)
        self.title(f"Agregar consumo")


        #consumos_filtered filtra los consumos que tienen cantidad 0 para asegurar que no se puedan vender consumos sin stock.
        consumos = recuperar_consumos(ruta_base_datos_consumos_listado)
        self.consumos_filtered = [consumo for consumo in consumos if consumo[1] > 0]
        self.first_columns = [consumo[0] for consumo in self.consumos_filtered]
        print("ConsumosFiltered: ", self.consumos_filtered)

        self.consumos_askdialog_frame = ttk.Frame(self)
        self.consumos_askdialog_frame.pack(fill="both", expand=True)

        self.consumos_combobox_listado = ttk.Combobox(self.consumos_askdialog_frame, values=self.first_columns)
        self.consumos_combobox_listado.insert(0, "Seleccionar consumo")
        self.consumos_combobox_listado.pack(pady=5, padx=5, fill='x')

        self.consumos_spinbox_listado = ttk.Spinbox(self.consumos_askdialog_frame, from_=1, to=50)
        self.consumos_spinbox_listado.insert(0, 'Cantidad')
        self.consumos_spinbox_listado.pack(pady=5, padx=5, fill='x')

        self.consumos_combobox_listado.bind("<<ComboboxSelected>>", self.update_spinbox)

        self.consumos_aceptar_button = ttk.Button(self.consumos_askdialog_frame, command=lambda: self.agregar_consumo_al_tab(ruta_base_datos_consumos_listado, selected_treeview))
        self.consumos_aceptar_button.config(text='Aceptar')
        self.consumos_aceptar_button.pack(pady=5, padx=5, fill='x')

        self.consumo_cancelar_button = ttk.Button(self.consumos_askdialog_frame, command=lambda: self.destroy())
        self.consumo_cancelar_button.config(text='Cancelar')
        self.consumo_cancelar_button.pack(pady=5, padx=5, fill='x')

    def update_spinbox(self, event):
        selected_consumo = self.consumos_combobox_listado.get()
        print("ConsumoSelected: ", selected_consumo)
        print("ConsumosListFiltered: ", self.consumos_filtered)
        selected_consumo_index = None
        if selected_consumo and selected_consumo != 'Seleccionar consumo':
            selected_consumo_index = next((index for index, consumo in enumerate(self.consumos_filtered) if consumo[0] == selected_consumo), None)
        if selected_consumo_index is not None:
            self.consumos_spinbox_listado.configure(from_=1, to=self.consumos_filtered[selected_consumo_index][1])
        else:
            self.consumos_spinbox_listado.configure(from_=1, to=50)

    def agregar_consumo_al_tab(self, ruta_base_datos_consumos_listado, selected_treeview):
        nombre = self.consumos_combobox_listado.get()
        cantidad = int(self.consumos_spinbox_listado.get())
        print(nombre, cantidad)

        
        
        if not nombre or nombre == 'Nombre del consumo' or not cantidad or cantidad == 'Cantidad':
            messagebox.showwarning("Datos inválidos", "Ingrese todos los datos del consumo.")
            return
        
        agregar_consumo_gasto(ruta_base_datos_consumos_listado, nombre, cantidad)
        selected_treeview.insert("", tk.END, values=(nombre, cantidad))

        self.destroy()
   
class EditConsumosWindow(tk.Toplevel):
    def __init__(self, parent, data, ruta_base_datos_consumos_listado, consumos_window):
        super().__init__(parent)
        self.title(f"Editar consumo")
        self.consumos_window = consumos_window

        self.consumos_edit_frame = ttk.Frame(self)
        self.consumos_edit_frame.pack(fill="both", expand=True)
        print(data)

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
        data[0] = self.consumos_entry_listado_edit.get()
        data[1] = int(self.consumos_spinbox_listado.get())
        data[2] = int(self.consumo_entry_precio.get())
        data[3] = int(data[3])
        
        try:
            if not data[0] or data[0] == 'Nombre del consumo' or not data[1] or data[1] == 'Cantidad' or not data[2] or data[2] == 'Precio':
                messagebox.showwarning("Datos inválidos", "Ingrese todos los datos del consumo.")
                return
            editar_consumo(ruta_base_datos_consumos_listado, data)
        except:
            messagebox.showwarning("Error", "Hubo un problema inesperado al editar el consumo.")
            return
        finally:
            self.consumos_window.update_treeview()
            self.destroy()
            return
        