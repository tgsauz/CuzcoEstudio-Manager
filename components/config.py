class Config:
    ruta_base_datos_reservas = None
    ruta_base_datos_bandas = None
    ruta_base_datos_consumos_listado = None

def set_rutas(ruta_base_datos_reservas, ruta_base_datos_bandas, ruta_base_datos_consumos_listado):
    Config.ruta_base_datos_reservas = ruta_base_datos_reservas
    Config.ruta_base_datos_bandas = ruta_base_datos_bandas
    Config.ruta_base_datos_consumos_listado = ruta_base_datos_consumos_listado

def get_rutas():
    return (Config.ruta_base_datos_reservas, Config.ruta_base_datos_bandas, Config.ruta_base_datos_consumos_listado)