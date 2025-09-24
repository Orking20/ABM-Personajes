from pathlib import Path
from habilidad import Habilidad
from equipo import Arma, Armadura, Escudo
from esfera import Esfera
import base_datos
from math import floor
import re
import json
import sqlite3 as sql

class Personaje:
    """Plantilla que representa cualquier personaje en Espada Negra."""
    def __init__(self):
        """Se inicializan los atributos del personaje."""
        self.id = Personaje._get_id() + 1
        self.jugador = None
        self.nombre = None
        self.sten = None
        self.rango = None # 1. Vulgar 2. Capacitado 3. Luchador 4. Héroe
        self.fuerza = None
        self.agilidad = None
        self.resistencia = None
        self.voluntad = None
        self.inteligencia = None
        self.liderazgo = None
        self.potencia = None
        self.defensa = None
        self.extension = None
        self.cant_esferas = None
        self.vida = None
        self.muerte = None
        self.aguante = None
        self.recuperacion = None
        self.iniciativa = None
        self.carga_total = None
        self.carga_en_manos = None
        self.resistencia_luz = None
        self.resistencia_oscuridad = None
        self.resistencia_elemental = None
        self.escudo_sobrenatural = None
        self.concentracion = 0
        self.aguante_actual = 0
        self.aguante_gastado_por_turno = 0
        self.vida_actual = 0
        self.dano_recibido = 0
        self.herida_grave = False
        self.turnos_aturdido = 0
        self.mod_vida = 0
        self.mod_aguante = 0
        self.mod_recuperacion = 0
        self.mod_iniciativa = 0
        self.mod_res_luz = 0
        self.mod_res_oscuridad = 0
        self.mod_res_elemental = 0
        self.mod_escudo_sobrenatural = 0
        self.habilidades = [] # Borrar JSON
        self.armas = [] # Borrar JSON
        self.armaduras = [] # Borrar JSON
        self.escudos = [] # Borrar JSON
        self.esferas = [] # Borrar JSON
        self.motivacion = 0
        self.energia = 0

    def asignar_jugador(self, nombre):
        """El usuario asigna el nombre del jugador."""
        if len(nombre) > 0:
            self.jugador = nombre
        else:
            print("El nombre del jugador no puede estar vacío.")

    def asignar_nombre(self, nombre):
        """El usuario asigna el nombre del personaje."""
        if len(nombre) > 0:
            self.nombre = nombre
        else:
            print("El nombre del personaje no puede estar vacío.")

    def asignar_sten(self, sten):
        """El usuario asigna la versión STEN que usará el personaje."""
        if sten == 1 or sten == 2:
            self.sten = sten
        else:
            print("La versión de STEN solo puede ser 1 o 2.")

    def asignar_rango(self, rango):
        """Asigna el rango al personaje."""
        primario = 6
        secundario = 5
        terciario = 5

        # Se suma el rango - 1 a los valores primarios, secundarios y terciarios
        if rango == 2 or rango == 3 or rango == 4:
            primario += rango - 1
            secundario += rango - 1
            terciario += rango - 1

        if rango >= 1 and rango <= 4:
            self.rango = rango
            return (primario, secundario, terciario)
        else:
            print("\nEl rango del personaje es inválido. Solo pueden ser números enteros entre el 1 y el 4.")

    def asignar_enfoque(self, enfoque, primario, secundario, terciario):
        """Acompaña al usuario a elegir su enfoque."""
        # Se ajustan los valores según el enfoque elegido
        if enfoque == 2:
            secundario += 1
            terciario -= 1
        elif enfoque == 3:
            primario += 1
            terciario -= 2
        elif enfoque == 4:
            primario += 1
            secundario -= 1
            terciario -= 1
        
        return (primario, secundario, terciario)

    def ascender(self):
        """Asciende el rango del personaje. Para lo cuál, el personaje ya debe estar creado."""
        if self.rango < 4:
            atributos = [("Fuerza", "Agilidad", "Resistencia"),
                        ("Voluntad", "Inteligencia", "Liderazgo"),
                        ("Potencia", "Defensa", "Extensión")]

            for atributo1, atributo2, atributo3 in atributos:
                eleccion = int(input(f"\nDebes elegir un atributo de cada bloque para subir en un punto.\n1. {atributo1}\n2. {atributo2}\n3. {atributo3}\n0. Salir\nElija un atributo para subir: "))

                if eleccion == 0:
                    return None
                elif eleccion < 0 or eleccion > 3:
                    print("Para subir un atributo debe ingresar un número entre el 1 y el 3.")
                    return None
                # Dependiendo de la elección del usuario se sube uno u otro atributo
                elif eleccion == 1:
                    valor_atributo = self._get_atributo_by_str(atributo1.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo1.lower(), valor_atributo)
                    self._actualizar_valor(self.id, atributo1, valor_atributo)
                elif eleccion == 2:
                    valor_atributo = self._get_atributo_by_str(atributo2.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo2.lower(), valor_atributo)
                    self._actualizar_valor(self.id, atributo2, valor_atributo)
                elif eleccion == 3:
                    valor_atributo = self._get_atributo_by_str(atributo3.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo3.lower(), valor_atributo)
                    self._actualizar_valor(self.id, atributo3, valor_atributo)

            self.rango += 1
            self._actualizar_valor(self.id, "Rango", self.rango)
            self.actualizar_cualidades(self.sten)
        else:
            print(f"Eres {Personaje.convertir_rango_a_str(self.rango)}! Has alcanzado el máximo rango.")

    def asignar_habilidades(self):
        """Asigna las habilidades básicas a un personaje."""
        lista_habilidades = [
            ("Escalada", ("F", "A", "R"), "Dinámica"),
            ("Escapismo", ("A"), "Dinámica"),
            ("Nadar / Bucear", ("A", "R"), "Dinámica"),
            ("Rastreo / Caza", ("I"), "Dinámica"),
            ("Robo", ("A", "I"), "Dinámica"),
            ("Sigilo", ("A", "I"), "Dinámica"),
            ("Abrir cerraduras", ("A", "I"), "Mecánica"),
            ("Hípica", ("A", "L"), "Mecánica"),
            ("Medicina", ("I"), "Mecánica"),
            ("Navegación", ("I", "L"), "Mecánica"),
            ("Orientación", ("I"), "Mecánica"),
            ("Pesca", ("A", "I"), "Mecánica"),
            ("Supervivencia", ("I"), "Mecánica"),
            ("Agricultura", ("R", "I"), "Productivas"),
            ("Ganadería", ("R", "I"), "Productivas"),
            ("Herbolaria / Recolección", ("R", "I"), "Productivas"),
            ("Minería", ("R", "I"), "Productivas"),
            ("Disfraces", ("A", "L"), "Sociales"),
            ("Docencia", ("L", "I"), "Sociales"),
            ("Engañar", ("L"), "Sociales"),
            ("Interpretar", ("A", "L"), "Sociales"),
            ("Seducir", ("L"), "Sociales"),
            ("Artes", ("I"), "Creativas"),
            ("Carpintería", ("A", "I"), "Creativas"),
            ("Cartografía", ("I"), "Creativas"),
            ("Cocina", ("I"), "Creativas"),
            ("Entrenar animales", ("L", "I"), "Creativas"),
            ("Falsificar", ("A", "I"), "Creativas"),
            ("Forja", ("R", "I"), "Creativas"),
            ("Peletería", ("A", "I"), "Creativas"),
            ("Química", ("I"), "Creativas"),
            ("Sastrería", ("A", "I"), "Creativas"),
            ("Ciencias teóricas", ("I"), "Conocimientos"),
            ("Criptografía", ("I"), "Conocimientos"),
            ("Detección", ("I"), "Conocimientos"),
            ("Finanzas", ("I"), "Conocimientos"),
            ("Historia", ("I"), "Conocimientos"),
            ("Ingeniería", ("I"), "Conocimientos"),
            ("Leyes", ("I"), "Conocimientos"),
            ("Concentración", ("D"), "Sobrenaturales"),
            ("Ritos", ("E"), "Sobrenaturales"),
            ("Combate a dos manos", ("F"), "Combate"),
            ("Combate con armas arrojadizas", ("F", "A"), "Combate"),
            ("Combate con armas de proyectiles", ("F", "A"), "Combate"),
            ("Combate con dos armas", ("A"), "Combate"),
            ("Combate con escudo", ("R"), "Combate"),
            ("Combate con un arma", ("A"), "Combate"),
            ("Manejo de alabarda", ("A", "R"), "Combate"),
            ("Manejo de espada", ("F", "A", "R"), "Combate"),
            ("Manejo de hacha", ("F", "R"), "Combate"),
            ("Manejo de lanza", ("A"), "Combate"),
            ("Manejo de mangual", ("R"), "Combate"),
            ("Manejo de maza", ("F"), "Combate"),
            ("Manejo de pico", ("F", "A"), "Combate"),
            ("Táctica", ("L"), "Combate")
        ]

        for nombre, atributos, tipo in lista_habilidades:
            self.habilidades.append(Habilidad(nombre, atributos, tipo))

    def _agregar_habilidad(self, nombre, atributos, tipo, es_esfera=False):
        """Agrega una habilidad al personaje."""
        if len(nombre) > 0 and Personaje._validar_tipo_habilidad(tipo) and Personaje._validar_atributos_habilidad(atributos):
            if es_esfera:
                nombre = f"Esfera ({nombre})"
            self.habilidades.append(Habilidad(f"{nombre}", atributos, tipo))
            self.calcular_xp_req_habilidades()
            self._guardar_habilidad()

    def _quitar_habilidad(self, nombre_hab, es_esfera=False):
        """Quita una habilidad al personaje."""
        if es_esfera:
            nombre_hab = f"Esfera ({nombre_hab})"
        i = 0
        for hab in self.habilidades:
            if i <= 55:
                if hab.nombre == nombre_hab:
                    self.habilidades.remove(hab)
                    self._guardar_habilidad()
            else:
                print("No puedes eliminar las habilidades por defecto.")
            i += 1

    @staticmethod
    def _validar_tipo_habilidad(tipo):
        """Valida el tipo de la habilidad."""
        if tipo in ("Dinámica", "Mecánica", "Productivas", "Sociales", "Creativas", "Conocimientos", "Sobrenaturales", "Combate"):
            return True
        else:
            return False

    @staticmethod
    def _validar_atributos_habilidad(atributos):
        """Valida los atributos de la habilidad."""
        for atr in atributos:
            if atr in ("F", "A", "R", "V", "I", "L", "P", "D", "E"):
                continue
            else:
                return False
        return True

    def actualizar_cualidades(self, sten):
        """Actualiza las cualidades de un personaje, como la vida, aguante, resistencia, etc."""
        self.sten = sten
        self.cant_esferas = self.extension
        self.aguante = self.resistencia * 5
        self.recuperacion = self.resistencia
        self.iniciativa = self.agilidad + self.inteligencia
        self.carga_total = self.fuerza * 5
        self.carga_en_manos = self.fuerza
        self.resistencia_luz = self.defensa
        self.resistencia_oscuridad = self.defensa
        self.resistencia_elemental = self.fuerza
        self.escudo_sobrenatural = self.voluntad + self.defensa
        self.aguante_actual = self.aguante
        if self.sten == 1:
            self.vida = self.voluntad * 3
            self.muerte = self.fuerza * 6
        elif sten == 2:
            self.vida = self.voluntad * 5
            self.muerte = self.fuerza * 10
        self.vida_actual = self.vida

    def _get_atributo_by_str(self, atributo_str):
        """Obtiene el valor del atributo pasado en string."""
        if atributo_str == "fuerza":
            return self.fuerza
        elif atributo_str == "agilidad":
            return self.agilidad
        elif atributo_str == "resistencia":
            return self.resistencia
        elif atributo_str == "voluntad":
            return self.voluntad
        elif atributo_str == "inteligencia":
            return self.inteligencia
        elif atributo_str == "liderazgo":
            return self.liderazgo
        elif atributo_str == "potencia":
            return self.potencia
        elif atributo_str == "defensa":
            return self.defensa
        elif atributo_str == "extensión":
            return self.extension

    def _set_atributo_by_str(self, atributo_str, valor):
        """Establece el nuevo valor de un atributo pasandole el atributo en string."""
        if atributo_str == "fuerza":
            self.fuerza = valor
        elif atributo_str == "agilidad":
            self.agilidad = valor
        elif atributo_str == "resistencia":
            self.resistencia = valor
        elif atributo_str == "voluntad":
            self.voluntad = valor
        elif atributo_str == "inteligencia":
            self.inteligencia = valor
        elif atributo_str == "liderazgo":
            self.liderazgo = valor
        elif atributo_str == "potencia":
            self.potencia = valor
        elif atributo_str == "defensa":
            self.defensa = valor
        elif atributo_str == "extensión":
            self.extension = valor

    def mostrar_atributos(self):
        """Muestra todos los atributos con sus respectivos valores."""
        print(f"\nFuerza: {self.fuerza}")
        print(f"Agilidad: {self.agilidad}")
        print(f"Resistencia: {self.resistencia}")
        print(f"Voluntad: {self.voluntad}")
        print(f"Inteligencia: {self.inteligencia}")
        print(f"Liderazgo: {self.liderazgo}")
        print(f"Potencia: {self.potencia}")
        print(f"Defensa: {self.defensa}")
        print(f"Extension: {self.extension}")
    
    def mostrar_cualidades(self):
        """Muestra todas las cualidades de un personaje con sus respectivos valores."""
        print(f"\nEsferas: {self.cant_esferas}")
        print(f"Vida: {self.vida}")
        print(f"Muerte: {self.muerte}")
        print(f"Aguante: {self.aguante}")
        print(f"Recuperación: {self.recuperacion}")
        print(f"Iniciativa: {self.iniciativa}")
        print(f"Carga total: {self.carga_total}")
        print(f"Carga en manos: {self.carga_en_manos}")
        print(f"Resistencia a la luz: {self.resistencia_luz}")
        print(f"Resistencia a la oscuridad: {self.resistencia_oscuridad}")
        print(f"Resistencia elemental: {self.resistencia_elemental}")
        print(f"Escudo sobrenatural: {self.escudo_sobrenatural}")

    def _calcular_xp_req(self, habilidad, id_pj=0):
        """Calcula la experiencia que se necesita para subir de nivel una habilidad."""
        id_habilidad = habilidad["id"]
        nivel = habilidad["nivel"]
        atributos = Personaje.select_habilidad_atributo(id_habilidad)
        lista_atributos = []

        for fila in atributos:
            lista_atributos.append(fila["atributo"])

        atributo_mas_bajo = self._calcular_atributo_mas_bajo(lista_atributos)
        xp_req = 5
        multiplicador = floor(nivel / atributo_mas_bajo)
        i = 0

        while i < multiplicador:
            xp_req *= 2
            i += 1
        
        nueva_xp_req = xp_req
        if id_pj != 0:
            self._update_personaje_habilidad("xp_requerida", nueva_xp_req, habilidad["id"])

    def calcular_xp_req_habilidades(self, id_pj=0):
        """Calcula la experiencia requerida para la subida de nivel de todas las habilidades."""
        habilidades = Personaje.select_personaje_habilidad(id_pj)
        for habilidad in habilidades:
            self._calcular_xp_req(habilidad, id_pj)

    def subir_nivel_habilidad(self, hab_dict, xp):
        """Sube el nivel de la habilidad."""
        pj = self.select_personaje()
        motivacion = pj[0]["motivacion"] # Se elige el primer personaje, porque en esta consulta, solo puede venir un personaje
        if motivacion - xp >= 0:
            xp_necesaria = hab_dict["xp_requerida"] - hab_dict["xp"]

            # Si se da experiencia negativa para bajar el nivel
            if xp < 0:
                self.bajar_nivel_habilidad(hab_dict, xp)
                return
            # Si la experiencía que se quiere añadir es mayor a la requerida
            elif xp > xp_necesaria:
                nueva_xp = 0
                nueva_motivacion = motivacion - xp_necesaria # Se gasta solo la experiencia que necesita para subir el nivel
                nuevo_nivel = hab_dict["nivel"] + 1
                es_esfera = re.search(r"Esfera \((.*?)\)", hab_dict["nombre"])
                if es_esfera:
                    self.subir_nivel_esfera(es_esfera.group(1))
                self._update_personaje_habilidad("nivel", nuevo_nivel, hab_dict["id"])
                self.calcular_xp_req_habilidades(self.id)
            # Si la experiencía que se quiere añadir es menor a la requerida
            elif xp < xp_necesaria:
                nueva_xp = hab_dict["xp"] + xp
                nueva_motivacion = motivacion - xp
            # Si la experiencía que se quiere añadir es igual a la requerida
            else:
                nueva_xp = 0
                nueva_motivacion = motivacion - xp
                nuevo_nivel = hab_dict["nivel"] + 1
                es_esfera = re.search(r"Esfera \((.*?)\)", hab_dict["nombre"])
                if es_esfera:
                    self.subir_nivel_esfera(es_esfera.group(1))
                self._update_personaje_habilidad("nivel", nuevo_nivel, hab_dict["id"])
                self.calcular_xp_req_habilidades(self.id)

            self._update_personaje_habilidad("xp", nueva_xp, hab_dict["id"])
            self.update_personaje("motivacion", nueva_motivacion)
        else:
            print("Necesitas más motivación para subir el nivel de esta habilidad.")

    def bajar_nivel_habilidad(self, hab_dict, xp):
        """Baja el nivel de una habilidad."""
        pj = self.select_personaje()
        nueva_motivacion = pj[0]["motivacion"] # Se elige el primer personaje, porque en esta consulta, solo puede venir un personaje
        xp_en_positivo = xp * -1 # Se pasa la xp a positivo para manejarla con más facilidad

        if hab_dict["nivel"] > 0:
            if xp_en_positivo <= hab_dict["xp"]:
                nueva_xp = hab_dict["xp"] - xp_en_positivo
                nueva_motivacion += xp_en_positivo
            # Si se pasa más xp de la que se necesita para bajar el nivel, se baja 1 nivel y la xp queda a un xp de subir
            elif xp_en_positivo > hab_dict["xp"]:
                nuevo_nivel = hab_dict["nivel"] - 1
                if hab_dict["xp"] == 0:
                    nueva_motivacion += 1
                else:
                    nueva_motivacion += hab_dict["xp"] + 1
                es_esfera = re.search(r"Esfera \((.*?)\)", hab_dict["nombre"])
                if es_esfera:
                    self.bajar_nivel_esfera(es_esfera.group(1))
                self._update_personaje_habilidad("nivel", nuevo_nivel, hab_dict["id"])
                self.calcular_xp_req_habilidades(self.id)
                # Se busca la nueva xp_requerida por la habilidad
                pj_hab = Personaje.select_personaje_habilidad(pj[0]["id"])
                for hab in pj_hab:
                    if hab["id_habilidad"] == hab_dict["id"]:
                        nueva_xp = hab["xp_requerida"] - 1
                        break
        else:
            if xp_en_positivo <= hab_dict["xp"]:
                nueva_xp = hab_dict["xp"] - xp_en_positivo
                nueva_motivacion += xp_en_positivo
            else:
                nueva_motivacion += hab_dict["xp"]
                nueva_xp = 0

        self.update_personaje("motivacion", nueva_motivacion)
        self._update_personaje_habilidad("xp", nueva_xp, hab_dict["id"])

    def subir_nivel_esfera(self, nombre):
        """Sube el nivel de una esfera."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            esf_nom = re.search(r"\((.*?)\)", fila["nombre_e"])
            if esf_nom:
                esf_nom = esf_nom.group(1)
                if esf_nom == nombre:
                    nuevo_nivel = fila["nivel"] + 1
                    self._update_personaje_esfera("nivel", nuevo_nivel, fila["id_esfera"])
                    self.calcular_afinidad()
                    break
        else: # El else en el for se ejecuta cuando termina el ciclio SOLO si no hubo un break
            print(f"No se encuentra una esfera con el nombre '{nombre}'")

    def bajar_nivel_esfera(self, nombre):
        """Sube el nivel de una esfera."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            esf_nom = re.search(r"\((.*?)\)", fila["nombre_e"])
            if esf_nom:
                esf_nom = esf_nom.group(1)
                if esf_nom == nombre:
                    nuevo_nivel = fila["nivel"] - 1
                    self._update_personaje_esfera("nivel", nuevo_nivel, fila["id_esfera"])
                    self.calcular_afinidad()
                    break
        else: # El else en el for se ejecuta cuando termina el ciclio SOLO si no hubo un break
            print(f"No se encuentra una esfera con el nombre '{nombre}'")

    def agregar_motivacion(self, motivacion):
        """Agrega la cantidad de motivación indicada al personaje."""
        self.motivacion += motivacion
        self.update_personaje("motivacion", self.motivacion)

    def quitar_motivacion(self, motivacion):
        """Sustrae la cantidad de motivación indicada al personaje."""
        if self.motivacion - motivacion >= 0:
            self.motivacion -= motivacion
            self.update_personaje("motivacion", self.motivacion)
        else:
            print("No tienes tanta motivación para quitar.")

    def agregar_energia(self, energia):
        """Agrega la cantidad de energía indicada al personaje."""
        self.energia += energia
        self.update_personaje("energia", self.energia)
        self.calcular_afinidad()

    def gastar_energia(self, energia=1):
        """Sustrae la cantidad de energía indicada al personaje."""
        if self.energia - energia >= 0:
            self.energia -= energia
            if energia == 1:
                print(f"Se gasta {energia} punto de energía")
            else:
                print(f"Se gasta {energia} puntos de energía")
            self.update_personaje("energia", self.energia)
            self.calcular_afinidad()
        else:
            if energia == 1:
                print("No tienes más energía para gastar.")
            else:
                print("No tienes tanta energía para gastar.")

    def _calcular_atributo_mas_bajo(self, atributos_char: list):
        """Calcula el atributo más bajo de los pasados por parámetros."""
        atributos = self._convertir_atr_char_a_int(atributos_char)
        return min(atributos)

    def agregar_esfera(self, id_esfera):
        """Agrega la esfera pasada por parámetros si el personaje tiene hueco para esferas."""
        if len(self.esferas) < self.cant_esferas:
            if self.sten == 1:
                esferas = Esfera.json_a_esfera()
                #clave_parametros = "Parámetros"
                #clave_efecto = "Efecto"
            elif self.sten == 2:
                esferas = Esfera.json_a_esfera(2)
                #clave_parametros = "Parámetros STEN2"
                #clave_efecto = "Efecto STEN2"
            for esfera in esferas:
                if esfera.id == id_esfera:
                    esfera.nivel = 0
                    #i = 0
                    #for poder in esfera.poderes:
                    #    esfera.poderes[i]["Parámetros"] = poder[clave_parametros]
                    #    esfera.poderes[i]["Efecto"] = poder[clave_efecto]
                    #    i += 1
                    self.esferas.append(esfera)
                    self._guardar_esfera() # Borrar JSON
                    self._agregar_habilidad(esfera.nombre, "P", "Sobrenaturales", True)
                    self.insert_personaje_esfera(esfera.id, esfera.nivel, 0)
                    return
            print("El ID de esfera pasado no existe.")
        else:
            print(f"\nNo puedes llevar más esferas. Tu número máximo de esferas es {self.cant_esferas}")

    def quitar_esfera(self, id_esfera):
        """Quita la esfera pasada por parámetros del personaje."""
        for esfera in self.esferas:
            if id_esfera == esfera.id:
                self.esferas.remove(esfera)
                self._quitar_habilidad(esfera.nombre, True)
                self._guardar_esfera()
                print("\nEsfera eliminada con éxito.")
            else:
                print(f"\nEsa esfera no se encuentra en el personaje.")

    def calcular_afinidad(self):
        """Calcula y guarda la afinidad de cada esfera del personaje."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            afinidad = min(fila["nivel"], self.energia)
            self._update_personaje_esfera("afinidad", afinidad, fila["id_esfera"])

    def equipar_arma(self, arma):
        """Equipa el arma pasada por argumento al personaje."""
        self.armas.append(arma)
        arma.iniciativa = arma.alcance + self.agilidad + self.inteligencia
        arma.asignar_calidad(1)
        self.insert_personaje_arma(arma.id, arma.iniciativa, arma.calidad)
        arma.id = Personaje._get_ultimo_id_equipo_de_personaje(self.armas) # Borrar JSON
        self._guardar_equipamento("Armas", self.armas) # Borrar JSON

    def equipar_armadura(self, armadura):
        """Equipa la armadura pasada por argumento al personaje."""
        self.armaduras.append(armadura)
        armadura.asignar_calidad(1)
        self.insert_personaje_armadura(armadura.id, armadura.calidad)
        armadura.id = Personaje._get_ultimo_id_equipo_de_personaje(self.armaduras) # Borrar JSON
        self._guardar_equipamento("Armaduras", self.armaduras) # Borrar JSON

    def equipar_escudo(self, escudo):
        """Equipa el escudo pasado por argumento al personaje."""
        self.escudos.append(escudo)
        escudo.asignar_calidad(1)
        self.insert_personaje_escudo(escudo.id, escudo.calidad)
        escudo.id = Personaje._get_ultimo_id_equipo_de_personaje(self.escudos) # Borrar JSON
        self._guardar_equipamento("Escudos", self.escudos) # Borrar JSON

    def desequipar_arma(self, arma):
        """Desequipa el arma pasada por argumento al personaje."""
        armas = Personaje.select_personaje_arma(self.id)
        for arma_pj in armas:
            if arma.id == arma_pj["id_pj_arma"]:
                Personaje.delete_personaje_arma(arma.id)
                print("Arma desequipada")
                break

    def desequipar_armadura(self, armadura):
        """Desequipa la armadura pasada por argumento al personaje."""
        armaduras = Personaje.select_personaje_armadura(self.id)
        for armadura_pj in armaduras:
            if armadura.id == armadura_pj["id_pj_armadura"]:
                Personaje.delete_personaje_armadura(armadura.id)
                print("Armadura desequipada")
                break

    def desequipar_escudo(self, escudo):
        """Desequipa el escudo pasado por argumento al personaje."""
        escudos = Personaje.select_personaje_escudo(self.id)
        for escudo_pj in escudos:
            if escudo.id == escudo_pj["id_pj_escudo"]:
                Personaje.delete_personaje_escudo(escudo.id)
                print("Escudo desequipado")
                break

    def cambiar_calidad_objeto(self, id_equipo, tipo_equipo, nueva_calidad):
        """Cambia la calidad de cualquier equipo: arma, armadura o escudo."""
        if nueva_calidad >= 0 or nueva_calidad <= 5:
            if tipo_equipo == "Armas":
                arma = self.id_a_arma(id_equipo)
                arma.calidad = nueva_calidad
                self._aplicar_efecto_calidad_arma(arma)
                self._actualizar_valor_equipo(self.id, arma, "Armas", "Calidad", nueva_calidad)
            elif tipo_equipo == "Armaduras":
                armadura = self.id_a_armadura(id_equipo)
                armadura.calidad = nueva_calidad
                self._aplicar_efecto_calidad_armadura(armadura)
                self._actualizar_valor_equipo(self.id, armadura, "Armaduras", "Calidad", nueva_calidad)
            elif tipo_equipo == "Escudos":
                escudo = self.id_a_escudo(id_equipo)
                escudo.calidad = nueva_calidad
                self._aplicar_efecto_calidad_escudo(escudo)
                self._actualizar_valor_equipo(self.id, escudo, "Escudos", "Calidad", nueva_calidad)
        else:
            print("La calidad del equipo no puede ser inferior a cero ni mayor a cinco.")

    def _aplicar_efecto_calidad_arma(self, arma):
        """Aplica el efecto en el arma según la calidad."""
        armas_json = Arma.leer_datos_armas(self.sten)
        for arma_json in armas_json:
            if arma.nombre == arma_json["Nombre"]:
                i = -1
                while i < arma.calidad - 1:
                    i += 1

                arma.estructura = arma_json["Estructura"] + i
                if self.sten == 2:
                    arma.iniciativa = arma_json["Alcance"] + self.agilidad + self.inteligencia + i
                    self._actualizar_valor_equipo(self.id, arma, "Armas", "Iniciativa", arma.iniciativa)

                self._actualizar_valor_equipo(self.id, arma, "Armas", "Estructura", arma.estructura)
                return

    def _aplicar_efecto_calidad_armadura(self, armadura):
        """Aplica el efecto en la armadura según la calidad."""
        armaduras_json = Armadura.leer_datos_armaduras(self.sten)
        for armadura_json in armaduras_json:
            if armadura.nombre == armadura_json["Nombre"]:
                i = -1
                j = 1
                while i < armadura.calidad - 1:
                    i += 1
                    j -= 1

                armadura.estructura = armadura_json["Estructura"] + i
                armadura.peso = armadura_json["Peso"] + j

                self._actualizar_valor_equipo(self.id, armadura, "Armaduras", "Estructura", armadura.estructura)
                self._actualizar_valor_equipo(self.id, armadura, "Armaduras", "Peso", armadura.peso)
                return

    def _aplicar_efecto_calidad_escudo(self, escudo):
        """Aplica el efecto en la escudo según la calidad."""
        escudos_json = Escudo.leer_datos_escudos(self.sten)
        for escudo_json in escudos_json:
            if escudo.nombre == escudo_json["Nombre"]:
                i = -1
                while i < escudo.calidad - 1:
                    i += 1

                escudo.estructura = escudo_json["Estructura"] + i

                self._actualizar_valor_equipo(self.id, escudo, "Escudos", "Estructura", escudo.estructura)
                return

    def cambiar_cualidad_arma(self, id_arma, operador, columna, valor):
        """Cambia una cualidad de un arma. operador 1: Suma. operador 2: resta"""
        armas = Personaje.select_personaje_arma(self.id)

        for arma in armas:
            if arma["id_pj_arma"] == id_arma:
                existe = True
                cualidad = arma[columna]
                break
        else:
            existe = False

        if existe:
            if operador == 1: # Suma
                nuevo_valor = cualidad + valor
            elif operador == 2: # Resta
                nuevo_valor = cualidad - valor
                if nuevo_valor < 0:
                    print(f"\n\033[31mEl nuevo valor de tu cualidad no puede estar por debajo de cero.\033[0m") # Se pinta de color rojo
                    return
            else:
                print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
                return

            Personaje._update_personaje_equipo("personaje_arma", id_arma, columna, nuevo_valor)
        else:
            print("Ese ID de arma no existe, o no corresponde con el personaje.")

    def cambiar_cualidad_armadura(self, id_armadura, operador, columna, valor):
        """Cambia una cualidad de una armadura. operador 1: Suma. operador 2: resta"""
        armaduras = Personaje.select_personaje_armadura(self.id)

        for armadura in armaduras:
            if armadura["id_pj_armadura"] == id_armadura:
                existe = True
                cualidad = armadura[columna]
                break
        else:
            existe = False

        if existe:
            if operador == 1: # Suma
                nuevo_valor = cualidad + valor
            elif operador == 2: # Resta
                nuevo_valor = cualidad - valor
                if nuevo_valor < 0:
                    print(f"\n\033[31mEl nuevo valor de tu cualidad no puede estar por debajo de cero.\033[0m") # Se pinta de color rojo
                    return
            else:
                print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
                return

            Personaje._update_personaje_equipo("personaje_armadura", id_armadura, columna, nuevo_valor)
        else:
            print("Ese ID de armadura no existe, o no corresponde con el personaje.")

    def cambiar_cualidad_escudo(self, id_escudo, operador, columna, valor):
        """Cambia una cualidad de un escudo. operador 1: Suma. operador 2: resta"""
        escudos = Personaje.select_personaje_escudo(self.id)

        for escudo in escudos:
            if escudo["id_pj_escudo"] == id_escudo:
                existe = True
                cualidad = escudo[columna]
                break
        else:
            existe = False

        if existe:
            if operador == 1: # Suma
                nuevo_valor = cualidad + valor
            elif operador == 2: # Resta
                nuevo_valor = cualidad - valor
                if nuevo_valor < 0:
                    print(f"\n\033[31mEl nuevo valor de tu cualidad no puede estar por debajo de cero.\033[0m") # Se pinta de color rojo
                    return
            else:
                print("\n\033[31mOperador inválido. El operador tiene que ser 1 para suma, o 2 para resta.\033[0m")
                return

            Personaje._update_personaje_equipo("personaje_escudo", id_escudo, columna, nuevo_valor)
        else:
            print("Ese ID de escudo no existe, o no corresponde con el personaje.")

    def modificador_vida(self, operador, valor):
        """Cambia el modificador a la vida del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_vida += valor
            self.vida += valor
            self.vida_actual += valor
        elif operador == 2: # Resta
            self.mod_vida -= valor
            self.vida -= valor
            self.vida_actual -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador vida", self.mod_vida)
        self._actualizar_valor(self.id, "Vida", self.vida)

    def modificador_aguante(self, operador, valor):
        """Cambia el modificador al aguante del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_aguante += valor
            self.aguante += valor
            self.aguante_actual += valor
        elif operador == 2: # Resta
            self.mod_aguante -= valor
            self.aguante -= valor
            self.aguante_actual -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador aguante", self.mod_aguante)
        self._actualizar_valor(self.id, "Aguante", self.aguante)

    def modificador_recuperacion(self, operador, valor):
        """Cambia el modificador a la recuperación del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_recuperacion += valor
            self.recuperacion += valor
        elif operador == 2: # Resta
            self.mod_recuperacion -= valor
            self.recuperacion -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador recuperación", self.mod_recuperacion)
        self._actualizar_valor(self.id, "Recuperación", self.mod_recuperacion)

    def modificador_iniciativa(self, operador, valor):
        """Cambia el modificador a la iniciativa del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_iniciativa += valor
            self.iniciativa += valor
        elif operador == 2: # Resta
            self.mod_iniciativa -= valor
            self.iniciativa -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador iniciativa", self.mod_iniciativa)
        self._actualizar_valor(self.id, "Iniciativa", self.iniciativa)

    def modificador_luz(self, operador, valor):
        """Cambia el modificador a la resistencia a la luz del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_luz += valor
            self.resistencia_luz += valor
        elif operador == 2: # Resta
            self.mod_res_luz -= valor
            self.resistencia_luz -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador luz", self.mod_res_luz)
        self._actualizar_valor(self.id, "Resistencia a la luz", self.resistencia_luz)

    def modificador_oscuridad(self, operador, valor):
        """Cambia el modificador a la resistencia a la oscuridad del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_oscuridad += valor
            self.resistencia_oscuridad += valor
        elif operador == 2: # Resta
            self.mod_res_oscuridad -= valor
            self.resistencia_oscuridad -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador oscuridad", self.mod_res_oscuridad)
        self._actualizar_valor(self.id, "Resistencia a la oscuridad", self.resistencia_oscuridad)

    def modificador_elemental(self, operador, valor):
        """Cambia el modificador a la resistencia elemental del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_elemental += valor
            self.resistencia_elemental += valor
        elif operador == 2: # Resta
            self.mod_res_elemental -= valor
            self.resistencia_elemental -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador elemental", self.mod_res_elemental)
        self._actualizar_valor(self.id, "Resistencia elemental", self.resistencia_elemental)

    def modificador_escudo_sobrenatural(self, operador, valor):
        """Cambia el modificador al escudo sobrenatural del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_escudo_sobrenatural += valor
            self.escudo_sobrenatural += valor
        elif operador == 2: # Resta
            self.mod_escudo_sobrenatural -= valor
            self.escudo_sobrenatural -= valor
        else:
            print("Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.")
            return

        self._actualizar_valor(self.id, "Modificador escudo sobrenatural", self.mod_escudo_sobrenatural)
        self._actualizar_valor(self.id, "Escudo sobrenatural", self.escudo_sobrenatural)

    def gastar_aguante(self):
        """Le resta un punto de aguante al personaje si puede."""
        if self.aguante_gastado_por_turno < self.resistencia:
            if self.aguante_actual - 1 >= 0:
                self.aguante_actual -= 1
                self.aguante_gastado_por_turno += 1
                print("Aguante -1")
            else:
                print(f"\nYa no te queda aguante para gastar.")
        else:
            print("No puedes gastar más puntos de aguante que tu resistencia por turno.")

        self._actualizar_valor(self.id, "Aguante actual", self.aguante_actual)
        self._actualizar_valor(self.id, "Aguante gastado por turno", self.aguante_gastado_por_turno)

    def recuperar_aguante(self, recuperacion):
        """Recupera tantos puntos de aguante al personaje como los pasados por parámetro, hasta un máximo como su aguante total."""
        if self.aguante_actual + recuperacion <= self.aguante:
            self.aguante_actual += recuperacion
            print(f"Aguante +{recuperacion}")
        else:
            self.aguante_actual = self.aguante
            print("Aguante recuperado completamente")

        self._actualizar_valor(self.id, "Aguante actual", self.aguante_actual)

    def recibir_dano(self, dano):
        """Recibe el daño y lo ve reflejado en su vida actual, en si queda aturdido y en si recibe heridas."""
        self.vida_actual -= dano
        self.dano_recibido += dano
        print(f"Vida -{dano}")

        if dano > self.voluntad * 2:
            self.turnos_aturdido = 2
            self.concentracion = 0
            print(f"Quedas aturdido este turno y el siguiente, y pierdes todos los puntos de concentración.")
            self._actualizar_valor(self.id, "Turnos aturdido", self.turnos_aturdido)
            self._actualizar_valor(self.id, "Concentración", self.concentracion)
        elif dano > self.voluntad:
            self.turnos_aturdido = 1
            print(f"Quedas aturdido este turno.")
            concentracion_perdida = dano - self.voluntad
            if self.concentracion > 0 and concentracion_perdida > 0:
                self.perder_concentracion(concentracion_perdida)
            self._actualizar_valor(self.id, "Turnos aturdido", self.turnos_aturdido)

        if dano > self.fuerza * 3 and self.sten == 1:
            print("A elección del atacante:\nBrazo: -2 daño, -1 vida por turno\nPierna: -6 iniciativa, -1 vida por turno\nTorso o cabeza: -6 aguante, -1 vida por turno\nSi el golpe fue en un brazo o una pierna, la extremidad se verá comprometida y no podrá utilizarse.")
            self.herida_grave = True
            self._actualizar_valor(self.id, "Herida grave", self.herida_grave)
        elif dano > self.fuerza * 3 and self.sten == 2:
            print("A elección del atacante: Pierde un punto del atributo a todos los efectos. -1 vida por turno\nSi el atributo dañado es fuerza o agilidad, respectivamente un brazo o una pierna se verá comprometido y no podrá utilizarse. Una vez se recupere, pierde un punto del atributo solamente con uno de los aspectos de dicho atributo (a elección del atacante).")
            self.herida_grave = True
            self._actualizar_valor(self.id, "Herida grave", self.herida_grave)
        elif dano > self.fuerza * 2 and self.sten == 1:
            print("A elección del atacante:\nBrazo: -1 daño\nPierna: -3 iniciativa\nTorso o cabeza: -3 aguante")
        elif dano > self.fuerza * 2 and self.sten == 2:
            print("A elección del atacante: El personaje pierde un punto del atributo en relación con únicamente uno de los aspectos de dicho atributo, hasta que recibe cirugía médica.")

        if self.vida_actual <= 0:
            self.vida_actual = 0
            print(f"{self.nombre} cae inconsciente. Sus puntos de vida llegaron a cero.")

        if self.dano_recibido >= self.muerte:
            print(f"{self.nombre} muere.")

        self._actualizar_valor(self.id, "Vida actual", self.vida_actual)
        self._actualizar_valor(self.id, "Dano recibido", self.dano_recibido)

    def recuperar_vida(self, puntos_restaurar):
        """Recupera los puntos de vida pasados por parámetros y los refleja en su vida actual."""
        if self.vida_actual + puntos_restaurar <= self.vida:
            self.vida_actual += puntos_restaurar
            self.dano_recibido -= puntos_restaurar
            print(f"Vida +{puntos_restaurar}")
        else:
            self.vida_actual = self.vida
            self.dano_recibido = 0
            print("Vida restaurada completamente")

        self._actualizar_valor(self.id, "Vida actual", self.vida_actual)
        self._actualizar_valor(self.id, "Dano recibido", self.dano_recibido)

    def curar_herida_grave(self):
        """Cura una herida grave en caso de tenerla."""
        if self.herida_grave:
            self.herida_grave = False
            print("Herida curada.")
            self._actualizar_valor(self.id, "Herida grave", self.herida_grave)
        else:
            print(f"{self.nombre} no tiene ninguna herida grave.")

    def ganar_concentracion(self, puntos_concentracion):
        """Gana los puntos de concentración pasados por parámetros."""
        self.concentracion += puntos_concentracion
        print(f"Concentración +{puntos_concentracion}")
        self._actualizar_valor(self.id, "Concentración", self.concentracion)

    def perder_concentracion(self, puntos_concentracion):
        """Pierde los puntos de concentración pasados por parámetros."""
        if self.concentracion - puntos_concentracion >= 0:
            self.concentracion -= puntos_concentracion
        else:
            self.concentracion = 0
        print(f"Concentración -{puntos_concentracion}")
        self._actualizar_valor(self.id, "Concentración", self.concentracion)

    def ronda_nueva(self):
        """Se encarga de retirar aturdimiento y aguante usado por turno del personaje en caso de tenerlo."""
        if self.aguante_gastado_por_turno > 0:
            self.aguante_gastado_por_turno = 0
            self._actualizar_valor(self.id, "Aguante gastado por turno", self.aguante_gastado_por_turno)

        if self.turnos_aturdido > 0:
            self.turnos_aturdido -= 1
            print("Turnos aturdidos -1")
            self._actualizar_valor(self.id, "Turnos aturdido", self.turnos_aturdido)

        if self.herida_grave:
            self.recibir_dano(1)

    def _convertir_atr_char_a_int(self, atributos_char: list):
        """Convierte una lista de atributos con caracteres al valor numérico de dicho atributo"""
        atributos = []
        if 'F' in atributos_char:
            atributos.append(self.fuerza)
        if 'A' in atributos_char:
            atributos.append(self.agilidad)
        if 'R' in atributos_char:
            atributos.append(self.resistencia)
        if 'V' in atributos_char:
            atributos.append(self.voluntad)
        if 'I' in atributos_char:
            atributos.append(self.inteligencia)
        if 'L' in atributos_char:
            atributos.append(self.liderazgo)
        if 'P' in atributos_char:
            atributos.append(self.potencia)
        if 'D' in atributos_char:
            atributos.append(self.defensa)
        if 'E' in atributos_char:
            atributos.append(self.extension)
        
        return atributos

    @staticmethod
    def convertir_rango_a_str(rango_pj):
        """Convierte el rango numérico del personaje en string."""
        # 1. Vulgar 2. Capacitado 3. Luchador 4. Héroe
        if rango_pj == 1:
            return "Vulgar"
        elif rango_pj == 2:
            return "Capacitado"
        elif rango_pj == 3:
            return "Luchador"
        elif rango_pj == 4:
            return "Héroe"

    def id_a_arma(self, id): # Borrar JSON
        """Mediante el ID de arma, consigue y devuelve un objeto Arma."""
        for arma in self.armas:
            if id == arma.id:
                return arma
        print(f"Arma con ID {id} no encontrada.")

    def id_a_armadura(self, id): # Borrar JSON
        """Mediante el ID de armadura, consigue y devuelve un objeto Armadura."""
        for armadura in self.armaduras:
            if id == armadura.id:
                return armadura
        print(f"Armadura con ID {id} no encontrada.")

    def id_a_escudo(self, id): # Borrar JSON
        """Mediante el ID de escudo, consigue y devuelve un objeto Escudo."""
        for escudo in self.escudos:
            if id == escudo.id:
                return escudo
        print(f"Escudo con ID {id} no encontrado.")

    @staticmethod
    def leer_datos_personajes(): # Borrar JSON
        """Lee los datos de los personajes guardados en el archivo JSON."""
        path = Path("personajes.json")
        try:
            if not path.exists():
                print("El archivo personajes.json no existe. Crea tu primer personaje para crearlo automáticamente.")
                return []
            
            if path.stat().st_size == 0:
                # El archivo existe pero está vacío
                return []

            # datos = path.read_text()
            with path.open("r", encoding="utf-8") as datos:
                return json.load(datos) # Personajes en formato lista (no son objetos)
        except json.JSONDecodeError:
            print("El archivo personajes.json está corrupto o malformado.")
            return []
        except Exception as e:
            print(f"Error inesperado al leer el archivo: {e}")
            return []

    @staticmethod
    def select_personajes():
        """Lee y devuelve los datos de los personajes guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM personajes")
            personajes = cursor.fetchall()
            return personajes
        except sql.OperationalError as e:
            print(f"La tabla de personajes no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def select_personaje(self):
        """Lee y devuelve los datos de los personajes guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM personajes WHERE id = ?", (self.id,))
            personaje = cursor.fetchall()
            return personaje
        except sql.OperationalError as e:
            print(f"La tabla de personajes no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_personaje_habilidad(id_personaje):
        """Lee y devuelve las habilidades de un personaje guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"""
                            SELECT h.id, h.nombre, h.tipo,
                            ph.id_habilidad, ph.nivel, ph.xp, ph.xp_requerida
                            FROM personaje_habilidad ph
                            JOIN habilidades h ON ph.id_habilidad = h.id
                            WHERE ph.id_personaje = ?
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            habilidades = cursor.fetchall()
            return habilidades
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_habilidad_atributo(id_habilidad):
        """Lee y devuelve los atributos de habilidades guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"SELECT * FROM habilidad_atributo WHERE id_habilidad = (?)", (id_habilidad,))
            atributos = cursor.fetchall()
            return atributos
        except sql.OperationalError as e:
            print(f"La tabla 'habilidad_atributo' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_personaje_arma(id_personaje):
        """Lee y devuelve las armas de un personaje guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"""
                            SELECT a.id, a.nombre, a.peso, a.alcance,
                            a.tipo_de_dano, a.tipo_de_arma, a.version,
                            pa.id AS id_pj_arma, pa.estructura, pa.impacto, pa.dano,
                            pa.iniciativa, pa.calidad
                            FROM personaje_arma pa
                            JOIN armas a ON pa.id_arma = a.id
                            WHERE pa.id_personaje = ?;
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            armas = cursor.fetchall()
            return armas
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_personaje_armadura(id_personaje):
        """Lee y devuelve las armaduras de un personaje guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"""
                            SELECT a.id, a.nombre, a.version, a.penalizador,
                            pa.id AS id_pj_armadura, pa.estructura, pa.peso, pa.contundente, pa.cortante,
                            pa.perforante, pa.cobertura, pa.evasion, pa.calidad
                            FROM personaje_armadura pa
                            JOIN armaduras a ON pa.id_armadura = a.id
                            WHERE pa.id_personaje = ?;
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            armaduras = cursor.fetchall()
            return armaduras
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_personaje_escudo(id_personaje):
        """Lee y devuelve los escudos de un personaje guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"""
                            SELECT e.id, e.nombre, e.peso, e.penalizador, e.version,
                            pe.id AS id_pj_escudo, pe.estructura, pe.contundente, pe.cortante,
                            pe.perforante, pe.cobertura, pe.evasion, pe.calidad
                            FROM personaje_escudo pe
                            JOIN escudos e ON pe.id_escudo = e.id
                            WHERE pe.id_personaje = ?;
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            escudos = cursor.fetchall()
            return escudos
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def select_personaje_esfera(id_personaje):
        """Lee y devuelve los esferas de un personaje guardados en la base de datos."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row # Devuelve diccionario en vez de tupla
            cursor = conexion.cursor()

            cursor.execute(f"""
                            SELECT e.id, e.nombre AS nombre_e, e.pasiva_sten1, e.pasiva_sten2,
                            pe.nivel, pe.afinidad,
                            p.nombre AS nombre_p, p.descripcion, p.efecto_sten1, p.efecto_sten2,
                            prm.version, prm.nombre AS nombre_prm, prm.valor
                            FROM personaje_esfera pe
                            JOIN esferas e ON pe.id_esfera = e.id
                            JOIN poderes p ON e.id = p.id_esfera
                            LEFT JOIN parametros prm ON p.id = prm.id_poder
                            WHERE pe.id_personaje = ?
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            esferas = cursor.fetchall()
            return esferas
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def guardar_personajes(self, personajes, pj_nuevo=True):
        """Guarda los personajes en un archivo JSON."""
        if pj_nuevo:
            personajes.append({"ID": self.id, "Jugador": self.jugador, "Nombre": self.nombre, "STEN": self.sten, "Rango": self.rango,
                        "Fuerza": self.fuerza, "Agilidad": self.agilidad, "Resistencia": self.resistencia,
                        "Voluntad": self.voluntad, "Inteligencia": self.inteligencia, "Liderazgo": self.liderazgo,
                        "Potencia": self.potencia, "Defensa": self.defensa, "Extensión": self.extension,
                        "Cantidad Esferas": self.cant_esferas, "Vida": self.vida, "Vida actual": self.vida_actual,
                        "Dano recibido": self.dano_recibido, "Herida grave": self.herida_grave, "Muerte": self.muerte,
                        "Aguante": self.aguante, "Aguante actual": self.aguante_actual,
                        "Aguante gastado por turno": self.aguante_gastado_por_turno, "Recuperación": self.recuperacion,
                        "Iniciativa": self.iniciativa, "Carga total": self.carga_total, "Carga en manos": self.carga_en_manos,
                        "Resistencia a la luz": self.resistencia_luz, "Resistencia a la oscuridad": self.resistencia_oscuridad,
                        "Resistencia elemental": self.resistencia_elemental, "Escudo sobrenatural": self.escudo_sobrenatural,
                        "Concentración": self.concentracion, "Turnos aturdido": self.turnos_aturdido,
                        "Modificador vida": self.mod_vida, "Modificador aguante": self.mod_aguante,
                        "Modificador recuperación": self.mod_recuperacion, "Modificador iniciativa": self.mod_iniciativa,
                        "Modificador luz": self.mod_res_luz, "Modificador oscuridad": self.mod_res_oscuridad,
                        "Modificador elemental": self.mod_res_elemental,
                        "Modificador escudo sobrenatural": self.mod_escudo_sobrenatural, "Motivación": self.motivacion,
                        "Energía": self.energia,
                        "Habilidades": [habilidad.convertir_a_diccionario() for habilidad in self.habilidades],
                        "Armas": [arma.convertir_a_diccionario() for arma in self.armas],
                        "Armaduras": [armadura.convertir_a_diccionario() for armadura in self.armaduras],
                        "Escudos": [escudo.convertir_a_diccionario() for escudo in self.escudos],
                        "Esferas": [esfera.convertir_a_diccionario() for esfera in self.esferas]})

        path = Path("personajes.json")
        datos = json.dumps(personajes, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
        try:
            path.write_text(datos)
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def insert_personaje(self):
        """Inserta un personaje nuevo en la tabla."""
        habilidades = base_datos.select_habilidades()
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"""
                        INSERT INTO personajes
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                           ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                           ?, ?)""", (self.id, self.jugador, self.nombre, self.sten, self.rango,
                        self.fuerza, self.agilidad, self.resistencia, self.voluntad,
                        self.inteligencia, self.liderazgo, self.potencia, self.defensa,
                        self.extension, self.cant_esferas, self.vida, self.vida_actual,
                        self.dano_recibido, self.herida_grave, self.muerte, self.aguante,
                        self.aguante_actual, self.aguante_gastado_por_turno, self.recuperacion,
                        self.iniciativa, self.carga_total, self.carga_en_manos,
                        self.resistencia_luz, self.resistencia_oscuridad,
                        self.resistencia_elemental, self.escudo_sobrenatural, self.concentracion,
                        self.turnos_aturdido, self.mod_vida, self.mod_aguante,
                        self.mod_recuperacion, self.mod_iniciativa, self.mod_res_luz,
                        self.mod_res_oscuridad, self.mod_res_elemental,
                        self.mod_escudo_sobrenatural, self.motivacion, self.energia))

            for hab in habilidades:
                cursor.execute(f"""INSERT INTO personaje_habilidad VALUES (?, ?, ?, ?, ?)""", (self.id, hab [0], 0, 0, 5))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personajes' o 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def update_personaje(self, clave, valor):
        """Actualiza un campo del personaje según el valor pasado."""
        columnas_validas = ("rango", "fuerza", "agilidad", "resistencia", "voluntad", "inteligencia",
                            "liderazgo", "potencia", "defensa", "extension", "cantidad_esferas",
                            "vida", "vida_actual", "dano_recibido", "herida_grave", "muerte",
                            "aguante", "aguante_actual", "aguante_gastado_por_turno", "recuperacion",
                            "iniciativa", "carga_total", "carga_en_manos", "resistencia_a_la_luz",
                            "resistencia_a_la_oscuridad", "resistencia_elemental",
                            "escudo_sobrenatural", "concentracion", "modificador_vida",
                            "modificador_aguante", "modificador_recuperacion",
                            "modificador_iniciativa", "modificador_luz", "modificador_oscuridad",
                            "modificador_elemental", "modificador_escudo_sobrenatural",
                            "motivacion", "energia")

        if clave not in columnas_validas:
            print("Esa columna no se puede modificar.")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personajes SET {clave} = ? WHERE id = ?", (valor, self.id))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"La tabla 'personajes' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def _update_personaje_equipo(tabla, id, columna, valor):
        """Actualiza un campo de la tabla personaje_esfera según el valor pasado."""
        tablas_validas = ("personaje_arma", "personaje_armadura", "personaje_escudo")

        if tabla not in tablas_validas:
            print("Esa tabla no se puede modificar.")
            return

        match tabla:
            case "personaje_arma":
                columnas_validas = ("estructura", "impacto", "dano", "calidad")
            case "personaje_armadura":
                columnas_validas = ("estructura", "peso", "contundente", "cortante",
                                    "perforante", "cobertura", "evasion", "calidad")
            case "personaje_escudo":
                columnas_validas = ("estructura", "contundente", "cortante", "perforante",
                                    "cobertura", "evasion", "calidad")

        if columna not in columnas_validas:
            print(f"La columna '{columna}' no se puede modificar.")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE {tabla} SET {columna} = ? WHERE id = ?",
                           (valor, id))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"La tabla '{tabla}' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def _update_personaje_esfera(self, clave, valor, id_esfera):
        """Actualiza un campo de la tabla personaje_esfera según el valor pasado."""
        columnas_validas = ("nivel", "afinidad")

        if clave not in columnas_validas:
            print("Esa columna no se puede modificar.")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personaje_esfera SET {clave} = ? WHERE id_personaje = ? AND id_esfera = ?",
                           (valor, self.id, id_esfera))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def _update_personaje_habilidad(self, clave, valor, id_habilidad):
        """Actualiza un campo de la tabla personaje_habilidad según el valor pasado."""
        columnas_validas = ("nivel", "xp", "xp_requerida")

        if clave not in columnas_validas:
            print("Esa columna no se puede modificar.")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personaje_habilidad SET {clave} = ? WHERE id_personaje = ? AND id_habilidad = ?",
                           (valor, self.id, id_habilidad))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def insert_personaje_arma(self, id_arma, iniciativa, calidad):
        """Inserta un arma a un personaje en la tabla personaje_arma."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row
            cursor = conexion.cursor()

            cursor.execute(f"""SELECT * FROM armas WHERE id = (?)""", (id_arma,))
            datos = cursor.fetchall()
            arma = dict(datos[0])
            cursor.execute(f"""INSERT INTO personaje_arma
                           (id_personaje, id_arma, estructura, impacto, dano, iniciativa, calidad)
                           VALUES (?, ?, ?, ?, ?, ?, ?)""",
                           (self.id, id_arma, arma["estructura"], arma["impacto"], arma["dano"],
                            iniciativa, calidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def insert_personaje_armadura(self, id_armadura, calidad):
        """Inserta un armadura a un personaje en la tabla personaje_armadura."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row
            cursor = conexion.cursor()

            cursor.execute(f"""SELECT * FROM armaduras WHERE id = (?)""", (id_armadura,))
            datos = cursor.fetchall()
            armadura = dict(datos[0])
            cursor.execute(f"""INSERT INTO personaje_armadura
                           (id_personaje, id_armadura, estructura, peso, contundente,
                           cortante, perforante, cobertura, evasion, calidad)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (self.id, id_armadura, armadura["estructura"], armadura["peso"],
                            armadura["contundente"], armadura["cortante"], armadura["perforante"],
                            armadura["cobertura"], armadura["evasion"], calidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def insert_personaje_escudo(self, id_escudo, calidad):
        """Inserta un escudo a un personaje en la tabla personaje_escudo."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            conexion.row_factory = sql.Row
            cursor = conexion.cursor()

            cursor.execute(f"""SELECT * FROM escudos WHERE id = (?)""", (id_escudo,))
            datos = cursor.fetchall()
            escudo = dict(datos[0])
            cursor.execute(f"""INSERT INTO personaje_escudo
                           (id_personaje, id_escudo, estructura, contundente,
                           cortante, perforante, cobertura, evasion, calidad)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (self.id, id_escudo, escudo["estructura"], escudo["contundente"],
                            escudo["cortante"], escudo["perforante"], escudo["cobertura"],
                            escudo["evasion"], calidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def insert_personaje_esfera(self, id_esfera, nivel, afinidad):
        """Inserta un esfera a un personaje en la tabla personaje_esfera."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"""INSERT INTO personaje_esfera VALUES (?, ?, ?, ?)""",
                           (self.id, id_esfera, nivel, afinidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def delete_personaje_arma(id_arma):
        """Elimina el arma seleccionada de las armas del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_arma WHERE id = ?",
                           (id_arma,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def delete_personaje_armadura(id_armadura):
        """Elimina el armadura seleccionada de las armaduras del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_armadura WHERE id = ?",
                           (id_armadura,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    @staticmethod
    def delete_personaje_escudo(id_escudo):
        """Elimina el escudo seleccionado de los escudos del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_escudo WHERE id = ?",
                           (id_escudo,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.")
            print(f"Error detallado: {e}")
        finally:
            conexion.close()

    def _actualizar_valor(self, id_pj, clave, valor): # Borrar JSON
        """Actualiza un solo atributo del JSON de personajes."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == id_pj:
                pj[clave] = valor
                self.guardar_personajes(personajes, False)
                break

    def _actualizar_valor_habilidad(self, id_pj, habilidad, clave, valor):
        """Actualiza un solo atributo de una habilidad del JSON de personajes."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == id_pj:
                for habilidad_json in pj["Habilidades"]:
                    #print(f"HabilidadJSON: {habilidad_json["Nombre"]} | Habilidad: {habilidad.nombre}")
                    if habilidad_json["Nombre"] == habilidad.nombre:
                        habilidad_json[clave] = valor
                        self.guardar_personajes(personajes, False)
                        break

    def _actualizar_valor_equipo(self, id_pj, equipo, tipo_equipo, clave, valor):
        """Actualiza un solo atributo de un arma del JSON de personajes."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == id_pj:
                for equipo_json in pj[tipo_equipo]:
                    if equipo_json["ID"] == equipo.id:
                        equipo_json[clave] = valor
                        self.guardar_personajes(personajes, False)
                        break

    def _actualizar_esfera(self, esfera, clave, valor):
        """Actualiza un solo atributo de una esfera del JSON de personajes."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == self.id:
                for esfera_json in pj["Esferas"]:
                    if esfera_json["ID"] == esfera.id:
                        esfera_json[clave] = valor
                        self.guardar_personajes(personajes, False)
                        return
        print("Error al actualizar esfera.")

    def _guardar_equipamento(self, clave_equipo, lista_equipo): # Borrar JSON
        """Guarda el equipo del personaje, ya sean armas, armaduras o escudos, dependiendo lo que se pase por parámetros."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == self.id:
                #pj[clave_equipo] = [e.convertir_a_diccionario() for e in lista_equipo]
                nuevo_equipo = []

                for equipo in lista_equipo:
                    ultimo_id = self._get_ultimo_id_equipo_de_personaje(nuevo_equipo)
                    equipo_dict = equipo.convertir_a_diccionario()
                    equipo_dict["ID"] = ultimo_id + 1
                    if "Iniciativa" in equipo_dict:
                        equipo_dict["Iniciativa"] = equipo.alcance + self.agilidad + self.inteligencia
                    nuevo_equipo.append(equipo_dict)

                pj[clave_equipo] = nuevo_equipo

                path = Path("personajes.json")
                datos = json.dumps(personajes, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
                try:
                    path.write_text(datos)
                except Exception as e:
                    print(f"Error al guardar el archivo: {e}")

    def _guardar_esfera(self):
        """Guarda una esfera en el personaje."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == self.id:
                nueva_esfera = []

                for esfera in self.esferas:
                    ultimo_id = self._get_ultimo_id_equipo_de_personaje(nueva_esfera)
                    esfera_dict = esfera.convertir_a_diccionario()
                    esfera_dict["ID"] = ultimo_id + 1
                    esfera_dict["Nivel"] = 0
                    esfera_dict["Afinidad"] = 0
                    nueva_esfera.append(esfera_dict)

                pj["Esferas"] = nueva_esfera

                path = Path("personajes.json")
                datos = json.dumps(personajes, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
                try:
                    path.write_text(datos)
                except Exception as e:
                    print(f"Error al guardar el archivo: {e}")

    def _guardar_habilidad(self):
        """Guarda una habilidad en el personaje."""
        personajes = Personaje.leer_datos_personajes()
        for pj in personajes:
            if pj["ID"] == self.id:
                nueva_habilidad = []

                for hab in self.habilidades:
                    hab_dict = hab.convertir_a_diccionario()
                    nueva_habilidad.append(hab_dict)

                pj["Habilidades"] = nueva_habilidad

                path = Path("personajes.json")
                datos = json.dumps(personajes, indent=4) # Guarda los datos en formato JSON. El indent es para darle formato
                try:
                    path.write_text(datos)
                except Exception as e:
                    print(f"Error al guardar el archivo: {e}")

    @staticmethod
    def _get_id():
        """Devuelve el último ID de los personajes guardados, o cero si no hay personajes guardados."""
        personajes = Personaje.leer_datos_personajes()

        if personajes:
            ultimo_personaje = personajes[-1]
            return ultimo_personaje["ID"]
        else:
            return 0
    
    @staticmethod
    def json_a_personaje():
        """Lee el JSON de personajes y devuelve una lista con esos personajes pasados a objetos Personaje."""
        personajes_json = Personaje.leer_datos_personajes()
        personajes = []

        for personaje_json in personajes_json:
            personaje = Personaje()
            personaje._set_atributos(personaje_json["ID"], personaje_json["Jugador"], personaje_json["Nombre"], personaje_json["STEN"]
                                     , personaje_json["Rango"], personaje_json["Fuerza"], personaje_json["Agilidad"]
                                     , personaje_json["Resistencia"], personaje_json["Voluntad"], personaje_json["Inteligencia"]
                                     , personaje_json["Liderazgo"], personaje_json["Potencia"], personaje_json["Defensa"]
                                     , personaje_json["Extensión"], personaje_json["Cantidad Esferas"], personaje_json["Vida"]
                                     , personaje_json["Vida actual"], personaje_json["Dano recibido"], personaje_json["Herida grave"]
                                     , personaje_json["Muerte"], personaje_json["Aguante"] , personaje_json["Aguante actual"]
                                     , personaje_json["Aguante gastado por turno"], personaje_json["Recuperación"]
                                     , personaje_json["Iniciativa"], personaje_json["Carga total"], personaje_json["Carga en manos"]
                                     , personaje_json["Resistencia a la luz"], personaje_json["Resistencia a la oscuridad"]
                                     , personaje_json["Resistencia elemental"], personaje_json["Escudo sobrenatural"]
                                     , personaje_json["Concentración"], personaje_json["Turnos aturdido"]
                                     , personaje_json["Modificador vida"], personaje_json["Modificador aguante"]
                                     , personaje_json["Modificador recuperación"], personaje_json["Modificador iniciativa"]
                                     , personaje_json["Modificador luz"], personaje_json["Modificador oscuridad"]
                                     , personaje_json["Modificador elemental"], personaje_json["Modificador escudo sobrenatural"]
                                     , personaje_json["Habilidades"], personaje_json["Motivación"], personaje_json["Energía"]
                                     , personaje_json["Armas"], personaje_json["Armaduras"], personaje_json["Escudos"],
                                     personaje_json["Esferas"])
            personajes.append(personaje)

        return personajes

    @staticmethod
    def db_a_personaje():
        """Lee el JSON de personajes y devuelve una lista con esos personajes pasados a objetos Personaje."""
        personajes_db = Personaje.select_personajes()
        personajes = []

        for pj_db in personajes_db:
            personaje = Personaje()
            personaje._set_atributos(pj_db["id"], pj_db["jugador"], pj_db["nombre"], pj_db["sten"]
                                     , pj_db["rango"], pj_db["fuerza"], pj_db["agilidad"]
                                     , pj_db["resistencia"], pj_db["voluntad"], pj_db["inteligencia"]
                                     , pj_db["liderazgo"], pj_db["potencia"], pj_db["defensa"]
                                     , pj_db["extension"], pj_db["cantidad_esferas"], pj_db["vida"]
                                     , pj_db["vida_actual"], pj_db["dano_recibido"], pj_db["herida_grave"]
                                     , pj_db["muerte"], pj_db["aguante"] , pj_db["aguante_actual"]
                                     , pj_db["aguante_gastado_por_turno"], pj_db["recuperacion"]
                                     , pj_db["iniciativa"], pj_db["carga_total"], pj_db["carga_en_manos"]
                                     , pj_db["resistencia_a_la_luz"], pj_db["resistencia_a_la_oscuridad"]
                                     , pj_db["resistencia_elemental"], pj_db["escudo_sobrenatural"]
                                     , pj_db["concentracion"], pj_db["turnos_aturdido"]
                                     , pj_db["modificador_vida"], pj_db["modificador_aguante"]
                                     , pj_db["modificador_recuperacion"], pj_db["modificador_iniciativa"]
                                     , pj_db["modificador_luz"], pj_db["modificador_oscuridad"]
                                     , pj_db["modificador_elemental"], pj_db["modificador_escudo_sobrenatural"]
                                     , pj_db["motivacion"], pj_db["energia"])
            personajes.append(personaje)

        return personajes

    def _set_atributos(self, id, jugador, nombre, sten, rango, f, a, r, v, i, l, p, d, e, esf, vida, vida_act, dano_recibido,
                       herida_grave, muerte, aguante, aguante_act, aguante_gas_por_tur, rec, ini, carga_total, carga_manos,
                       res_luz, res_osc, res_ele, esc_sob, concentracion, tur_atur, mod_vida, mod_agu, mod_rec, mod_ini, mod_luz,
                       mod_osc, mod_ele, mod_esc_sob, mot, ene):
        """Asigna todos los valores pasados por argumentos al personaje."""
        self.id = id
        self.jugador = jugador
        self.nombre = nombre
        self.sten = sten
        self.rango = rango
        self.fuerza = f
        self.agilidad = a
        self.resistencia = r
        self.voluntad = v
        self.inteligencia = i
        self.liderazgo = l
        self.potencia = p
        self.defensa = d
        self.extension = e
        self.cant_esferas = esf
        self.vida = vida
        self.vida_actual = vida_act
        self.dano_recibido = dano_recibido
        self.herida_grave = herida_grave
        self.muerte = muerte
        self.aguante = aguante
        self.aguante_actual = aguante_act
        self.aguante_gastado_por_turno = aguante_gas_por_tur
        self.recuperacion = rec
        self.iniciativa = ini
        self.carga_total = carga_total
        self.carga_en_manos = carga_manos
        self.resistencia_luz = res_luz
        self.resistencia_oscuridad = res_osc
        self.resistencia_elemental = res_ele
        self.escudo_sobrenatural = esc_sob
        self.concentracion = concentracion
        self.turnos_aturdido = tur_atur
        self.mod_vida = mod_vida
        self.mod_aguante = mod_agu
        self.mod_recuperacion = mod_rec
        self.mod_iniciativa = mod_ini
        self.mod_res_luz = mod_luz
        self.mod_res_oscuridad = mod_osc
        self.mod_res_elemental = mod_ele
        self.mod_escudo_sobrenatural = mod_esc_sob
        #for hab_json in habilidades_json:
        #    habilidad = Habilidad(hab_json["Nombre"], hab_json["Atributos relacionados"], hab_json["Tipo"])
        #    habilidad.set_atributos(hab_json["Nivel"], hab_json["XP"], hab_json["XP requerida"])
        #    self.habilidades.append(habilidad)
        self.motivacion = mot
        self.energia = ene
        #for arma_json in armas_json:
        #    arma = Arma(arma_json["Nombre"], arma_json["Estructura"], arma_json["Peso"], arma_json["Impacto"], arma_json["Dano"],
        #                arma_json["Alcance"], arma_json["Tipo de dano"], arma_json["Tipo de arma"])
        #    arma.id = Personaje._get_ultimo_id_equipo_de_personaje(self.armas) + 1
        #    arma.calidad = arma_json["Calidad"]
        #    arma.iniciativa = arma.alcance + self.agilidad + self.inteligencia
        #    self.armas.append(arma)
        #for armadura_json in armaduras_json:
        #    armadura = Armadura(armadura_json["Nombre"], armadura_json["Estructura"], armadura_json["Peso"],
        #                        armadura_json["Contundente"], armadura_json["Cortante"], armadura_json["Perforante"],
        #                        armadura_json["Cobertura"], armadura_json["Evasión"], armadura_json["Penalizador"])
        #    armadura.id = Personaje._get_ultimo_id_equipo_de_personaje(self.armaduras) + 1
        #    armadura.calidad = armadura_json["Calidad"]
        #    self.armaduras.append(armadura)
        #for escudo_json in escudos_json:
        #    escudo = Escudo(escudo_json["Nombre"], escudo_json["Estructura"], escudo_json["Peso"],
        #                        escudo_json["Contundente"], escudo_json["Cortante"], escudo_json["Perforante"],
        #                        escudo_json["Cobertura"], escudo_json["Evasión"], escudo_json["Penalizador"])
        #    escudo.id = Personaje._get_ultimo_id_equipo_de_personaje(self.escudos) + 1
        #    escudo.calidad = escudo_json["Calidad"]
        #    self.escudos.append(escudo)
        #for esfera_json in esferas_json:
        #    esfera = Esfera(esfera_json["Nombre"], esfera_json["Poderes"], esfera_json["Pasiva"])
        #    esfera.id = Personaje._get_ultimo_id_esfera_de_personaje(self.esferas) + 1
        #    esfera.nivel = esfera_json["Nivel"]
        #    esfera.afinidad = min(esfera.nivel, self.energia)
        #    self.esferas.append(esfera)

    @staticmethod
    def _get_ultimo_id_equipo_de_personaje(lista_equipo):
        """Devuelve el último ID de equipo guardado en el personaje (ya sea de arma, armadura o escudo),
        o cero si no hay equipo guardado en el personaje."""
        if lista_equipo:
            id = 0
            for item in lista_equipo:
                id += 1
            return id
        else:
            return 0

    @staticmethod
    def _get_ultimo_id_esfera_de_personaje(lista_esferas):
        """Devuelve el último ID de esfera guardado en el personaje, o cero si no hay esferas guardadas en el personaje."""
        if lista_esferas:
            id = 0
            for esfera in lista_esferas:
                id += 1
            return id
        else:
            return 0