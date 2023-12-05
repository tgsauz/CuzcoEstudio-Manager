from tkinter import ttk
import tkinter as tk
class BarComp(ttk.Frame):
    def __init__(self, parent, style):
        ttk.Frame.__init__(self, parent)

        self.style = style

        self.button_add_tab_frame = ttk.Frame(self)
        self.button_add_tab_frame.pack(fill="x", expand=False)

        self.notebook_and_content_frame = ttk.Frame(self)
        self.notebook_and_content_frame.pack(fill="both", expand=True)

        self.button_add_tab = ttk.Button(self.button_add_tab_frame)
        self.button_add_tab.config(text='+', width=2)
        self.button_add_tab.pack(pady=(0,4), side=tk.RIGHT)

        self.notebook_bar = ttk.Notebook(self.notebook_and_content_frame)
        self.notebook_bar.pack(fill="both", expand=True)
        

        