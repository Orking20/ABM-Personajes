from pathlib import Path
import json

class Equipo:
    """Representa el equipo que lleva un personaje."""

    def __init__(self, nombre, estructura, peso):
        """Inicializa los atributos del equipo."""
        self.nombre = nombre
        self.estructura = estructura
        self.peso = peso
        self.calidad = None

    def asignar_calidad(self, calidad):
        """Asigna la calidad del equipo."""
        if calidad >= 0 and calidad <= 5:
            self.calidad = calidad
            print(f"Calidad asignada en {self.calidad} para {self.nombre}")
        else:
            print("\nEsa no es una calidad válida. La calidad mínima es de 0, y la calidad máxima es de 5.")

    @staticmethod
    def _equipo_max_longitud(sten):
        """Retorna el nombre más largo de todas las armas, armaduras y escudos."""
        arma_max_len = Arma._arma_max_longitud(sten)
        armadura_max_len = Armadura._armadura_max_longitud(sten)
        escudo_max_len = Escudo._escudo_max_longitud(sten)

        return max([arma_max_len, armadura_max_len, escudo_max_len], key=len)


class Arma(Equipo):
    """Representa un arma para usar en combate."""
    
    def __init__(self, nombre, estructura, peso, impacto, dano, alcance, tipo_dano, tipo_arma):
        """Inicializa los atributos del arma."""
        super().__init__(nombre, estructura, peso)
        #self.id = Arma._get_id() + 1
        self.impacto = impacto
        self.dano = dano
        self.alcance = alcance
        self.iniciativa = None
        self.tipo_dano = tipo_dano
        self.tipo_arma = tipo_arma

    # @staticmethod
    # def _get_id():
    #     """Devuelve el último ID de las armas guardadas, o cero si no hay armas guardadas."""
    #     lista_armas = Arma.leer_datos_armas()

    #     if lista_armas:
    #         ultima_arma = lista_armas[-1]
    #         return ultima_arma["ID"]
    #     else:
    #         return 0

    @staticmethod
    def leer_datos_armas(sten):
        """Lee los datos de las armas guardadas en el archivo JSON."""
        if sten == 1:
            archivo = "armas_sten1.json"
        elif sten == 2:
            archivo = "armas_sten2.json"
        path = Path(archivo)

        try:
            if not path.exists():
                print(f"El archivo {archivo} no existe. Puedes crearlo indicando:\nID\nNombre\nEstructura\nPeso\nImpacto\nDano\nAlcance\nIniciativa\nTipo de dano\nTipo de arma\nCalidad")
                return []

            # datos = path.read_text()
            with path.open("r", encoding="utf-8") as datos:
                return json.load(datos) # Armas en formato lista (no son objetos)
        except json.JSONDecodeError:
            print(f"El archivo {archivo} está corrupto o malformado.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}\nProbablemente el archivo esté vacío. Si es el caso puedes rellenarlo indicando:\nID\nNombre\nEstructura\nPeso\nImpacto\nDano\nAlcance\nIniciativa\nTipo de dano\nTipo de arma\nCalidad")
            return []

    @staticmethod
    def json_a_arma(sten):
        """Lee el JSON de armas y devuelve una lista con esas armas pasadas a objetos Arma."""
        armas_json = Arma.leer_datos_armas(sten)
        armas = []

        for arma_json in armas_json:
            arma = Arma(arma_json["Nombre"], arma_json["Estructura"], arma_json["Peso"], arma_json["Impacto"], arma_json["Dano"],
                        arma_json["Alcance"], arma_json["Tipo de dano"], arma_json["Tipo de arma"])
            arma.id = arma_json["ID"]
            armas.append(arma)

        return armas

    # def guardar_armas(self, armas):
    #     """Guarda las armas en un archivo JSON."""
    #     armas.append({"ID": self.id, "Nombre": self.nombre, "Estructura": self.estructura, "Peso": self.peso,
    #                 "Impacto": self.impacto, "Dano": self.dano, "Alcance": self.alcance, "Iniciativa": self.iniciativa,
    #                 "Tipo de dano": self.tipo_dano, "Tipo de arma": self.tipo_arma, "Calidad": self.calidad})

    #     path = Path("armas.json")
    #     datos = json.dumps(armas, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #     try:
    #         path.write_text(datos)
    #     except Exception as e:
    #         print(f"Error al guardar el archivo: {e}")

    # @staticmethod
    # def eliminar_arma(id):
    #     """Elimina el arma con el ID pasado por parámetro del archivo JSON."""
    #     armas = Arma.leer_datos_armas()

    #     for arma in armas:
    #         if arma["ID"] == id:
    #             armas.remove(arma)
    #             arma_encontrada = True

    #     if arma_encontrada:
    #         path = Path("armas.json")
    #         datos = json.dumps(armas, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #         try:
    #             path.write_text(datos)
    #         except Exception as e:
    #             print(f"Error al eliminar el arma: {e}")

    def convertir_a_diccionario(self):
        """Convierte un objeto Arma en diccionario."""
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Estructura": self.estructura,
            "Peso": self.peso,
            "Impacto": self.impacto,
            "Dano": self.dano,
            "Alcance": self.alcance,
            "Iniciativa": self.iniciativa,
            "Tipo de dano": self.tipo_dano,
            "Tipo de arma": self.tipo_arma,
            "Calidad": self.calidad
            }

    @staticmethod
    def _arma_max_longitud(sten):
        """Retorna el nombre más largo de todas las armas."""
        armas = Arma.json_a_arma(sten)

        palabras = []

        for arma in armas:
            palabras.append(arma.nombre)

        return max(palabras, key=len)


