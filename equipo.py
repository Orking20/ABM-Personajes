from pathlib import Path
import json
import sqlite3 as sql

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

    @staticmethod
    def select_armas(sten):
        """Lee y devuelve los datos de las armas guardadas en la base de datos."""
        if sten == 1:
            version = "STEN1"
        elif sten == 2:
            version = "STEN2"

        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM armas WHERE version = ?", (version,))
            armas = cursor.fetchall()
            return armas
        except sql.OperationalError as e:
            print(f"La tabla 'armas' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def db_a_armas(sten):
        """Lee la base de datos de armas y devuelve una lista con esos personajes como objetos Arma."""
        armas_db = Arma.select_armas(sten)
        armas = []

        for arma_db in armas_db:
            arma = Arma(arma_db["nombre"], arma_db["estructura"], arma_db["peso"], arma_db["impacto"],
                        arma_db["dano"], arma_db["alcance"], arma_db["tipo_de_dano"], arma_db["tipo_de_arma"])
            arma.id = arma_db["id"]
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
        armas = Arma.db_a_armas(sten)

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

    @staticmethod
    def select_armaduras(sten):
        """Lee y devuelve los datos de las armaduras guardadas en la base de datos."""
        if sten == 1:
            version = "STEN1"
        elif sten == 2:
            version = "STEN2"

        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM armaduras WHERE version = ?", (version,))
            armaduras = cursor.fetchall()
            return armaduras
        except sql.OperationalError as e:
            print(f"La tabla 'armaduras' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def db_a_armaduras(sten):
        """Lee la base de datos de armaduras y devuelve una lista con esos personajes como objetos Armadura."""
        armaduras_db = Armadura.select_armaduras(sten)
        armaduras = []

        for armadura_db in armaduras_db:
            armadura = Armadura(armadura_db["nombre"], armadura_db["estructura"], armadura_db["peso"],
                                armadura_db["contundente"], armadura_db["cortante"], armadura_db["perforante"],
                                armadura_db["cobertura"], armadura_db["evasion"], armadura_db["penalizador"])
            armadura.id = armadura_db["id"]
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
        armaduras = Armadura.db_a_armaduras(sten)

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

    @staticmethod
    def select_escudos(sten):
        """Lee y devuelve los datos de las escudos guardadas en la base de datos."""
        if sten == 1:
            version = "STEN1"
        elif sten == 2:
            version = "STEN2"

        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM escudos WHERE version = ?", (version,))
            escudos = cursor.fetchall()
            return escudos
        except sql.OperationalError as e:
            print(f"La tabla 'escudos' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def db_a_escudos(sten):
        """Lee la base de datos de escudos y devuelve una lista con esos personajes como objetos Escudo."""
        escudos_db = Escudo.select_escudos(sten)
        escudos = []

        for escudo_db in escudos_db:
            escudo = Escudo(escudo_db["nombre"], escudo_db["estructura"], escudo_db["peso"],
                            escudo_db["contundente"], escudo_db["cortante"], escudo_db["perforante"],
                            escudo_db["cobertura"], escudo_db["evasion"], escudo_db["penalizador"])
            escudo.id = escudo_db["id"]
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
        escudos = Escudo.db_a_escudos(sten)

        palabras = []

        for escudo in escudos:
            palabras.append(escudo.nombre)

        return max(palabras, key=len)