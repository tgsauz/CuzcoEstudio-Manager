class Config:
    ruta_base_datos_reservas = None
    ruta_base_datos_bandas = None

def set_rutas(ruta_base_datos_reservas, ruta_base_datos_bandas):
    Config.ruta_base_datos_reservas = ruta_base_datos_reservas
    Config.ruta_base_datos_bandas = ruta_base_datos_bandas

def get_rutas():
    print("Ruta reservas en calendar.py:", Config.ruta_base_datos_reservas, "Ruta bandas en calendar.py:", Config.ruta_base_datos_bandas)
    return (Config.ruta_base_datos_reservas, Config.ruta_base_datos_bandas)