class Armadura(Equipo):
    """Representa un armadura para usar en combate."""

    def __init__(self, nombre, estructura, peso, contundente, cortante, perforante, cobertura, evasion, penalizador):
        """Inicializa los atributos del arma."""
        super().__init__(nombre, estructura, peso)
        #self.id = Armadura._get_id() + 1
        self.contundente = contundente
        self.cortante = cortante
        self.perforante = perforante
        self.cobertura = cobertura
        self.evasion = evasion
        self.penalizador = penalizador

    # @staticmethod
    # def _get_id():
    #     """Devuelve el último ID de las armaduras guardadas, o cero si no hay armaduras guardadas."""
    #     lista_armaduras = Armadura.leer_datos_armaduras()

    #     if lista_armaduras:
    #         ultima_armadura = lista_armaduras[-1]
    #         return ultima_armadura["ID"]
    #     else:
    #         return 0

    @staticmethod
    def leer_datos_armaduras(sten):
        """Lee los datos de las armaduras guardadas en el archivo JSON."""
        if sten == 1:
            archivo = "armaduras_sten1.json"
        elif sten == 2:
            archivo = "armaduras_sten2.json"
        path = Path(archivo)

        try:
            if not path.exists():
                print(f"El archivo {archivo} no existe. Puedes crearlo indicando:\nID\nNombre\nEstructura\nPeso\nContundente\nCortante\nPerforante\nCobertura\nEvasión\nPenalizador")
                return []

            # datos = path.read_text()
            with path.open("r", encoding="utf-8") as datos:
                return json.load(datos) # Armaduras en formato lista (no son objetos)
        except json.JSONDecodeError:
            print(f"El archivo {archivo} está corrupto o malformado.")
            return []
        except FileNotFoundError:
            print()
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}\nProbablemente el archivo esté vacío. Si es el caso puedes rellenarlo indicando:\nID\nNombre\nEstructura\nPeso\nContundente\nCortante\nPerforante\nCobertura\nEvasión\nPenalizador")
            return []

    @staticmethod
    def json_a_armadura(sten):
        """Lee el JSON de armaduras y devuelve una lista con esas armaduras pasadas a objetos Armadura."""
        armaduras_json = Armadura.leer_datos_armaduras(sten)
        armaduras = []

        for armadura_json in armaduras_json:
            armadura = Armadura(armadura_json["Nombre"], armadura_json["Estructura"], armadura_json["Peso"],
                                armadura_json["Contundente"], armadura_json["Cortante"], armadura_json["Perforante"],
                                armadura_json["Cobertura"], armadura_json["Evasión"], armadura_json["Penalizador"])
            armadura.id = armadura_json["ID"]
            armaduras.append(armadura)

        return armaduras

    # def guardar_armaduras(self, armaduras):
    #     """Guarda las armaduras en un archivo JSON."""
    #     armaduras.append({"ID": self.id, "Nombre": self.nombre, "Estructura": self.estructura, "Peso": self.peso,
    #                     "Contundente": self.contundente, "Cortante": self.cortante, "Perforante": self.perforante,
    #                     "Cobertura": self.cobertura, "Evasión": self.evasion, "Penalizador": self.penalizador})

    #     path = Path("armaduras.json")
    #     datos = json.dumps(armaduras, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #     try:
    #         path.write_text(datos)
    #     except Exception as e:
    #         print(f"Error al guardar el archivo: {e}")

    # @staticmethod
    # def eliminar_armadura(id):
    #     """Elimina el armadura con el ID pasado por parámetro del archivo JSON."""
    #     armaduras = Armadura.leer_datos_armaduras()

    #     for armadura in armaduras:
    #         if armadura["ID"] == id:
    #             armaduras.remove(armadura)
    #             armadura_encontrada = True

    #     if armadura_encontrada:
    #         path = Path("armaduras.json")
    #         datos = json.dumps(armaduras, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #         try:
    #             path.write_text(datos)
    #         except Exception as e:
    #             print(f"Error al eliminar el armadura: {e}")

    def convertir_a_diccionario(self):
        """Convierte un objeto Armadura en diccionario."""
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Estructura": self.estructura,
            "Peso": self.peso,
            "Contundente": self.contundente,
            "Cortante": self.cortante,
            "Perforante": self.perforante,
            "Cobertura": self.cobertura,
            "Evasión": self.evasion,
            "Penalizador": self.penalizador,
            "Calidad": self.calidad
            }

    @staticmethod
    def _armadura_max_longitud(sten):
        """Retorna el nombre más largo de todas las armaduras."""
        armaduras = Armadura.json_a_armadura(sten)

        palabras = []

        for armadura in armaduras:
            palabras.append(armadura.nombre)

        return max(palabras, key=len)


