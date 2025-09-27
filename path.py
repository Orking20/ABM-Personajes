import os
import sys

def ruta_absoluta(nombre_archivo: str) -> str:
    """Devuelve la ruta absoluta de un archivo junto al script o al ejecutable."""
    if getattr(sys, 'frozen', False): # si está empaquetado con PyInstaller
        dir_base = os.path.dirname(sys.executable)
    else:
        dir_base = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(dir_base, nombre_archivo)