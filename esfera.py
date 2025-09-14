from pathlib import Path
import json

class Esfera:
    """Representa una esfera sobrenatural en el mundo de Espada Negra."""
    def __init__(self, nombre, poderes, pasiva):
        """Inicializa los atributos de una esfera."""
        self.id = Esfera._get_id() + 1
        self.nombre = nombre
        self.nivel = None
        self.poderes = []
        for poder in poderes:
            self.poderes.append(poder)
        self.pasiva = pasiva
        self.afinidad = None

    @staticmethod
    def leer_datos_esferas():
        """Lee los datos de las esferas guardadas en el archivo JSON."""
        path = Path("esferas.json")
        try:
            # datos = path.read_text()
            with path.open("r", encoding="utf-8") as datos:
                return json.load(datos) # Esferas en formato lista (no son objetos)
        except FileNotFoundError:
            print("El archivo esferas.json no existe.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}\nProbablemente el archivo esté vacío.")
            return []

    @staticmethod
    def json_a_esfera(sten=1):
        """Lee el JSON de armas y devuelve una lista con esas armas pasadas a objetos Arma."""
        esferas_json = Esfera.leer_datos_esferas()
        esferas = []

        for esfera_json in esferas_json:
            if sten == 1:
                esfera = Esfera(esfera_json["Nombre"], esfera_json["Poderes"], esfera_json["Pasiva"])
            elif sten == 2:
                esfera = Esfera(esfera_json["Nombre"], esfera_json["Poderes"], esfera_json["Pasiva STEN2"])
            esfera.id = esfera_json["ID"]
            esfera.nivel = esfera_json["Nivel"]
            esfera.afinidad = esfera_json["Afinidad"]
            esferas.append(esfera)

        return esferas

    @staticmethod
    def _get_id():
        """Devuelve el último ID de las esferas guardadas, o cero si no hay esferas guardadas."""
        esferas = Esfera.leer_datos_esferas()

        if esferas:
            ultima_esfera = esferas[-1]
            return ultima_esfera["ID"]
        else:
            return 0

    def convertir_a_diccionario(self):
        """Convierte un objeto Esfera en diccionario."""
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Nivel": self.nivel,
            "Poderes": self.poderes,
            "Pasiva": self.pasiva,
            "Afinidad": self.afinidad
            }


class Poder:
    """Representa un poder perteneciente a una esfera."""
    def __init__(self, nombre, descripcion, efecto, parametros):
        """Inicializa los atributos de un poder."""
        self.nombre = nombre
        self.descripcion = descripcion
        self.efecto = efecto
        self.parametros = parametros

    def convertir_a_diccionario(self):
        """Convierte un objeto Poder en diccionario."""
        return {
            "Nombre": self.nombre,
            "Descripción": self.descripcion,
            "Efecto": self.efecto,
            "Parámetros": self.parametros
            }