class Escudo(Equipo):
    """Representa un escudo para usar en combate."""

    def __init__(self, nombre, estructura, peso, contundente, cortante, perforante, cobertura, evasion, penalizador):
        """Inicializa los atributos del arma."""
        super().__init__(nombre, estructura, peso)
        #self.id = Escudo._get_id() + 1
        self.contundente = contundente
        self.cortante = cortante
        self.perforante = perforante
        self.cobertura = cobertura
        self.evasion = evasion
        self.penalizador = penalizador

    # @staticmethod
    # def _get_id():
    #     """Devuelve el último ID de los escudos guardados, o cero si no hay escudos guardados."""
    #     lista_escudos = Escudo.leer_datos_escudos()

    #     if lista_escudos:
    #         ultima_escudos = lista_escudos[-1]
    #         return ultima_escudos["ID"]
    #     else:
    #         return 0

    @staticmethod
    def leer_datos_escudos(sten):
        """Lee los datos de los escudos guardados en el archivo JSON."""
        if sten == 1:
            archivo = "escudos_sten1.json"
        elif sten == 2:
            archivo = "escudos_sten2.json"
        path = Path(archivo)

        try:
            if not path.exists():
                print(f"El archivo {archivo} no existe. Puedes crearlo indicando:\nID\nNombre\nEstructura\nPeso\nContundente\nCortante\nPerforante\nCobertura\nEvasión\nPenalizador")
                return []

            # datos = path.read_text()
            with path.open("r", encoding="utf-8") as datos:
                return json.load(datos) # Escudos en formato lista (no son objetos)
        except json.JSONDecodeError:
            print(f"El archivo {archivo} está corrupto o malformado.")
            return []
        except Exception as e:
            print(f"Error al leer el archivo: {e}\nProbablemente el archivo esté vacío. Si es el caso puedes rellenarlo indicando:\nID\nNombre\nEstructura\nPeso\nContundente\nCortante\nPerforante\nCobertura\nEvasión\nPenalizador")
            return []

    @staticmethod
    def json_a_escudo(sten):
        """Lee el JSON de escudos y devuelve una lista con esos escudos pasados a objetos Escudo."""
        escudos_json = Escudo.leer_datos_escudos(sten)
        escudos = []

        for escudo_json in escudos_json:
            escudo = Escudo(escudo_json["Nombre"], escudo_json["Estructura"], escudo_json["Peso"],
                                escudo_json["Contundente"], escudo_json["Cortante"], escudo_json["Perforante"],
                                escudo_json["Cobertura"], escudo_json["Evasión"], escudo_json["Penalizador"])
            escudo.id = escudo_json["ID"]
            escudos.append(escudo)

        return escudos

    # def guardar_escudos(self, escudos):
    #     """Guarda los escudos en un archivo JSON."""
    #     escudos.append({"ID": self.id, "Nombre": self.nombre, "Estructura": self.estructura, "Peso": self.peso,
    #                     "Contundente": self.contundente, "Cortante": self.cortante, "Perforante": self.perforante,
    #                     "Cobertura": self.cobertura, "Evasión": self.evasion, "Penalizador": self.penalizador})

    #     path = Path("escudos.json")
    #     datos = json.dumps(escudos, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #     try:
    #         path.write_text(datos)
    #     except Exception as e:
    #         print(f"Error al guardar el archivo: {e}")

    # @staticmethod
    # def eliminar_escudo(id):
    #     """Elimina el escudo con el ID pasado por parámetro del archivo JSON."""
    #     escudos = Escudo.leer_datos_escudos()

    #     for escudo in escudos:
    #         if escudo["ID"] == id:
    #             escudos.remove(escudo)
    #             escudo_encontrada = True

    #     if escudo_encontrada:
    #         path = Path("escudos.json")
    #         datos = json.dumps(escudos, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
    #         try:
    #             path.write_text(datos)
    #         except Exception as e:
    #             print(f"Error al eliminar el escudo: {e}")

    def convertir_a_diccionario(self):
        """Convierte un objeto Escudo en diccionario."""
        return {
            "ID": self.id,
            "Nombre": self.nombre,
            "Estructura": self.estructura,
            "Peso": self.peso,
            "Contundente": self.contundente,
            "Cortante": self.cortante,
            "Perforante": self.perforante,
            "Cobertura": self.cobertura,
            "Evasión": self.evasion,
            "Penalizador": self.penalizador,
            "Calidad": self.calidad
            }

    @staticmethod
    def _escudo_max_longitud(sten):
        """Retorna el nombre más largo de todos los escudos."""
        escudos = Escudo.json_a_escudo(sten)

        palabras = []

        for escudo in escudos:
            palabras.append(escudo.nombre)

        return max(palabras, key=len)