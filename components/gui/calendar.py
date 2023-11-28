from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import Calendar
from .. import logic
from ..config import get_rutas

class CalendarioComp(ttk.Frame):
    def __init__(self, parent, style):
        ttk.Frame.__init__(self, parent)
        self.ruta_base_datos_reservas, _ = get_rutas()

        # Crear calendario
        self.calendario = Calendar(self, locale='es_ES', showweeknumbers=False)
        self.calendario.pack(fill="both", expand=True)
        self.calendario.bind("<<CalendarSelected>>", self.on_calendar_click)
        self.actualizar_calendario(self.ruta_base_datos_reservas)
        self._last_click_time = 0
        self._click_interval = 500  # Tiempo en milisegundos para considerar un doble clic


    def on_calendar_click(self, event):
        current_time = datetime.now().timestamp() * 1000
        elapsed_time = current_time - self._last_click_time
        self._last_click_time = current_time

        if elapsed_time < self._click_interval:
            self.mostrar_entradas(event)

    def actualizar_calendario(self, ruta_base_datos_reservas):
        data = logic.cargar_datos_reservas(ruta_base_datos_reservas)

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
            selected_date_str = selected_date.strftime("%d-%m-%Y")
            data = logic.cargar_datos_reservas(self.ruta_base_datos_reservas)
            entradas_seleccionadas = [tupla for tupla in data if tupla[3] == selected_date_str]

            if entradas_seleccionadas:
                popup_content = "Entradas agendadas para {}:\n\n".format(selected_date_str)
                for entrada in entradas_seleccionadas:
                    popup_content += "Banda: {}\nSala: {}\nFecha: {}\nHorario: {}\nHR/s: {}\n\n".format(
                        entrada[1], entrada[2], entrada[3], entrada[4], entrada[5]
                    )

                messagebox.showinfo("Entradas Agendadas", popup_content)
            else:
                messagebox.showinfo("Sin entradas", "No hay entradas agendadas para {}".format(selected_date_str))
