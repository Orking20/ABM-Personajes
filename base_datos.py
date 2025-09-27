import sqlite3 as sql
from path import ruta_absoluta

@staticmethod
def select_habilidades():
    """Devuelve todas las habilidades básicas."""
    path = ruta_absoluta("espada_negra.db")
    conexion = sql.connect(path)
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM habilidades")
    datos = cursor.fetchall() # Recupera todas las filas seleccionadas y la devuelve como una lista de tuplas

    conexion.close()
    return datos

@staticmethod
def select_esferas():
    """Lee y devuelve las esferas guardadas en la base de datos."""
    try:
        path = ruta_absoluta("espada_negra.db")
        conexion = sql.connect(path)
        conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
        cursor = conexion.cursor()

        cursor.execute(f"SELECT * FROM esferas",) # El segundo parámetro tiene que ser una tupla
        esferas = cursor.fetchall()
        return esferas
    except sql.OperationalError as e:
        print(f"La tabla 'esferas' no existe, o no se puede abrir por falta de persmisos.")
        print(f"Error detallado: {e}")
    finally:
        conexion.close()