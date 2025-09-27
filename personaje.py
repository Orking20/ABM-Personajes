from colores import Color
import base_datos
from math import floor
import re
import sqlite3 as sql

class Personaje:
    """Plantilla que representa cualquier personaje en Espada Negra."""
    def __init__(self):
        """Se inicializan los atributos del personaje."""
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
        self.mod_carga_total = 0
        self.motivacion = 0
        self.energia = 0

    def asignar_jugador(self, nombre):
        """El usuario asigna el nombre del jugador."""
        if len(nombre) > 0:
            self.jugador = nombre
        else:
            print(f"{Color.AMARILLO}El nombre del jugador no puede estar vacío.{Color.FIN}")

    def asignar_nombre(self, nombre):
        """El usuario asigna el nombre del personaje."""
        if len(nombre) > 0:
            self.nombre = nombre
        else:
            print(f"{Color.AMARILLO}El nombre del personaje no puede estar vacío.{Color.FIN}")

    def asignar_sten(self, sten):
        """El usuario asigna la versión STEN que usará el personaje."""
        if sten == 1 or sten == 2:
            self.sten = sten
        else:
            print(f"{Color.AMARILLO}La versión de STEN solo puede ser 1 o 2.{Color.FIN}")

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
            print(f"\n{Color.AMARILLO}El rango del personaje es inválido. Solo pueden ser números enteros entre el 1 y el 4.{Color.FIN}")

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
                    print(f"{Color.AMARILLO}Para subir un atributo debe ingresar un número entre el 1 y el 3.{Color.FIN}")
                    return None
                # Dependiendo de la elección del usuario se sube uno u otro atributo
                elif eleccion == 1:
                    valor_atributo = self._get_atributo_by_str(atributo1.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo1.lower(), valor_atributo)
                    self._update_personaje(atributo1.lower(), valor_atributo)
                elif eleccion == 2:
                    valor_atributo = self._get_atributo_by_str(atributo2.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo2.lower(), valor_atributo)
                    self._update_personaje(atributo2.lower(), valor_atributo)
                elif eleccion == 3:
                    valor_atributo = self._get_atributo_by_str(atributo3.lower())
                    valor_atributo += 1
                    self._set_atributo_by_str(atributo3.lower(), valor_atributo)
                    self._update_personaje(atributo3.lower(), valor_atributo)

            self.rango += 1
            self._update_personaje("rango", self.rango)
            self._actualizar_cualidades()
        else:
            print(f"{Color.AMARILLO}Eres {Personaje.convertir_rango_a_str(self.rango)}! Has alcanzado el máximo rango.{Color.FIN}")

    def _resetear_habilidad(self, id_hab):
        """Quita una habilidad al personaje."""
        habilidades = Personaje.select_personaje_habilidad(self.id)
        for hab in habilidades:
            if hab["id_personaje"] == self.id and hab["id_habilidad"] == id_hab:
                self._update_personaje_habilidad("nivel", 0, id_hab)
                self._update_personaje_habilidad("xp", 0, id_hab)
                self._update_personaje_habilidad("xp_requerida", 5, id_hab)
                break

    def _actualizar_cualidades(self):
        """Actualiza las cualidades de un personaje, como la vida, aguante, resistencia, etc."""
        pj = self.select_personaje()
        pj = pj[0]
        cant_esferas = pj["extension"]
        aguante = (pj["resistencia"] * 5) + pj["modificador_aguante"]
        recuperacion = (pj["resistencia"]) + pj["modificador_recuperacion"]
        iniciativa = (pj["agilidad"] + pj["inteligencia"]) + pj["modificador_iniciativa"]
        carga_total = pj["fuerza"] * 5 + pj["modificador_escudo_sobrenatural"]
        carga_en_manos = pj["fuerza"]
        resistencia_luz = pj["defensa"] + pj["modificador_luz"]
        resistencia_oscuridad = pj["defensa"] + pj["modificador_oscuridad"]
        resistencia_elemental = pj["fuerza"] + pj["modificador_elemental"]
        escudo_sobrenatural = pj["voluntad"] + pj["defensa"] + pj["modificador_escudo_sobrenatural"]
        if pj["sten"] == 1:
            vida = (pj["voluntad"] * 3) + pj["modificador_vida"]
            muerte = pj["fuerza"] * 6
        elif pj["sten"] == 2:
            vida = (pj["voluntad"] * 5) + pj["modificador_vida"]
            muerte = pj["fuerza"] * 10
        vida_actual = vida
        aguante_actual = aguante

        self._update_personaje("cantidad_esferas", cant_esferas)
        self._update_personaje("aguante", aguante)
        self._update_personaje("recuperacion", recuperacion)
        self._update_personaje("iniciativa", iniciativa)
        self._update_personaje("carga_total", carga_total)
        self._update_personaje("carga_en_manos", carga_en_manos)
        self._update_personaje("resistencia_a_la_luz", resistencia_luz)
        self._update_personaje("resistencia_a_la_oscuridad", resistencia_oscuridad)
        self._update_personaje("resistencia_elemental", resistencia_elemental)
        self._update_personaje("escudo_sobrenatural", escudo_sobrenatural)
        self._update_personaje("vida", vida)
        self._update_personaje("muerte", muerte)
        self._update_personaje("vida_actual", vida_actual)
        self._update_personaje("aguante_actual", aguante_actual)

    def asignar_cualidades(self):
        """Asigna las cualidades del personaje."""
        self.cant_esferas = self.extension
        self.aguante = (self.resistencia * 5) + self.mod_aguante
        self.recuperacion = (self.resistencia) + self.mod_recuperacion
        self.iniciativa = (self.agilidad + self.inteligencia) + self.mod_iniciativa
        self.carga_total = self.fuerza * 5 + self.mod_carga_total
        self.carga_en_manos = self.fuerza
        self.resistencia_luz = self.defensa + self.mod_res_luz
        self.resistencia_oscuridad = self.defensa + self.mod_res_oscuridad
        self.resistencia_elemental = self.fuerza + self.mod_res_elemental
        self.escudo_sobrenatural = self.voluntad + self.defensa + self.mod_escudo_sobrenatural
        if self.sten == 1:
            self.vida = (self.voluntad * 3) + self.mod_vida
            self.muerte = self.fuerza * 6
        elif self.sten == 2:
            self.vida = (self.voluntad * 5) + self.mod_vida
            self.muerte = self.fuerza * 10
        self.vida_actual = self.vida
        self.aguante_actual = self.aguante

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
                    tiene_esfera = self.subir_nivel_esfera(es_esfera.group(1))
                    if not tiene_esfera:
                        return
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
                    tiene_esfera = self.subir_nivel_esfera(es_esfera.group(1))
                    if not tiene_esfera:
                        return
                self._update_personaje_habilidad("nivel", nuevo_nivel, hab_dict["id"])
                self.calcular_xp_req_habilidades(self.id)

            self._update_personaje_habilidad("xp", nueva_xp, hab_dict["id"])
            self._update_personaje("motivacion", nueva_motivacion)
        else:
            print(f"{Color.AMARILLO}Necesitas más motivación para subir el nivel de esta habilidad.{Color.FIN}")

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
                    self.bajar_nivel_esfera(hab_dict["id"])
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

        self._update_personaje("motivacion", nueva_motivacion)
        self._update_personaje_habilidad("xp", nueva_xp, hab_dict["id"])

    def subir_nivel_esfera(self, nombre):
        """Sube el nivel de una esfera. Si no tiene la esfera devuelve False."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            #esf_nom = re.search(r"\((.*?)\)", fila["nombre_e"])
            #if esf_nom:
            #    esf_nom = esf_nom.group(1)
            if fila["nombre_e"] == nombre:
                nuevo_nivel = fila["nivel"] + 1
                self._update_personaje_esfera("nivel", nuevo_nivel, fila["id_esfera"])
                self.calcular_afinidad()
                return True
        else: # El else en el for se ejecuta cuando termina el ciclio SOLO si no hubo un break
            print(f"{Color.AMARILLO}No se encuentra una esfera con el nombre '{nombre}'{Color.FIN}")
            return False

    def bajar_nivel_esfera(self, id_hab):
        """Sube el nivel de una esfera."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            if fila["id"] == id_hab:
                nuevo_nivel = fila["nivel"] - 1
                self._update_personaje_esfera("nivel", nuevo_nivel, fila["id_esfera"])
                self.calcular_afinidad()
                break
        else: # El else en el for se ejecuta cuando termina el ciclio SOLO si no hubo un break
            print(f"{Color.AMARILLO}No se encuentra una esfera con el id '{id_hab}'{Color.FIN}")

    def agregar_motivacion(self, motivacion):
        """Agrega la cantidad de motivación indicada al personaje."""
        self.motivacion += motivacion
        self._update_personaje("motivacion", self.motivacion)

    def quitar_motivacion(self, motivacion):
        """Sustrae la cantidad de motivación indicada al personaje."""
        if self.motivacion - motivacion >= 0:
            self.motivacion -= motivacion
            self._update_personaje("motivacion", self.motivacion)
        else:
            print(f"{Color.AMARILLO}No tienes tanta motivación para quitar.{Color.FIN}")

    def agregar_energia(self, energia):
        """Agrega la cantidad de energía indicada al personaje."""
        self.energia += energia
        self._update_personaje("energia", self.energia)
        self.calcular_afinidad()

    def gastar_energia(self, energia=1):
        """Sustrae la cantidad de energía indicada al personaje."""
        if self.energia - energia >= 0:
            self.energia -= energia
            if energia == 1:
                print(f"{Color.NARANJA}Se gasta {energia} punto de energía{Color.FIN}")
            else:
                print(f"{Color.NARANJA}Se gasta {energia} puntos de energía{Color.FIN}")
            self._update_personaje("energia", self.energia)
            self.calcular_afinidad()
        else:
            if energia == 1:
                print(f"{Color.AMARILLO}No tienes más energía para gastar.{Color.FIN}")
            else:
                print(f"{Color.AMARILLO}No tienes tanta energía para gastar.{Color.FIN}")

    def _calcular_atributo_mas_bajo(self, atributos_char: list):
        """Calcula el atributo más bajo de los pasados por parámetros."""
        atributos = self._convertir_atr_char_a_int(atributos_char)
        return min(atributos)

    def agregar_esfera(self, id_esfera):
        """Agrega la esfera pasada por parámetros si el personaje tiene hueco para esferas."""
        #Se calcula la cantidad de esferas del personaje
        esferas_pj = Personaje.select_personaje_esfera(self.id)
        cantidad = 0
        id_anterior = None
        for esfera in esferas_pj:
            if esfera["id"] != id_anterior:
                id_anterior = esfera["id"]
                cantidad += 1

        if cantidad < self.cant_esferas:
            esferas = base_datos.select_esferas()
            for esfera in esferas:
                if esfera["id"] == id_esfera:
                    self._insert_personaje_esfera(id_esfera, 0, 0)
                    return
            print(f"{Color.AMARILLO}El ID de esfera pasado no existe.{Color.FIN}")
        else:
            print(f"\n{Color.AMARILLO}No puedes llevar más esferas. Tu número máximo de esferas es {self.cant_esferas}{Color.FIN}")

    def quitar_esfera(self, id_esfera):
        """Quita la esfera pasada por parámetros del personaje."""
        habilidades = Personaje.select_personaje_habilidad(self.id)
        for hab in habilidades:
            if id_esfera == hab["id"]:
                self._resetear_habilidad(id_esfera)
                self._delete_personaje_esfera(id_esfera)
                print(f"\n{Color.VERDE}Esfera eliminada con éxito.{Color.FIN}")
                break
        else:
            print(f"\n{Color.AMARILLO}Esa esfera no se encuentra en el personaje.{Color.FIN}")

    def calcular_afinidad(self):
        """Calcula y guarda la afinidad de cada esfera del personaje."""
        esferas = Personaje.select_personaje_esfera(self.id)
        for fila in esferas:
            afinidad = min(fila["nivel"], self.energia)
            self._update_personaje_esfera("afinidad", afinidad, fila["id_esfera"])

    def equipar_arma(self, arma):
        """Equipa el arma pasada por argumento al personaje."""
        arma.iniciativa = arma.alcance + self.agilidad + self.inteligencia
        arma.asignar_calidad(1)
        self._insert_personaje_arma(arma.id, arma.iniciativa, arma.calidad)

    def equipar_armadura(self, armadura):
        """Equipa la armadura pasada por argumento al personaje."""
        armadura.asignar_calidad(1)
        self._insert_personaje_armadura(armadura.id, armadura.calidad)

    def equipar_escudo(self, escudo):
        """Equipa el escudo pasado por argumento al personaje."""
        escudo.asignar_calidad(1)
        self._insert_personaje_escudo(escudo.id, escudo.calidad)

    def desequipar_arma(self, id_arma):
        """Desequipa el arma pasada por argumento al personaje."""
        Personaje._delete_personaje_arma(id_arma)
        print(f"{Color.VERDE}Arma desequipada{Color.FIN}")

    def desequipar_armadura(self, id_armadura):
        """Desequipa la armadura pasada por argumento al personaje."""
        Personaje._delete_personaje_armadura(id_armadura)
        print(f"{Color.VERDE}Armadura desequipada{Color.FIN}")

    def desequipar_escudo(self, id_escudo):
        """Desequipa el escudo pasado por argumento al personaje."""
        Personaje._delete_personaje_escudo(id_escudo)
        print(f"{Color.VERDE}Escudo desequipado{Color.FIN}")

    def cambiar_calidad_objeto(self, id_equipo, tipo_equipo, nueva_calidad):
        """Cambia la calidad de cualquier equipo: arma, armadura o escudo."""
        if nueva_calidad >= 0 or nueva_calidad <= 5:
            if tipo_equipo == "Armas":
                armas = Personaje.select_personaje_arma(self.id)
                for arma in armas:
                    if arma["id_pj_arma"] == id_equipo:
                        existe = True
                        calidad_anterior = arma["calidad"]
                        break
                
                if existe:
                    Personaje._update_personaje_equipo("personaje_arma", id_equipo, "calidad", nueva_calidad)
                    self._aplicar_efecto_calidad_arma(id_equipo, calidad_anterior)
                else:
                    print(f"{Color.AMARILLO}Ese ID de arma no existe, o no corresponde con el personaje.{Color.FIN}")
            elif tipo_equipo == "Armaduras":
                armaduras = Personaje.select_personaje_armadura(self.id)
                for armadura in armaduras:
                    if armadura["id_pj_armadura"] == id_equipo:
                        existe = True
                        calidad_anterior = armadura["calidad"]
                        break

                if existe:
                    Personaje._update_personaje_equipo("personaje_armadura", id_equipo, "calidad", nueva_calidad)
                    self._aplicar_efecto_calidad_armadura(id_equipo, calidad_anterior)
                else:
                    print(f"{Color.AMARILLO}Ese ID de armadura no existe, o no corresponde con el personaje.{Color.FIN}")
            elif tipo_equipo == "Escudos":
                escudos = Personaje.select_personaje_escudo(self.id)
                for escudo in escudos:
                    if escudo["id_pj_escudo"] == id_equipo:
                        existe = True
                        calidad_anterior = escudo["calidad"]
                        break

                if existe:
                    Personaje._update_personaje_equipo("personaje_escudo", id_equipo, "calidad", nueva_calidad)
                    self._aplicar_efecto_calidad_escudo(id_equipo, calidad_anterior)
                else:
                    print(f"{Color.AMARILLO}Ese ID del escudo no existe, o no corresponde con el personaje.{Color.FIN}")
        else:
            print(f"{Color.AMARILLO}La calidad del equipo no puede ser inferior a cero ni mayor a cinco.{Color.FIN}")

    def _aplicar_efecto_calidad_arma(self, id_arma, calidad_anterior):
        """Aplica el efecto en el arma según la calidad."""
        armas = Personaje.select_personaje_arma(self.id)
        for arma in armas:
            if id_arma == arma["id_pj_arma"]:
                nueva_calidad = arma["calidad"]
                if nueva_calidad > calidad_anterior:
                    diferencia_calidad = nueva_calidad - calidad_anterior
                    estructura = arma["estructura"] + diferencia_calidad
                elif nueva_calidad < calidad_anterior:
                    diferencia_calidad = calidad_anterior - nueva_calidad
                    estructura = arma["estructura"] - diferencia_calidad
                else: # Si la calidad anterior es igual a la nueva
                    break

                if self.sten == 2:
                    iniciativa = arma["alcance"] + self.agilidad + self.inteligencia + diferencia_calidad
                    Personaje._update_personaje_equipo("personaje_arma", id_arma, "iniciativa", iniciativa)

                Personaje._update_personaje_equipo("personaje_arma", id_arma, "estructura", estructura)
                break

    def _aplicar_efecto_calidad_armadura(self, id_armadura, calidad_anterior):
        """Aplica el efecto en la armadura según la calidad."""
        armaduras = Personaje.select_personaje_armadura(self.id)
        for armadura in armaduras:
            if id_armadura == armadura["id_pj_armadura"]:
                nueva_calidad = armadura["calidad"]
                if nueva_calidad > calidad_anterior:
                    diferencia_calidad = nueva_calidad - calidad_anterior
                    estructura = armadura["estructura"] + diferencia_calidad
                    peso = armadura["peso"] - diferencia_calidad
                elif nueva_calidad < calidad_anterior:
                    diferencia_calidad = calidad_anterior - nueva_calidad
                    estructura = armadura["estructura"] - diferencia_calidad
                    peso = armadura["peso"] + diferencia_calidad
                else: # Si la calidad anterior es igual a la nueva
                    break

                Personaje._update_personaje_equipo("personaje_armadura", id_armadura, "estructura", estructura)
                Personaje._update_personaje_equipo("personaje_armadura", id_armadura, "peso", peso)
                break

    def _aplicar_efecto_calidad_escudo(self, id_escudo, calidad_anterior):
        """Aplica el efecto en el escudo según la calidad."""
        escudos = Personaje.select_personaje_escudo(self.id)
        for escudo in escudos:
            if id_escudo == escudo["id_pj_escudo"]:
                nueva_calidad = escudo["calidad"]
                if nueva_calidad > calidad_anterior:
                    diferencia_calidad = nueva_calidad - calidad_anterior
                    estructura = escudo["estructura"] + diferencia_calidad
                elif nueva_calidad < calidad_anterior:
                    diferencia_calidad = calidad_anterior - nueva_calidad
                    estructura = escudo["estructura"] - diferencia_calidad
                else: # Si la calidad anterior es igual a la nueva
                    break

                Personaje._update_personaje_equipo("personaje_escudo", id_escudo, "estructura", estructura)
                break

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
                    print(f"\n{Color.AMARILLO}El nuevo valor de tu cualidad no puede estar por debajo de cero.{Color.FIN}")
                    return
            else:
                print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
                return

            Personaje._update_personaje_equipo("personaje_arma", id_arma, columna, nuevo_valor)
        else:
            print(f"{Color.AMARILLO}Ese ID de arma no existe, o no corresponde con el personaje.{Color.FIN}")

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
                    print(f"\n{Color.AMARILLO}El nuevo valor de tu cualidad no puede estar por debajo de cero.{Color.FIN}")
                    return
            else:
                print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
                return

            Personaje._update_personaje_equipo("personaje_armadura", id_armadura, columna, nuevo_valor)
        else:
            print(f"{Color.AMARILLO}Ese ID de armadura no existe, o no corresponde con el personaje.{Color.FIN}")

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
                    print(f"\n{Color.AMARILLO}El nuevo valor de tu cualidad no puede estar por debajo de cero.{Color.FIN}")
                    return
            else:
                print(f"\n{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
                return

            Personaje._update_personaje_equipo("personaje_escudo", id_escudo, columna, nuevo_valor)
        else:
            print(f"{Color.AMARILLO}Ese ID de escudo no existe, o no corresponde con el personaje.{Color.FIN}")

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
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_vida", self.mod_vida)
        self._update_personaje("vida", self.vida)

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
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_aguante", self.mod_aguante)
        self._update_personaje("aguante", self.aguante)

    def modificador_recuperacion(self, operador, valor):
        """Cambia el modificador a la recuperación del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_recuperacion += valor
            self.recuperacion += valor
        elif operador == 2: # Resta
            self.mod_recuperacion -= valor
            self.recuperacion -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_recuperacion", self.mod_recuperacion)
        self._update_personaje("recuperacion", self.recuperacion)

    def modificador_iniciativa(self, operador, valor):
        """Cambia el modificador a la iniciativa del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_iniciativa += valor
            self.iniciativa += valor
        elif operador == 2: # Resta
            self.mod_iniciativa -= valor
            self.iniciativa -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_iniciativa", self.mod_iniciativa)
        self._update_personaje("iniciativa", self.iniciativa)

    def modificador_luz(self, operador, valor):
        """Cambia el modificador a la resistencia a la luz del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_luz += valor
            self.resistencia_luz += valor
        elif operador == 2: # Resta
            self.mod_res_luz -= valor
            self.resistencia_luz -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_luz", self.mod_res_luz)
        self._update_personaje("resistencia_a_la_luz", self.resistencia_luz)

    def modificador_oscuridad(self, operador, valor):
        """Cambia el modificador a la resistencia a la oscuridad del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_oscuridad += valor
            self.resistencia_oscuridad += valor
        elif operador == 2: # Resta
            self.mod_res_oscuridad -= valor
            self.resistencia_oscuridad -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_oscuridad", self.mod_res_oscuridad)
        self._update_personaje("resistencia_a_la_oscuridad", self.resistencia_oscuridad)

    def modificador_elemental(self, operador, valor):
        """Cambia el modificador a la resistencia elemental del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_res_elemental += valor
            self.resistencia_elemental += valor
        elif operador == 2: # Resta
            self.mod_res_elemental -= valor
            self.resistencia_elemental -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_elemental", self.mod_res_elemental)
        self._update_personaje("resistencia_elemental", self.resistencia_elemental)

    def modificador_escudo_sobrenatural(self, operador, valor):
        """Cambia el modificador al escudo sobrenatural del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_escudo_sobrenatural += valor
            self.escudo_sobrenatural += valor
        elif operador == 2: # Resta
            self.mod_escudo_sobrenatural -= valor
            self.escudo_sobrenatural -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_escudo_sobrenatural", self.mod_escudo_sobrenatural)
        self._update_personaje("escudo_sobrenatural", self.escudo_sobrenatural)

    def modificador_carga_total(self, operador, valor):
        """Cambia el modificador a la carga total del personaje. operador 1: Suma. operador 2: resta"""
        if operador == 1: # Suma
            self.mod_carga_total += valor
            self.carga_total += valor
        elif operador == 2: # Resta
            self.mod_carga_total -= valor
            self.carga_total -= valor
        else:
            print(f"{Color.AMARILLO}Operador inválido. El operador tiene que ser 1 para suma, o 2 para resta.{Color.FIN}")
            return

        self._update_personaje("modificador_carga_total", self.mod_carga_total)
        self._update_personaje("carga_total", self.carga_total)

    def gastar_aguante(self):
        """Le resta un punto de aguante al personaje si puede."""
        if self.aguante_gastado_por_turno < self.resistencia:
            if self.aguante_actual - 1 >= 0:
                self.aguante_actual -= 1
                self.aguante_gastado_por_turno += 1
                print(f"{Color.NARANJA}Aguante -1{Color.FIN}")
            else:
                print(f"\n{Color.AMARILLO}Ya no te queda aguante para gastar.{Color.FIN}")
        else:
            print(f"{Color.AMARILLO}No puedes gastar más puntos de aguante que tu resistencia por turno.{Color.FIN}")

        self._update_personaje("aguante_actual", self.aguante_actual)
        self._update_personaje("aguante_gastado_por_turno", self.aguante_gastado_por_turno)

    def recuperar_aguante(self, recuperacion):
        """Recupera tantos puntos de aguante al personaje como los pasados por parámetro, hasta un máximo como su aguante total."""
        if self.aguante_actual + recuperacion <= self.aguante:
            self.aguante_actual += recuperacion
            print(f"{Color.NARANJA}Aguante +{recuperacion}{Color.FIN}")
        else:
            self.aguante_actual = self.aguante
            print(f"{Color.NARANJA}Aguante recuperado completamente{Color.FIN}")

        self._update_personaje("aguante_actual", self.aguante_actual)

    def recibir_dano(self, dano):
        """Recibe el daño y lo ve reflejado en su vida actual, en si queda aturdido y en si recibe heridas."""
        self.vida_actual -= dano
        self.dano_recibido += dano
        print(f"{Color.NARANJA}Vida -{dano}{Color.FIN}")

        if dano > self.voluntad * 2:
            self.turnos_aturdido = 2
            self.concentracion = 0
            print(f"{Color.NARANJA}Quedas aturdido este turno y el siguiente, y pierdes todos los puntos de concentración.{Color.FIN}")
            self._update_personaje("concentracion", self.concentracion)
            self._update_personaje("turnos_aturdido", self.turnos_aturdido)
        elif dano > self.voluntad:
            self.turnos_aturdido = 1
            print(f"{Color.NARANJA}Quedas aturdido este turno.{Color.FIN}")
            concentracion_perdida = dano - self.voluntad
            if self.concentracion > 0 and concentracion_perdida > 0:
                self.perder_concentracion(concentracion_perdida)
            self._update_personaje("turnos_aturdido", self.turnos_aturdido)

        if dano > self.fuerza * 3 and self.sten == 1:
            print(f"{Color.NARANJA}A elección del atacante:\nBrazo: -2 daño, -1 vida por turno\nPierna: -6 iniciativa, -1 vida por turno\nTorso o cabeza: -6 aguante, -1 vida por turno\nSi el golpe fue en un brazo o una pierna, la extremidad se verá comprometida y no podrá utilizarse.{Color.FIN}")
            self.herida_grave = True
            self._update_personaje("herida_grave", self.herida_grave)
        elif dano > self.fuerza * 3 and self.sten == 2:
            print(f"{Color.NARANJA}A elección del atacante: Pierde un punto del atributo a todos los efectos. -1 vida por turno\nSi el atributo dañado es fuerza o agilidad, respectivamente un brazo o una pierna se verá comprometido y no podrá utilizarse. Una vez se recupere, pierde un punto del atributo solamente con uno de los aspectos de dicho atributo (a elección del atacante).{Color.FIN}")
            self.herida_grave = True
            self._update_personaje("herida_grave", self.herida_grave)
        elif dano > self.fuerza * 2 and self.sten == 1:
            print(f"{Color.NARANJA}A elección del atacante:\nBrazo: -1 daño\nPierna: -3 iniciativa\nTorso o cabeza: -3 aguante{Color.FIN}")
        elif dano > self.fuerza * 2 and self.sten == 2:
            print(f"{Color.NARANJA}A elección del atacante: El personaje pierde un punto del atributo en relación con únicamente uno de los aspectos de dicho atributo, hasta que recibe cirugía médica.{Color.FIN}")

        if self.vida_actual <= 0:
            self.vida_actual = 0
            print(f"{Color.NARANJA}{self.nombre} cae inconsciente. Sus puntos de vida llegaron a cero.{Color.FIN}")

        if self.dano_recibido >= self.muerte:
            print(f"{Color.NARANJA}{self.nombre} muere.{Color.FIN}")

        self._update_personaje("vida_actual", self.vida_actual)
        self._update_personaje("dano_recibido", self.dano_recibido)

    def recuperar_vida(self, puntos_restaurar):
        """Recupera los puntos de vida pasados por parámetros y los refleja en su vida actual."""
        if self.vida_actual + puntos_restaurar <= self.vida:
            self.vida_actual += puntos_restaurar
            self.dano_recibido -= puntos_restaurar
            print(f"{Color.NARANJA}Vida +{puntos_restaurar}{Color.FIN}")
        else:
            self.vida_actual = self.vida
            self.dano_recibido = 0
            print(f"{Color.NARANJA}Vida restaurada completamente{Color.FIN}")

        self._update_personaje("vida_actual", self.vida_actual)
        self._update_personaje("dano_recibido", self.dano_recibido)

    def curar_herida_grave(self):
        """Cura una herida grave en caso de tenerla."""
        if self.herida_grave:
            self.herida_grave = False
            print(f"{Color.NARANJA}Herida curada.{Color.FIN}")
            self._actualizar_valor(self.id, "Herida grave", self.herida_grave)
            self._update_personaje("herida_grave", self.herida_grave)
        else:
            print(f"{Color.AMARILLO}{self.nombre} no tiene ninguna herida grave.{Color.FIN}")

    def ganar_concentracion(self, puntos_concentracion):
        """Gana los puntos de concentración pasados por parámetros."""
        self.concentracion += puntos_concentracion
        print(f"{Color.NARANJA}Concentración +{puntos_concentracion}{Color.FIN}")
        self._update_personaje("concentracion", self.concentracion)

    def perder_concentracion(self, puntos_concentracion):
        """Pierde los puntos de concentración pasados por parámetros."""
        if self.concentracion - puntos_concentracion >= 0:
            self.concentracion -= puntos_concentracion
        else:
            self.concentracion = 0
        print(f"{Color.NARANJA}Concentración -{puntos_concentracion}{Color.FIN}")
        self._update_personaje("concentracion", self.concentracion)

    def ronda_nueva(self):
        """Se encarga de retirar aturdimiento y aguante usado por turno del personaje en caso de tenerlo."""
        if self.aguante_gastado_por_turno > 0:
            self.aguante_gastado_por_turno = 0
            self._update_personaje("aguante_gastado_por_turno", self.aguante_gastado_por_turno)

        if self.turnos_aturdido > 0:
            self.turnos_aturdido -= 1
            print(f"{Color.NARANJA}Turnos aturdidos -1{Color.FIN}")
            self._update_personaje("turnos_aturdido", self.turnos_aturdido)

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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla de personajes no existe, o no se puede abrir por falta de persmisos.{Color.ROJO}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla de personajes no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
                            ph.id_personaje, ph.id_habilidad, ph.nivel, ph.xp, ph.xp_requerida
                            FROM personaje_habilidad ph
                            JOIN habilidades h ON ph.id_habilidad = h.id
                            WHERE ph.id_personaje = ?
                            """, (id_personaje,)) # El segundo parámetro tiene que ser una tupla
            habilidades = cursor.fetchall()
            return habilidades
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'habilidad_atributo' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
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
                            pe.id_esfera, pe.nivel, pe.afinidad,
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def insert_personaje(self):
        """Inserta un personaje nuevo en la tabla."""
        habilidades = base_datos.select_habilidades()
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"""
                        INSERT INTO personajes (jugador, nombre, sten, rango, fuerza, agilidad, resistencia,
                        voluntad, inteligencia, liderazgo, potencia, defensa, extension, cantidad_esferas,
                        vida, vida_actual, dano_recibido, herida_grave, muerte, aguante, aguante_actual,
                        aguante_gastado_por_turno, recuperacion, iniciativa, carga_total, carga_en_manos,
                        resistencia_a_la_luz, resistencia_a_la_oscuridad, resistencia_elemental,
                        escudo_sobrenatural, concentracion, turnos_aturdido, modificador_vida,
                        modificador_aguante, modificador_recuperacion, modificador_iniciativa,
                        modificador_luz, modificador_oscuridad, modificador_elemental,
                        modificador_escudo_sobrenatural, modificador_carga_total, motivacion, energia)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (self.jugador, self.nombre, self.sten, self.rango,
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
                        self.mod_res_oscuridad, self.mod_res_elemental, self.mod_escudo_sobrenatural,
                        self.mod_carga_total, self.motivacion, self.energia))
            id_pj = cursor.lastrowid # Obtiene el id autogenerado

            for hab in habilidades:
                cursor.execute(f"""INSERT INTO personaje_habilidad VALUES (?, ?, ?, ?, ?)""", (id_pj, hab [0], 0, 0, 5))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personajes' o 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _update_personaje(self, columna, valor):
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
                            "modificador_carga_total", "motivacion", "energia")

        if columna not in columnas_validas:
            print(f"{Color.ROJO}Esa columna no se puede modificar.{Color.FIN}")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personajes SET {columna} = ? WHERE id = ?", (valor, self.id))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personajes' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def _update_personaje_equipo(tabla, id, columna, valor):
        """Actualiza un campo de la tabla personaje_esfera según el valor pasado."""
        tablas_validas = ("personaje_arma", "personaje_armadura", "personaje_escudo")

        if tabla not in tablas_validas:
            print(f"{Color.ROJO}Esa tabla no se puede modificar.{Color.FIN}")
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
            print(f"{Color.ROJO}La columna '{columna}' no se puede modificar.{Color.FIN}")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE {tabla} SET {columna} = ? WHERE id = ?",
                           (valor, id))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla '{tabla}' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _update_personaje_esfera(self, columna, valor, id_esfera):
        """Actualiza un campo de la tabla personaje_esfera según el valor pasado."""
        columnas_validas = ("nivel", "afinidad")

        if columna not in columnas_validas:
            print(f"{Color.ROJO}Esa columna no se puede modificar.{Color.FIN}")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personaje_esfera SET {columna} = ? WHERE id_personaje = ? AND id_esfera = ?",
                           (valor, self.id, id_esfera))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _update_personaje_habilidad(self, columna, valor, id_habilidad):
        """Actualiza un campo de la tabla personaje_habilidad según el valor pasado."""
        columnas_validas = ("nivel", "xp", "xp_requerida")

        if columna not in columnas_validas:
            print(f"{Color.ROJO}Esa columna no se puede modificar.{Color.FIN}")
            return

        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"UPDATE personaje_habilidad SET {columna} = ? WHERE id_personaje = ? AND id_habilidad = ?",
                           (valor, self.id, id_habilidad))

            conexion.commit()
            conexion.close()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _insert_personaje_arma(self, id_arma, iniciativa, calidad):
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _insert_personaje_armadura(self, id_armadura, calidad):
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _insert_personaje_escudo(self, id_escudo, calidad):
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
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _insert_personaje_esfera(self, id_esfera, nivel, afinidad):
        """Inserta un esfera a un personaje en la tabla personaje_esfera."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute(f"""INSERT INTO personaje_esfera VALUES (?, ?, ?, ?)""",
                           (self.id, id_esfera, nivel, afinidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def eliminar_personaje(self):
        """Elimina el personaje seleccionado y todas sus referencias."""
        armas = Personaje.select_personaje_arma(self.id)
        armaduras = Personaje.select_personaje_armadura(self.id)
        escudos = Personaje.select_personaje_escudo(self.id)
        habilidades = Personaje.select_personaje_habilidad(self.id)
        esferas = Personaje.select_personaje_esfera(self.id)

        for arma in armas:
            Personaje._delete_personaje_arma(arma["id_pj_arma"])
        for armadura in armaduras:
            Personaje._delete_personaje_armadura(armadura["id_pj_armadura"])
        for escudo in escudos:
            Personaje._delete_personaje_escudo(escudo["id_pj_escudo"])
        for hab in habilidades:
            Personaje._delete_personaje_habilidad(self.id, hab["id_habilidad"])
        for esfera in esferas:
            self._delete_personaje_esfera(esfera["id_esfera"])
        Personaje._delete_personaje(self.id)

    @staticmethod
    def _delete_personaje(id_pj):
        """Elimina el personaje seleccionado."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personajes WHERE id = ?",
                           (id_pj,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personajes' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def _delete_personaje_arma(id_arma):
        """Elimina el arma seleccionada de las armas del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_arma WHERE id = ?",
                           (id_arma,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_arma' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def _delete_personaje_armadura(id_armadura):
        """Elimina el armadura seleccionada de las armaduras del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_armadura WHERE id = ?",
                           (id_armadura,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_armadura' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def _delete_personaje_escudo(id_escudo):
        """Elimina el escudo seleccionado de los escudos del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_escudo WHERE id = ?",
                           (id_escudo,))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_escudo' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def _delete_personaje_habilidad(id_personaje, id_habilidad):
        """Elimina la habilidad seleccionada del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_habilidad WHERE id_personaje = ? AND id_habilidad = ?",
                           (id_personaje, id_habilidad))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_habilidad' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    def _delete_personaje_esfera(self, id_esfera):
        """Elimina la esfera seleccionada del personaje."""
        try:
            conexion = sql.connect(f"espada_negra.db")
            cursor = conexion.cursor()

            cursor.execute("DELETE FROM personaje_esfera WHERE id_personaje = ? AND id_esfera = ?",
                           (self.id, id_esfera))

            conexion.commit()
        except sql.OperationalError as e:
            print(f"{Color.ROJO}{Color.NEGRITA}Posible error:{Color.FIN}{Color.GRIS} La tabla 'personaje_esfera' no existe, o no se puede abrir por falta de persmisos.{Color.FIN}")
            print(f"{Color.ROJO}{Color.NEGRITA}Error detallado: {Color.FIN}{Color.GRIS}{e}{Color.FIN}")
        finally:
            conexion.close()

    @staticmethod
    def db_a_personaje():
        """Lee la tabla de personajes y devuelve una lista con esos personajes pasados a objetos Personaje."""
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
                                     , pj_db["modificador_carga_total"], pj_db["motivacion"], pj_db["energia"])
            personajes.append(personaje)

        return personajes

    def _set_atributos(self, id, jugador, nombre, sten, rango, f, a, r, v, i, l, p, d, e, esf, vida, vida_act, dano_recibido,
                       herida_grave, muerte, aguante, aguante_act, aguante_gas_por_tur, rec, ini, carga_total, carga_manos,
                       res_luz, res_osc, res_ele, esc_sob, concentracion, tur_atur, mod_vida, mod_agu, mod_rec, mod_ini, mod_luz,
                       mod_osc, mod_ele, mod_esc_sob, mod_carga_total, mot, ene):
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
        self.mod_carga_total = mod_carga_total
        self.motivacion = mot
        self.energia = ene