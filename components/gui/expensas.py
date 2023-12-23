import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from ..logic import recuperar_consumos

class ExpensasComp(ttk.Frame):
    def __init__(self, parent, style, ruta_base_datos_consumos_listado):
        ttk.Frame.__init__(self, parent)
        self.ruta_base_datos_consumos_listado = ruta_base_datos_consumos_listado


        self.expensas_comp_buttons_frame = ttk.Frame(self)
        self.expensas_comp_buttons_frame.pack(fill="x", expand=False)

        self.expensas_comp_frame = ttk.Frame(self)
        self.expensas_comp_frame.pack(fill="both", expand=True)

        self.balance_button = ttk.Button(self.expensas_comp_buttons_frame)
        self.balance_button.config(text='Balance')
        self.balance_button.pack(pady=(0,4), padx=(0,4), side=tk.LEFT)

        self.expensas_treeview_frame = ttk.Frame(self.expensas_comp_frame)
        self.expensas_treeview_frame.pack(fill="both", expand=True)

        self.expensas_treeview = ttk.Treeview(self.expensas_treeview_frame, columns=("Producto", "Cantidad", "Precio", "Descripción", "ID"), show='headings')

        for col in ("Producto", "Cantidad", "Precio", "Descripción", "ID"):
            self.expensas_treeview.heading(col, text=col, anchor=tk.CENTER)
            self.expensas_treeview.column(col, anchor=tk.CENTER)
            if col == "ID":
                self.expensas_treeview.column(col, width=0, stretch=tk.NO)
            else:
                self.expensas_treeview.column(col, anchor=tk.CENTER, width=Font().measure(col + 'WW'))

        self.expensas_treeview.pack(fill="both", expand=True)

        self.expensas_treeview.bind("<ButtonRelease-3>", self.show_popup_menu)

    def update_treeview(self):
        
        consumos = recuperar_consumos(self.ruta_base_datos_consumos_listado)
        for i in self.expensas_treeview.get_children():
            self.expensas_treeview.delete(i)
        for consumo in consumos:
            self.expensas_treeview.insert("", tk.END, values=consumo)

    def show_popup_menu(self, event):
        if self.expensas_treeview.selection():
            self.popup_menu = tk.Menu(self, tearoff=0)
            self.popup_menu.add_command(label="Editar", command=self.edit_expense)
            self.popup_menu.add_command(label="Ver", command=self.view_expense)
            self.popup_menu.add_separator()
            self.popup_menu.add_command(label="Eliminar", command=self.delete_expense)
            self.popup_menu.post(event.x_root, event.y_root)
            self.popup_menu.grab_set()
            self.popup_menu.bind("<FocusOut>", self.hide_popup_menu)

    def hide_popup_menu(self, event=None):
        if self.popup_menu:
            self.popup_menu = None

    def edit_expense(self):
        selected_item = self.expensas_treeview.selection()[0]
        print(f"Editando {selected_item}")

    def view_expense(self):
        selected_item = self.expensas_treeview.selection()[0]
        print(f"Viendo {selected_item}")

    def delete_expense(self):     
        selected_item = self.expensas_treeview.selection()[0]
        print(f"Eliminando {selected_item}")
