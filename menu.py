from personaje import Personaje
from equipo import Equipo, Arma, Armadura, Escudo
from esfera import Esfera
import base_datos
from rich.console import Console
from rich.table import Table
from collections import defaultdict

class Menu:
    """Clase que sirve para que el usuario pueda controlar e interaccionar con sus personajes mediante un menú."""

    def menu_principal(self):
        """Muestra el menú principal para crear, administrar personajes, etc."""
        print("\n-------------------------------- Espada Negra --------------------------------")
        eleccion = Menu._input_eleccion_menu("\n1. Crear personaje\n2. Ver personajes\n0. Salir\n: ",
                                             "\nDebes ingresar un número entre 0 y 2 del menú.", [0, 1, 2])

        if eleccion == 0:
            exit()
        elif eleccion == 1:
            Menu._menu_crear_personaje()
        elif eleccion == 2:
            Menu._menu_lista_personajes()
        #elif eleccion == 3:
        #    Menu._menu_administrar_equipo()

    @staticmethod
    def _menu_crear_personaje():
        """Abre el menú para crear un personaje."""
        personaje = Personaje()
        if not Menu._asignar_sten(personaje):
            return

        if not Menu._asignar_jugador(personaje):
            return

        if not Menu._asignar_nombre(personaje):
            return

        if not Menu._asignar_atributos(personaje):
            return

        personaje.asignar_habilidades()
        personaje.calcular_xp_req_habilidades()
        personaje.actualizar_cualidades(personaje.sten)
        personajes = Personaje.leer_datos_personajes() # Borrar JSON
        personaje.guardar_personajes(personajes) # Borrar JSON
        personaje.insert_personaje()

    @staticmethod
    def _asignar_sten(personaje):
        """El usuario asigna la verión de STEN que usará el personaje."""
        while True:
            eleccion = Menu._input_eleccion_menu("\nElija la versión de STEN que va a usar su personaje.\n1. STEN\n2. STEN2\n0. Salir\n: ",
                                                 "Debes ingresar una de las opciones del menú.", [0, 1, 2])

            if eleccion == 0:
                return False

            if eleccion == 1 or eleccion == 2:
                personaje.asignar_sten(eleccion)
                return True
            else:
                print("La versión de STEN solo puede ser 1 o 2.")

    @staticmethod
    def _asignar_jugador(personaje):
        """El usuario asigna el nombre del jugador."""
        while True:
            print("\nIngrese 'q' para salir.")
            nombre = input("Nombre de jugador: ")

            if nombre.lower() == "q":
                return False

            if len(nombre) > 0:
                personaje.asignar_jugador(nombre)
                return True
            else:
                print("El nombre del jugador no puede estar vacío.")

    @staticmethod
    def _asignar_nombre(personaje):
        """El usuario asigna el nombre del personaje."""
        while True:
            print("\nIngrese 'q' para salir.")
            nombre = input("Nombre de personaje: ")

            if nombre.lower() == "q":
                return False

            if len(nombre) > 0:
                personaje.asignar_nombre(nombre)
                return True
            else:
                print("El nombre del personaje no puede estar vacío.")

    @staticmethod
    def _asignar_atributos(personaje):
        """Acompaña al usuario para asignar los atributos del personaje."""
        (primario, secundario, terciario) = Menu._asignar_rango(personaje)
        if (primario, secundario, terciario) == (0, 0, 0):
            return False
        (primario, secundario, terciario) = Menu._asignar_enfoque(personaje, primario, secundario, terciario)
        if (primario, secundario, terciario) == (0, 0, 0):
            return False
        bloque_atributos = Menu._elegir_bloque_atributos(primario, secundario, terciario)

        if bloque_atributos:
            grupos = ["fisico", "mental", "sobrenatural"]

            for grupo in grupos:
                if bloque_atributos[grupo] == 1:
                    puntos = primario
                elif bloque_atributos[grupo] == 2:
                    puntos = secundario
                elif bloque_atributos[grupo] == 3:
                    puntos = terciario

                Menu._distribuir_atributos(personaje, grupo, puntos)
            
            return True
        else:
            return False

    @staticmethod
    def _asignar_rango(personaje):
        """Abre el menú para acompañar al usuario a elegir su rango."""
        while True:
            rango = Menu._input_eleccion_menu("\nElija su rango.\n1. Vulgar\n2. Capacitado\n3. Luchador\n4. Héroe\n0. Salir\nIngrese el número para elegir su rango: ",
                                            "Para elegir un rango debes ingresar un número entre el 1 y el 4.", [0, 1, 2, 3, 4])
            if rango == 0:
                return (0, 0, 0)

            return personaje.asignar_rango(rango)

    @staticmethod
    def _asignar_enfoque(personaje, primario, secundario, terciario):
        """Abre el menú para acompañar al usuario a elegir su enfoque."""
        while True:
            enfoque = Menu._input_eleccion_menu(f"\nElija su enfoque.\n1. Equilibrado [{primario}, {secundario}, {terciario}]\n2. Focalizado [{primario}, {secundario + 1}, {terciario - 1}]\n3. Muy focalizado [{primario + 1}, {secundario}, {terciario - 2}]\n4. Centrado [{primario + 1}, {secundario - 1}, {terciario - 1}]\n0. Salir\nIngrese el número para elegir su enfoque: ",
                                                "Para elegir un enfoque debes ingresar un número entre el 1 y el 4.", [0, 1, 2, 3, 4])

            if enfoque == 0:
                return (0, 0, 0)

            return personaje.asignar_enfoque(enfoque, primario, secundario, terciario)

    @staticmethod
    def _elegir_bloque_atributos(primario, secundario, terciario):
        """Abre el menú para acompañar al usuario a elegir que valor va a cada bloque de atributos."""
        while True:
            print(f"\nSegún tu rango y tu enfoque estos son los valores que tienes para asignar: {primario} {secundario} {terciario}")
            bloque = Menu._input_eleccion_menu(f"Asigna el valor más alto ({primario}) a un bloque de atributos.\n1. Físico\n2. Mental\n3. Sobrenatural\n0. Salir\nElija un bloque de atirbutos: ",
                                               "Para asignar un valor a un bloque de atributos debe ingresar un número entre el 1 y el 3.",
                                               [0, 1, 2, 3])
            bloques_atributos = {}

            if bloque == 0:
                break
            # Se asigna el primer bloque de atributo
            elif bloque == 1:
                fisico = primario
                mental = None
                sobrenatural = None
                bloques_atributos["fisico"] = 1
                print(f"\nTe quedan dos valores para asignar: {secundario} {terciario}.\nEl valor que no asignes, se asignará automáticamente al bloque que quede.")
                while True:
                    bloque = Menu._input_eleccion_menu(f"Asigna el valor más alto ({secundario}) a un bloque de atributos.\n1. Mental\n2. Sobrenatural\n0. Atrás\nElija un bloque de atirbutos: ",
                                                       "Ingrese una de las opciones del menú.", [0, 1, 2])
                    if bloque == 0:
                        break
                    elif bloque == 1 or bloque == 2:
                        return Menu._seguir_bloque_atributos(bloques_atributos, bloque, secundario, terciario, fisico, mental, sobrenatural)
            elif bloque == 2:
                fisico = None
                mental = primario
                sobrenatural = None
                bloques_atributos["mental"] = 1
                print(f"\nTe quedan dos valores para asignar: {secundario} {terciario}.\nEl valor que no asignes, se asignará automáticamente al bloque que quede.")
                while True:
                    bloque = Menu._input_eleccion_menu(f"Asigna el valor más alto ({secundario}) a un bloque de atributos.\n1. Físico\n2. Sobrenatural\n0. Atrás\nElija un bloque de atirbutos: ",
                                                       "Ingrese una de las opciones del menú.", [0, 1, 2])
                    if bloque == 0:
                        break
                    elif bloque == 1 or bloque == 2:
                        return Menu._seguir_bloque_atributos(bloques_atributos, bloque, secundario, terciario, fisico, mental, sobrenatural)
            elif bloque == 3:
                fisico = None
                mental = None
                sobrenatural = primario
                bloques_atributos["sobrenatural"] = 1
                print(f"\nTe quedan dos valores para asignar: {secundario} {terciario}.\nEl valor que no asignes, se asignará automáticamente al bloque que quede.")
                while True:
                    bloque = Menu._input_eleccion_menu(f"Asigna el valor más alto ({secundario}) a un bloque de atributos.\n1. Físico\n2. Mental\n0. Atrás\nElija un bloque de atirbutos: ",
                                                       "Ingrese una de las opciones del menú.", [0, 1, 2])
                    if bloque == 0:
                        break
                    elif bloque == 1 or bloque == 2:
                        return Menu._seguir_bloque_atributos(bloques_atributos, bloque, secundario, terciario, fisico, mental, sobrenatural)

    @staticmethod
    def _seguir_bloque_atributos(bloques_atributos, bloque, secundario, terciario, fisico, mental, sobrenatural):
        """Acompaña al usuario a elegir los dos bloques de atributos que le faltan."""
        # Se asigna el segundo y tercer bloque de atributo
        if bloque == 1 and mental == None and sobrenatural == None:
            mental = secundario
            sobrenatural = terciario
            bloques_atributos["mental"] = 2
            bloques_atributos["sobrenatural"] = 3
        elif bloque == 1 and fisico == None and sobrenatural == None:
            fisico = secundario
            sobrenatural = terciario
            bloques_atributos["fisico"] = 2
            bloques_atributos["sobrenatural"] = 3
        elif bloque == 1 and fisico == None and mental == None:
            fisico == secundario
            mental == terciario
            bloques_atributos["fisico"] = 2
            bloques_atributos["mental"] = 3
        elif bloque == 2 and mental == None and sobrenatural == None:
            sobrenatural = secundario
            mental = terciario
            bloques_atributos["sobrenatural"] = 2
            bloques_atributos["mental"] = 3
        elif bloque == 2 and fisico == None and sobrenatural == None:
            sobrenatural = secundario
            fisico = terciario
            bloques_atributos["sobrenatural"] = 2
            bloques_atributos["fisico"] = 3
        elif bloque == 2 and fisico == None and mental == None:
            mental = secundario
            fisico = terciario
            bloques_atributos["mental"] = 2
            bloques_atributos["fisico"] = 3

        return bloques_atributos

    @staticmethod
    def _distribuir_atributos(personaje, bloque, puntos):
        """Acompaña al usuario a distribuir sus atributos."""
        if bloque == "fisico":
            atributos = ["fuerza", "agilidad", "resistencia"]
        elif bloque == "mental":
            atributos = ["voluntad", "inteligencia", "liderazgo"]
        elif bloque == "sobrenatural":
            atributos = ["potencia", "defensa", "extensión"]

        for atributo in atributos:
            valor_maximo = 5
            if puntos < 5:
                valor_maximo = puntos
            lista_opciones_validas = list(range(valor_maximo + 1))

            if atributo == "resistencia" or atributo == "liderazgo" or atributo == "extensión":
                eleccion = valor_maximo
                print(f"\nSu atributo {atributo} queda en {eleccion}")
            else:
                while True:
                    eleccion = Menu._input_eleccion_menu(f"\nDistribuyamos los puntos en cada atributo.\nEmpecemos con el bloque {bloque}. Tienes {puntos} puntos para distribuir.\n¿Cuántos puntos van a ir a la {atributo} [0-{valor_maximo}]?: ",
                                                         f"No puedes tener menos de 0 puntos ni más de {valor_maximo} puntos en {atributo}.",
                                                         lista_opciones_validas)
                    if eleccion >= 0 and eleccion <= valor_maximo:
                        break

            if eleccion >= 0 and eleccion <= valor_maximo:
                personaje._set_atributo_by_str(atributo, eleccion)
                puntos -= eleccion

    @staticmethod
    def _menu_lista_personajes():
        """Muestra una lista de todos los personajes para que el usuario elija cual quiere ver."""
        while True:
            # Obtenemos los personajes como una lista de objetos Personaje
            #personajes = Personaje.json_a_personaje() # Borrar JSON
            #personajes = Personaje.select_personajes() # Obtenemos los personajes en un diccionario
            personajes = Personaje.db_a_personaje() # Obtenemos los personajes como objetos

            print("\n-------------------------------- Personajes --------------------------------")

            opciones_pjs = "\n"
            opciones_menu = [0]
            i = 0

            if personajes:
                for personaje in personajes:
                    i += 1
                    #opciones_pjs += f"{i}. {personaje.nombre}\n" # Borrar JSON
                    opciones_pjs += f"{i}. {personaje.nombre}\n"
                    opciones_menu.append(i)
            else:
                print("Todavía no tienes personajes creados.\n")

            opciones_pjs += "0. Atrás\n: "

            eleccion = Menu._input_eleccion_menu(opciones_pjs, f"\nDebes ingresar una opción del menú. Para salir 0.", opciones_menu)

            if eleccion == 0:
                break
            else:
                if personajes:
                    i = 1
                    for personaje in personajes:
                        if i == eleccion:
                            Menu._menu_personaje(personaje)
                        i += 1

    @staticmethod
    def _menu_personaje(personaje):
        """Abre el menú del personaje, para que el usuario pueda administrarlo."""
        while True:
            Menu._mostrar_personaje(personaje)

            eleccion = Menu._input_eleccion_menu("\n1. Habilidades\n2. Equipo\n3. Esferas\n4. Combate\n5. Motivación\n6. Energía\n7. Ascender\n8. Modificadores\n0. Atrás\n: ",
                                                "\nPara seleccionar una opción del menú ingrese un número entre el 1 y el 8.",
                                                [0, 1, 2, 3, 4, 5, 6, 7, 8])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_habilidades(personaje)
            elif eleccion == 2:
                Menu._menu_equipo(personaje)
            elif eleccion == 3:
                if(Menu._menu_esferas(personaje)):
                    break
            elif eleccion == 4:
                Menu._menu_combate(personaje)
            elif eleccion == 5:
                Menu._menu_motivacion(personaje)
            elif eleccion == 6:
                Menu._menu_energia(personaje)
            elif eleccion == 7:
                Menu._menu_ascender(personaje)
            elif eleccion == 8:
                Menu._menu_modificadores(personaje)

    @staticmethod
    def _mostrar_personaje(personaje):
        personaje = personaje.select_personaje() # Se vuelve a leer el personaje para actualizar los valores
        personaje = personaje[0]
        """Muestra el personaje pasado por parámetros."""
        print(f"\n-------------------------------- {personaje["nombre"]} --------------------------------\n")
        consola = Console()
        tabla = Table(show_header=False, box=None, padding=(0, 1))
        tabla.add_row(f"[underline]Jugador                                {personaje["jugador"]}[/]")
        tabla.add_row(f"[underline]Rango                                  {Personaje.convertir_rango_a_str(personaje["rango"])}[/]")
        tabla.add_row(f"[underline]Fuerza                                 {personaje["fuerza"]}[/]")
        tabla.add_row(f"[underline]Agilidad                               {personaje["agilidad"]}[/]")
        tabla.add_row(f"[underline]Resistencia                            {personaje["resistencia"]}[/]")
        tabla.add_row(f"[underline]Voluntad                               {personaje["voluntad"]}[/]")
        tabla.add_row(f"[underline]Inteligencia                           {personaje["inteligencia"]}[/]")
        tabla.add_row(f"[underline]Liderazgo                              {personaje["liderazgo"]}[/]")
        tabla.add_row(f"[underline]Potencia                               {personaje["potencia"]}[/]")
        tabla.add_row(f"[underline]Defensa                                {personaje["defensa"]}[/]")
        tabla.add_row(f"[underline]Extensión                              {personaje["extension"]}[/]")
        tabla.add_row(f"[underline]Esferas                                {personaje["cantidad_esferas"]}[/]")
        tabla.add_row(f"[underline]Vida                                   {personaje["vida"]}[/]")
        tabla.add_row(f"[underline]Muerte                                 {personaje["muerte"]}[/]")
        tabla.add_row(f"[underline]Aguante                                {personaje["aguante"]}[/]")
        tabla.add_row(f"[underline]Recuperación                           {personaje["recuperacion"]}[/]")
        tabla.add_row(f"[underline]Iniciativa                             {personaje["iniciativa"]}[/]")
        tabla.add_row(f"[underline]Carga total                            {personaje["carga_total"]}[/]")
        tabla.add_row(f"[underline]Carga en manos                         {personaje["carga_en_manos"]}[/]")
        tabla.add_row(f"[underline]Resistencia a la luz                   {personaje["resistencia_a_la_luz"]}[/]")
        tabla.add_row(f"[underline]Resistencia a la oscuridad             {personaje["resistencia_a_la_oscuridad"]}[/]")
        tabla.add_row(f"[underline]Resistencia elemental                  {personaje["resistencia_elemental"]}[/]")
        tabla.add_row(f"[underline]Escudo sobrenatural                    {personaje["escudo_sobrenatural"]}[/]")
        if personaje["modificador_vida"] != 0:
            tabla.add_row(f"[underline]Modificador vida                   {personaje["modificador_vida"]}[/]")
        if personaje["modificador_aguante"] != 0:
            tabla.add_row(f"[underline]Modificador aguante                {personaje["modificador_aguante"]}[/]")
        if personaje["modificador_recuperacion"] != 0:
            tabla.add_row(f"[underline]Modificador recuperación           {personaje["modificador_recuperacion"]}[/]")
        if personaje["modificador_iniciativa"] != 0:
            tabla.add_row(f"[underline]Modificador iniciativa             {personaje["modificador_iniciativa"]}[/]")
        if personaje["modificador_luz"] != 0:
            tabla.add_row(f"[underline]Modificador resistencia luz        {personaje["modificador_luz"]}[/]")
        if personaje["modificador_oscuridad"] != 0:
            tabla.add_row(f"[underline]Modificador resistencia oscuridad  {personaje["modificador_oscuridad"]}[/]")
        if personaje["modificador_elemental"] != 0:
            tabla.add_row(f"[underline]Modificador resistencia elemental  {personaje["modificador_elemental"]}[/]")
        if personaje["modificador_escudo_sobrenatural"] != 0:
            tabla.add_row(f"[underline]Modificador escudo sobrenatural    {personaje["modificador_escudo_sobrenatural"]}[/]")
        tabla.add_row(f"[underline]Motivación                             {personaje["motivacion"]}[/]")
        tabla.add_row(f"[underline]Energía                                {personaje["energia"]}[/]")
        consola.print(tabla)

    @staticmethod
    def _menu_habilidades(personaje):
        """Abre el menú de habilidades del personaje."""
        while True:
            print(f"\n-------------------------------- Habilidades de {personaje.nombre} --------------------------------")
            print("\nNombre | Nivel | Atributos | XP\n")
            pj_habilidades = Personaje.select_personaje_habilidad(personaje.id)

            i = 1
            opciones_menu = [0]
            for pj_habilidad in pj_habilidades:
                if pj_habilidad["nivel"] > 0:
                    cant_espacios_nom = 0
                    espacios_nom = ""
                    cant_espacios_atr = 0
                    espacios_atr = ""
                    atributos_relacionados = Personaje.select_habilidad_atributo(pj_habilidad["id"])
                    if len(pj_habilidad["nombre"]) < 32:
                        cant_espacios_nom += 32 - len(pj_habilidad["nombre"])
                        espacios_nom = " " * cant_espacios_nom
                    if len(atributos_relacionados) == 1:
                        cant_espacios_atr += 10
                        espacios_atr = " " * cant_espacios_atr
                    elif len(atributos_relacionados) == 2:
                        cant_espacios_atr += 5
                        espacios_atr = " " * cant_espacios_atr

                    atr_rel = [str(a["atributo"]) for a in atributos_relacionados]
                    print(f"{pj_habilidad["nombre"]}{espacios_nom} | {pj_habilidad["nivel"]} | {atr_rel}{espacios_atr} | {pj_habilidad["xp"]}/{pj_habilidad["xp_requerida"]}")
                    opciones_menu.append(i)
                i += 1

            eleccion = Menu._input_eleccion_menu("\n1. Administrar\n0. Atrás\n: ",
                                                "\nIngrese el número de la opción a la que quiera acceder, luego pulse 'Enter'.",
                                                [0, 1])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_administrar_habilidades(personaje)

    @staticmethod
    def _menu_administrar_habilidades(personaje):
        """Abre el menu de administración de habilidades."""
        while True:
            print(f"\n-------------------------------- Habilidades de {personaje.nombre} --------------------------------")
            print("\nNombre | Nivel | Atributos | XP\n")
            pj_habilidades = Personaje.select_personaje_habilidad(personaje.id)

            i = 1
            opciones_menu = [0]
            for pj_habilidad in pj_habilidades:
                cant_espacios_nom = 0
                espacios_nom = ""
                cant_espacios_atr = 0
                espacios_atr = ""
                atributos_relacionados = Personaje.select_habilidad_atributo(pj_habilidad["id"])
                if len(pj_habilidad["nombre"]) < 32:
                    cant_espacios_nom += 32 - len(pj_habilidad["nombre"])
                    espacios_nom = " " * cant_espacios_nom
                    if i < 10:
                        espacios_nom += " "
                if len(atributos_relacionados) == 1:
                    cant_espacios_atr += 10
                    espacios_atr = " " * cant_espacios_atr
                elif len(atributos_relacionados) == 2:
                    cant_espacios_atr += 5
                    espacios_atr = " " * cant_espacios_atr

                atr_rel = [str(a["atributo"]) for a in atributos_relacionados]
                print(f"{i}. {pj_habilidad["nombre"]}{espacios_nom} | {pj_habilidad["nivel"]} | {atr_rel}{espacios_atr} | {pj_habilidad["xp"]}/{pj_habilidad["xp_requerida"]}")
                opciones_menu.append(i)
                i += 1

            (num_hab, xp) = Menu._input_eleccion_menu_comando("\nIngrese el número de habilidad seguido de la experiencia que quiere agregar. Ejemplo: [35 5]\nSi quiere quitar experiencia o incluso bajar de nivel, use [35 -5]. La motivación se le devolverá al personaje automáticamente.\n: ",
                                                        f"Debes ingresar un número de habilidad entre el 1 y el {i}.", opciones_menu)

            if num_hab == 0:
                break

            habilidades = Personaje.select_personaje_habilidad(personaje.id)
            for pj_habilidad in habilidades:
                if num_hab == pj_habilidad["id"]:
                    personaje.subir_nivel_habilidad(pj_habilidad, xp)
                    break

    @staticmethod
    def _menu_equipo(personaje):
        """Abre el menú para ver y administrar el equipo."""
        while True:
            print(f"\n-------------------------------- Equipo de {personaje.nombre} --------------------------------")
            Menu._mostrar_equipo(personaje)

            eleccion = input("\nPara las opciones 4 para arriba escriba la opción del menú, seguido de el número de ID. Ejemplo [7 2]\n1. Equipar arma\n2. Equipar armadura\n3. Equipar escudo\n4. Desequipar arma\n5. Desequipar armadura\n6. Desequipar escudo\n7. Cualidades armas\n8. Cualidades armaduras\n9. Cualidades escudos\n0. Atrás\n: ")
            
            if len(eleccion) > 1:
                entrada = eleccion.strip().split()

                if len(entrada) != 2:
                    print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de equipo>")
                else:
                    try:
                        opc_menu = int(entrada[0])
                        id = int(entrada[1])

                        if opc_menu < 4 or opc_menu > 9:
                            print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de equipo>")
                        elif opc_menu == 4:
                            Menu._desequipar_equipo(personaje, "Armas", id)
                        elif opc_menu == 5:
                            Menu._desequipar_equipo(personaje, "Armaduras", id)
                        elif opc_menu == 6:
                            Menu._desequipar_equipo(personaje, "Escudos", id)
                        elif opc_menu == 7:
                            Menu._menu_cambiar_cualidad_arma(personaje, id)
                        elif opc_menu == 8:
                            Menu._menu_cambiar_cualidad_armadura(personaje, id)
                        elif opc_menu == 9:
                            Menu._menu_cambiar_cualidad_escudo(personaje, id)
                    except ValueError:
                        print("\nPor favor, ingresa solo números válidos.")
            else:
                try:
                    eleccion = int(eleccion)

                    if eleccion == 0:
                        break
                    elif eleccion < 0 or eleccion > 3:
                        print("Para seleccionar una opción del menú ingrese un número entre el 1 y el 3.")
                        return None
                    elif eleccion == 1:
                        Menu._menu_equipar_armas(personaje)
                    elif eleccion == 2:
                        Menu._menu_equipar_armaduras(personaje)
                    elif eleccion == 3:
                        Menu._menu_equipar_escudos(personaje)
                except ValueError:
                    print("\nDebes ingresar un número válido.")


    @staticmethod
    def _menu_equipar_armas(personaje):
        """Abre el menú de armas, donde el usuario puede agregar armas a su equipo."""
        while True:
            armas = Arma.db_a_armas(personaje.sten)
            print("\nNombre | Impacto | Daño | Alcance | Tipo de daño | Tipo de arma | Estructura | Peso")

            opciones_menu = [0]
            i = 1
            for arma in armas:
                cant_espacios_nom = 0
                espacios_nom = ""
                cant_espacios_tip_dano = 0
                espacios_tip_dano = ""
                cant_espacios_tip_arma = 0
                espacios_tip_arma = ""
                if len(arma.nombre) < 20:
                    cant_espacios_nom += 20 - len(arma.nombre)
                    espacios_nom = " " * cant_espacios_nom
                    if arma.id < 10:
                        espacios_nom += " "
                if len(arma.tipo_dano) < 11:
                    cant_espacios_tip_dano += 11 - len(arma.tipo_dano)
                    espacios_tip_dano = " " * cant_espacios_tip_dano
                if len(arma.tipo_arma) < 11:
                    cant_espacios_tip_arma += 11 - len(arma.tipo_arma)
                    espacios_tip_arma = " " * cant_espacios_tip_arma
                print(f"{arma.id}. {arma.nombre}{espacios_nom} | {arma.impacto} | {arma.dano} | {arma.alcance} | {arma.tipo_dano}{espacios_tip_dano} | {arma.tipo_arma}{espacios_tip_arma} | {arma.estructura} | {arma.peso}")
                opciones_menu.append(i)
                i += 1
            print("0. Atrás")

            eleccion = Menu._input_eleccion_menu("\nIngrese el número de arma que quieres agregar al personaje: ",
                                      f"Debes ingresar el número del arma.",
                                      opciones_menu)

            if eleccion == 0:
                break
            else:
                for arma in armas:
                    if eleccion == arma.id:
                        personaje.equipar_arma(arma)
                        print("Arma equipada")
                        return

    @staticmethod
    def _menu_equipar_armaduras(personaje):
        """Abre el menú de armaduras, donde el usuario puede agregar armaduras a su equipo."""
        while True:
            armaduras = Armadura.db_a_armaduras(personaje.sten)
            print("\nNombre | Contundente | Cortante | Perforante | Cobertura | Evasión | Penalizador | Estructura | Peso")

            opciones_menu = [0]
            i = 1
            for armadura in armaduras:
                cant_espacios_nom = 0
                espacios_nom = ""
                espacios_pen = ""
                if len(armadura.nombre) < 30:
                    cant_espacios_nom += 30 - len(armadura.nombre)
                    espacios_nom = " " * cant_espacios_nom
                    if armadura.id < 10:
                        espacios_nom += " "
                if armadura.penalizador == 0:
                    espacios_pen = " "
                print(f"{armadura.id}. {armadura.nombre}{espacios_nom} | {armadura.contundente} | {armadura.cortante} | {armadura.perforante} | {armadura.cobertura} | {armadura.evasion} | {armadura.penalizador}{espacios_pen} | {armadura.estructura} | {armadura.peso}")
                opciones_menu.append(i)
                i += 1
            print("0. Atrás")

            eleccion = Menu._input_eleccion_menu("\nIngrese el número de armadura que quieres agregar al personaje: ",
                                      f"Debes ingresar el número del armadura.",
                                      opciones_menu)

            if eleccion == 0:
                break
            else:
                for armadura in armaduras:
                    if eleccion == armadura.id:
                        print("Armadura equipada")
                        personaje.equipar_armadura(armadura)
                        return

    @staticmethod
    def _menu_equipar_escudos(personaje):
        """Abre el menú de escudos, donde el usuario puede agregar escudos a su equipo."""
        while True:
            escudos = Escudo.db_a_escudos(personaje.sten)
            print("\nNombre | Contundente | Cortante | Perforante | Cobertura | Evasión | Penalizador | Estructura | Peso")

            opciones_menu = [0]
            i = 1
            for escudo in escudos:
                cant_espacios_nom = 0
                espacios_nom = ""
                espacios_pen = ""
                if len(escudo.nombre) < 15:
                    cant_espacios_nom += 15 - len(escudo.nombre)
                    espacios_nom = " " * cant_espacios_nom
                    if escudo.id < 10:
                        espacios_nom += " "
                if escudo.penalizador == 0:
                    espacios_pen = " "
                print(f"{escudo.id}. {escudo.nombre}{espacios_nom} | {escudo.contundente} | {escudo.cortante} | {escudo.perforante} | {escudo.cobertura} | {escudo.evasion} | {escudo.penalizador}{espacios_pen} | {escudo.estructura} | {escudo.peso}")
                opciones_menu.append(i)
                i += 1
            print("0. Atrás")

            eleccion = Menu._input_eleccion_menu("\nIngrese el número de escudo que quieres agregar al personaje: ",
                                      f"Debes ingresar el número del escudo.",
                                      opciones_menu)

            if eleccion == 0:
                break
            else:
                for escudo in escudos:
                    if eleccion == escudo.id:
                        print("Escudo equipado")
                        personaje.equipar_escudo(escudo)
                        return

    @staticmethod
    def _desequipar_equipo(personaje, tipo_equipo, id_seleccionado):
        """Se encarga de desequipar cualquier tipo de equipo: armas, armaduras y escudos."""
        if tipo_equipo == "Armas":
            equipo = Arma.db_a_armas(personaje.sten)
        elif tipo_equipo == "Armaduras":
            equipo = Armadura.db_a_armaduras(personaje.sten)
        elif tipo_equipo == "Escudos":
            equipo = Escudo.db_a_escudos(personaje.sten)
        
        for item in equipo:
            if item.id == id_seleccionado:
                if tipo_equipo == "Armas":
                    personaje.desequipar_arma(item)
                    return
                elif tipo_equipo == "Armaduras":
                    personaje.desequipar_armadura(item)
                    return
                elif tipo_equipo == "Escudos":
                    personaje.desequipar_escudo(item)
                    return
        print(f"No tienes ningun equipo con el ID {id_seleccionado}")

    @staticmethod
    def _menu_cambiar_cualidad_arma(personaje, id_seleccionado):
        """Abre el menú que se encarga de acompañar al usuario a cambiar cualidades de su arma."""
        while True:
            eleccion = Menu._input_eleccion_menu("\nElije la cualidad que quieres cambiar de tu arma.\n1. Impacto\n2. Daño\n3. Calidad\n4. Estructura\n0. Atrás\n: ",
                                                 "Debe ingresar una opción del menú.", [0, 1, 2, 3, 4])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_arma", "impacto") # Llamada a función cambiar_cualidad_arma en personaje
                break
            elif eleccion == 2:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_arma", "dano") # Llamada a función cambiar_cualidad_arma en personaje
                break
            elif eleccion == 3:
                Menu._asignar_calidad(personaje, "Armas", id_seleccionado)
                break
            elif eleccion == 4:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_arma", "estructura") # Llamada a función cambiar_cualidad_arma en personaje

    @staticmethod
    def _menu_cambiar_cualidad_armadura(personaje, id_seleccionado):
        """Abre el menú que se encarga de acompañar al usuario a cambiar cualidades de su armadura."""
        while True:
            eleccion = Menu._input_eleccion_menu("\nElije la cualidad que quieres cambiar de tu armadura.\n1. Contundente\n2. Cortante\n3. Perforante\n4. Estructura\n5. Peso\n6. Cobertura\n7. Evasión\n8. Calidad\n0. Atrás\n: ",
                                                "Debe ingresar una opción del menú.", [0, 1, 2, 3, 4, 5, 6, 7, 8])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "contundente") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 2:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "cortante") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 3:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "perforante") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 4:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "estructura") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 5:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "peso") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 6:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "cobertura") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 7:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_armadura", "evasion") # Llamada a función cambiar_cualidad_armadura en personaje
                break
            elif eleccion == 8:
                Menu._asignar_calidad(personaje, "Armaduras", id_seleccionado)
                break

    @staticmethod
    def _menu_cambiar_cualidad_escudo(personaje, id_seleccionado):
        """Abre el menú que se encarga de acompañar al usuario a cambiar cualidades de su escudo."""
        while True:
            eleccion = Menu._input_eleccion_menu("\nElije la cualidad que quieres cambiar de tu escudo.\n1. Contundente\n2. Cortante\n3. Perforante\n4. Estructura\n5. Cobertura\n6. Evasión\n7. Calidad\n0. Atrás\n: ",
                                                "Debe ingresar una opción del menú.", [0, 1, 2, 3, 4, 5, 6, 7])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "contundente") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 2:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "cortante") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 3:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "perforante") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 4:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "estructura") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 5:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "cobertura") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 6:
                Menu._menu_cambiar_cualidad(personaje, id_seleccionado, "cambiar_cualidad_escudo", "evasion") # Llamada a función cambiar_cualidad_escudo en personaje
                break
            elif eleccion == 7:
                Menu._asignar_calidad(personaje, "Escudos", id_seleccionado)
                break

    @staticmethod
    def _menu_cambiar_cualidad(personaje, id, nombre_metodo, columna):
        """Acompaña al usuario a sumar o restar una cantidad a una cualidad de arma, armadura o escudo."""
        while True:
            (opc_menu, valor) = Menu._input_eleccion_menu_comando("\nElija si sumar o restar, seguido del valor que quieras operar. Ejemplo [1 2]\n1. Sumar\n2. Restar\n0. Atrás\n: ",
                                                         "\nFormato inválido. Debes ingresar <Opción de menú> <Valor a sumar o restar>",
                                                         [0, 1, 2])

            if opc_menu == 0:
                break
            elif opc_menu == 1 or opc_menu == 2:
                metodo = getattr(personaje, nombre_metodo, None) # Llama al método pasado por argumento
                if not metodo:
                    print(f"Error: el método '{nombre_metodo}' no existe en el objeto personaje.")
                    return

                metodo(id, opc_menu, columna, valor)
                break

    @staticmethod
    def _asignar_calidad(personaje, tipo_equipo, id_seleccionado):
        """Se encarga de asignar la calidad de cualquier equipo: armas, armaduras y escudos."""
        while True:
            try:
                nueva_calidad = int(input("\nElija la nueva calidad: "))

                if nueva_calidad >= 0 and nueva_calidad <= 5:
                    personaje.cambiar_calidad_objeto(id_seleccionado, tipo_equipo, nueva_calidad)
                    return
                else:
                    print("\n\033[31mEl equipo solo puede tener calidad entre 0 y 5.\033[0m")
            except ValueError:
                print("\n\033[31mIngrese un número válido entre 0 y 5.\033[0m")

    @staticmethod
    def _mostrar_equipo(personaje):
        """Muestra el equipo del personaje."""
        equipo_max_len = Equipo._equipo_max_longitud(personaje.sten)
        armas = Personaje.select_personaje_arma(personaje.id)
        armaduras = Personaje.select_personaje_armadura(personaje.id)
        escudos = Personaje.select_personaje_escudo(personaje.id)

        if armas:
            print("\nArmas:")
            for arma in armas:
                espacios_id = ""
                espacios_nom = ""
                espacios_dano = ""
                espacios_tipo_dano = ""
                espacios_ini = ""
                espacios_peso = ""
                espacios_tipo_arma = ""
                for i in range(len(str(arma["id_pj_arma"])) - 1):
                    espacios_id += " "
                #if arma["id_pj_arma"] < 10:
                #    espacios_id += " "
                for i in range(Menu._num_dif_palabras(arma["nombre"], equipo_max_len)):
                    espacios_nom += " "
                for i in range(Menu._num_dif_palabras(arma["tipo_de_dano"], "Contundente")):
                    espacios_tipo_dano += " "
                if arma["dano"] < 10:
                    espacios_dano += " "
                if arma["iniciativa"] < 10:
                    espacios_ini += " "
                if len(str(arma["peso"])) == 1:
                    espacios_peso += "   "
                elif len(str(arma["peso"])) == 3:
                    espacios_peso += " "
                for i in range(Menu._num_dif_palabras(arma["tipo_de_arma"], "Proyectiles")):
                    espacios_tipo_arma += " "
                print(f"{arma["id_pj_arma"]}.{espacios_id} {arma["nombre"]} {espacios_nom}| Impacto {arma["impacto"]} | Daño {arma["dano"]}{espacios_dano} | {arma["tipo_de_dano"]}{espacios_tipo_dano} | Iniciativa {arma["iniciativa"]}{espacios_ini} | Estructura {arma["estructura"]} | Peso {arma["peso"]}{espacios_peso} | Alcance {arma["alcance"]} | Tipo arma '{arma["tipo_de_arma"]}'{espacios_tipo_arma} | Calidad {arma["calidad"]}")

        if armaduras:
            print("\nArmaduras:")
            for armadura in armaduras:
                espacios_id = ""
                espacios_nom = ""
                espacios_est = ""
                espacios_peso = ""
                espacios_pen = ""
                for i in range(len(str(armadura["id_pj_armadura"])) - 1):
                    espacios_id += " "
                if armadura["estructura"] < 10:
                    espacios_est += " "
                if armadura["peso"] < 10:
                    espacios_peso += " "
                if armadura["penalizador"] == 0:
                    espacios_pen += " "
                for i in range(Menu._num_dif_palabras(armadura["nombre"], equipo_max_len)):
                    espacios_nom += " "
                print(f"{armadura["id_pj_armadura"]}.{espacios_id} {armadura["nombre"]} {espacios_nom}| Contundente {armadura["contundente"]} | Cortante {armadura["cortante"]} | Perforante {armadura["perforante"]} | Cobertura {armadura["cobertura"]} | Evasion {armadura["evasion"]} | Estructura {armadura["estructura"]}{espacios_est} | Peso {armadura["peso"]}{espacios_peso} | Penalizador {armadura["penalizador"]}{espacios_pen} | Calidad {armadura["calidad"]}")

        if escudos:
            print("\nEscudos:")
            for escudo in escudos:
                espacios_id = ""
                espacios_nom = ""
                espacios_peso = ""
                for i in range(Menu._num_dif_palabras(escudo["nombre"], equipo_max_len)):
                    espacios_nom += " "
                for i in range(len(str(escudo["id_pj_escudo"])) - 1):
                    espacios_id += " "
                if len(str(escudo["peso"])) < 2:
                    espacios_peso += "  "
                print(f"{escudo["id_pj_escudo"]}.{espacios_id} {escudo["nombre"]} {espacios_nom}| Contundente {escudo["contundente"]} | Cortante {escudo["cortante"]} | Perforante {escudo["perforante"]} | Cobertura {escudo["cobertura"]} | Evasion {escudo["evasion"]} | Estructura {escudo["estructura"]} | Peso {escudo["peso"]}{espacios_peso} | Penalizador {escudo["penalizador"]} | Calidad {escudo["calidad"]}")

    @staticmethod
    def _menu_combate(personaje):
        """Abre menú para administrar todos los atributos de combate así como las cualidades."""
        while True:
            print(f"\n-------------------------------- {personaje.nombre} en combate --------------------------------\n")
            Menu._mostrar_atributos_combate(personaje)

            eleccion = input("\n1. Gastar un punto aguante\n2. Recibir daño\n3. Concentrarse\n4. Recuperar aguante\n5. Recuperar vida\n6. Gastar concentración\n7. Gastar un punto energía\n8. Curar herida grave\n9. Ronda nueva\n0. Atrás\n: ")
            print("")

            if len(eleccion) > 1:
                entrada = eleccion.strip().split()
                if len(entrada) != 2:
                    print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de equipo>")
                else:
                    try:
                        opc_menu = int(entrada[0])
                        valor = int(entrada[1])

                        if opc_menu < 2 or opc_menu > 6:
                            print("\nPara las opciones 2 a 6 del menú, debes ingresar <Opción de menú> <Valor a sumar o restar>. Ejemplo [3 5]")
                        elif opc_menu == 2:
                            personaje.recibir_dano(valor)
                        elif opc_menu == 3:
                            personaje.ganar_concentracion(valor)
                        elif opc_menu == 4:
                            personaje.recuperar_aguante(valor)
                        elif opc_menu == 5:
                            personaje.recuperar_vida(valor)
                        elif opc_menu == 6:
                            personaje.perder_concentracion(valor)
                    except ValueError:
                        print("\nPor favor, ingresa solo números válidos.")
            else:
                try:
                    eleccion = int(eleccion)

                    if eleccion == 0:
                        break
                    elif eleccion not in (1, 7, 8, 9):
                        print("\nPara las opciones 2 a 6 del menú, debes ingresar <Opción de menú> <Valor a sumar o restar>. Ejemplo [3 5]")
                    elif eleccion == 1:
                        personaje.gastar_aguante()
                    elif eleccion == 7:
                        personaje.gastar_energia()
                    elif eleccion == 8:
                        personaje.curar_herida_grave()
                    elif eleccion == 9:
                        personaje.ronda_nueva()
                except ValueError:
                    print("\nPor favor, ingresa solo números válidos.")

    @staticmethod
    def _mostrar_atributos_combate(personaje):
        """Muestra todos los atributos de combate."""
        Menu._mostrar_equipo(personaje)
        consola = Console()
        tabla = Table(show_header=False, box=None, padding=(0, 1))
        tabla.add_row(f"[underline]Fuerza                      {personaje.fuerza}[/]")
        tabla.add_row(f"[underline]Agilidad                    {personaje.agilidad}[/]")
        tabla.add_row(f"[underline]Resistencia                 {personaje.resistencia}[/]")
        tabla.add_row(f"[underline]Voluntad                    {personaje.voluntad}[/]")
        tabla.add_row(f"[underline]Inteligencia                {personaje.inteligencia}[/]")
        tabla.add_row(f"[underline]Liderazgo                   {personaje.liderazgo}[/]")
        tabla.add_row(f"[underline]Potencia                    {personaje.potencia}[/]")
        tabla.add_row(f"[underline]Defensa                     {personaje.defensa}[/]")
        tabla.add_row(f"[underline]Extensión                   {personaje.extension}[/]")
        tabla.add_row(f"[underline]Aguante actual              {personaje.aguante_actual}[/]")
        tabla.add_row(f"[underline]Aguante gastado por turno   {personaje.aguante_gastado_por_turno}[/]")
        tabla.add_row(f"[underline]Vida actual                 {personaje.vida_actual}[/]")
        tabla.add_row(f"[underline]Muerte                      {personaje.muerte}[/]")
        tabla.add_row(f"[underline]Resistencia luz             {personaje.resistencia_luz}[/]")
        tabla.add_row(f"[underline]Resistencia Oscuridad       {personaje.resistencia_oscuridad}[/]")
        tabla.add_row(f"[underline]Resistencia elemental       {personaje.resistencia_elemental}[/]")
        tabla.add_row(f"[underline]Escudo sobrenatural         {personaje.escudo_sobrenatural}[/]")
        tabla.add_row(f"[underline]Concentración               {personaje.concentracion}[/]")
        tabla.add_row(f"[underline]Energía                     {personaje.energia}[/]")
        tabla.add_row(f"[underline]Aturdido                    {personaje.turnos_aturdido}[/]")
        consola.print(tabla)

    @staticmethod
    def _menu_esferas(personaje):
        """Abre el menú para ver y administrar las esferas"""
        while True:
            print(f"\n-------------------------------- Esferas de {personaje.nombre} --------------------------------")
            Menu._mostrar_esferas(personaje)
            eleccion = Menu._input_eleccion_menu("\n1. Agregar esfera\n2. Quitar esfera\n0. Atrás\n: ",
                                                            f"Debes ingresar un número del menú.", [0, 1, 2])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._agregar_esfera(personaje)
                return True # Indica que se agregó una esfera y se tiene que volver al menu de personajes
            elif eleccion == 2:
                Menu._quitar_esfera(personaje)
                return True # Indica que se quitó una esfera y se tiene que volver al menu de personajes

    @staticmethod
    def _mostrar_esferas(personaje=None):
        """Si se pasa un personaje por parámetros, muestra todas sus esferas. Sino se muestra una lista de todas las esferas."""
        if personaje != None:
            esferas = Personaje.select_personaje_esfera(personaje.id)
            esferas_dic = {}

            if personaje.sten == 1:
                version = "STEN1"
            elif personaje.sten == 2:
                version = "STEN2"

            # Se preparan los datos de las esferas
            for fila in esferas:
                esfera_nombre = fila["nombre_e"]
                poder_id = fila['nombre_p']
                parametros = (fila['nombre_prm'], fila['valor'])

                # Si la esfera todavía no existe, la creamos
                if esfera_nombre not in esferas_dic:
                    if version == "STEN1":
                        pasiva = fila["pasiva_sten1"]
                    elif version == "STEN2":
                        pasiva = fila["pasiva_sten2"]

                    esferas_dic[esfera_nombre] = {
                        "id": fila["id"],
                        "afinidad": fila["afinidad"],
                        "nivel": fila["nivel"],
                        "pasiva": pasiva,
                        "poderes": {}
                    }

                # Si el poder todavía no existe en esta esfera, lo creamos
                if poder_id not in esferas_dic[esfera_nombre]["poderes"]:
                    if version == "STEN1":
                        efecto = fila["efecto_sten1"]
                    elif version == "STEN2":
                        efecto = fila["efecto_sten2"]

                    esferas_dic[esfera_nombre]["poderes"][poder_id] = {
                        "descripcion": fila["descripcion"],
                        "efecto": efecto,
                        "parametros": []
                    }

                # Agregamos parámetros solo si son de la versión correcta
                if fila["version"] == version and parametros not in esferas_dic[esfera_nombre]["poderes"][poder_id]["parametros"]:
                    esferas_dic[esfera_nombre]["poderes"][poder_id]["parametros"].append(parametros)

            # Se muestran las esferas
            for esfera, valores in esferas_dic.items():
                print(f"\n·Esfera: [{esfera.upper()}]")
                print(f"\n·ID: {valores["id"]}")
                print(f"·Afinidad: {valores["afinidad"]}")
                print(f"·Nivel: {valores["nivel"]}")
                print(f"\n·Pasiva: {valores["pasiva"]}")

                print("\n↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓")
                for poder, datos in valores["poderes"].items():
                    print(f"\n·Poder: {poder}")
                    print(f"Descripción: {datos['descripcion']}\nEfecto: {datos['efecto']}")
                    print(f"\n·Parámetro:")
                    for prm_nombre, valor in datos["parametros"]:
                        print(f"\t{prm_nombre} = {valor}")
                    print("\n------------------------------------------------------------------------------------------------")
        else: # Si no se pasa personaje por argumento, se muestran todas las esferas
            esferas = Esfera.leer_datos_esferas() # Borrar JSON
            esferas = base_datos.select_esferas()
            for fila in esferas:
                esfera = dict(fila)
                print(f"{esfera["id"]}. {esfera["nombre"]}")

    @staticmethod
    def _agregar_esfera(personaje):
        """Acompaña al usuario para agregar una esfera al personaje."""
        while True:
            print(f"\n-------------------------------- Agregar esfera a {personaje.nombre} --------------------------------")
            Menu._mostrar_esferas()
            opciones = [0] + list(range(40, 65 + 1))
            eleccion = Menu._input_eleccion_menu(f"\nElija la esfera que quieres agregar a {personaje.nombre}\n: ",
                                                 "\nIngrese una esfera válida.", opciones)

            if eleccion == 0:
                break
            elif eleccion in opciones:
                personaje.agregar_esfera(eleccion)
                break

    @staticmethod
    def _quitar_esfera(personaje):
        """Acompaña al usuario para quitar una esfera al personaje."""
        while True:
            print(f"\n-------------------------------- Quitar esfera a {personaje.nombre} --------------------------------")
            print("\nIMPORTANTE: Esta opción está solo por si agregaste una esfera por error al personaje. Según las reglas del juego, una vez agregas una esfera a un personaje, esta te acompaña para siempre.")

            habilidades = Personaje.select_personaje_habilidad(personaje.id)
            esferas = Personaje.select_personaje_esfera(personaje.id)

            nombres = []
            for esfera in esferas:
                if esfera["nombre_e"] not in nombres:
                    nombres.append(f"Esfera ({esfera["nombre_e"]})")

            opciones = [0]
            for hab in habilidades:
                if hab["nombre"] in nombres:
                    print(f"{hab["id"]}. {hab["nombre"]}")
                    opciones.append(hab["id"])

            eleccion = Menu._input_eleccion_menu(f"\nElija la esfera que quieres eliminar a {personaje.nombre}\n: ",
                                                 "\nIngrese una esfera válida.", opciones)

            if eleccion == 0:
                break
            elif eleccion in opciones:
                personaje.quitar_esfera(eleccion)
                break

    @staticmethod
    def _menu_motivacion(personaje):
        """Abre el menú para agregar o quitar motivación al personaje."""
        while True:
            print(f"\n-------------------------------- Motivación para {personaje.nombre} --------------------------------")
            print(f"Motivación actual: {personaje.motivacion}")

            (opc_menu, motivacion) = Menu._input_eleccion_menu_comando("\nIngrese la opción de menú seguido de la motivación que quiere agregar o quitar. Ejemplo: [1 10]\n1. Agregar motivación\n2. Quitar motivación\n0. Atrás\n: ",
                                                         "Para seleccionar una opción del menú ingrese un número entre el 1 y el 2.",
                                                         [0, 1, 2])

            if opc_menu == 0:
                break
            elif opc_menu == 1:
                personaje.agregar_motivacion(motivacion)
                break
            elif opc_menu == 2:
                personaje.quitar_motivacion(motivacion)
                break

    @staticmethod
    def _menu_energia(personaje):
        """Abre el menú para agregar o quitar energía al personaje."""
        while True:
            print(f"\n-------------------------------- Energía para {personaje.nombre} --------------------------------")
            print(f"Energía actual: {personaje.energia}")

            (opc_menu, energia) = Menu._input_eleccion_menu_comando("\nIngrese la opción de menú seguido de la energía que quiere agregar o quitar. Ejemplo: [1 2]\n1. Agregar energía\n2. Quitar energía\n0. Atrás\n: ",
                                                         "Para seleccionar una opción del menú ingrese un número entre el 1 y el 2.",
                                                         [0, 1, 2])
            if opc_menu == 0:
                break
            elif opc_menu == 1:
                personaje.agregar_energia(energia)
                break
            elif opc_menu == 2:
                personaje.gastar_energia(energia)
                break

    @staticmethod
    def _menu_ascender(personaje):
        """Abre el menú para ascender un personaje."""
        while True:
            eleccion = Menu._input_eleccion_menu(f"\n¿ESTÁS SEGURO de que quieres ascender a {personaje.nombre}? Esta decisión no se puede deshacer.\n1. Estoy seguro\n2. No\n: ",
                                                "\nDebes ingresar una opción de las que se muestran en el menú.")

            if eleccion == 2:
                break
            elif eleccion == 1:
                personaje.ascender()

    @staticmethod
    def _menu_modificadores(personaje):
        """Abre el menú que acompaña al usuario a aplicar distintos modificadores a alguna de sus cualidades."""
        while True:
            eleccion = Menu._input_eleccion_menu("\nElija una de las siguientes cualidades para agregar un bonificador o perjuicio.\n1. Vida\n2. Aguante\n3. Recuperación\n4. Iniciativa\n5. Resitencia luz\n6. Resitencia oscuridad\n7. Resistencia elemental\n8. Escudo sobrenatural\n0. Atrás\n: ",
                                                "Debes ingresar una opción de las que se muestran en el menú.", [0, 1, 2, 3, 4, 5, 6, 7, 8])

            if eleccion == 0:
                break
            elif eleccion == 1:
                Menu._menu_mod_cualidades(personaje, "modificador_vida")
            elif eleccion == 2:
                Menu._menu_mod_cualidades(personaje, "modificador_aguante")
            elif eleccion == 3:
                Menu._menu_mod_cualidades(personaje, "modificador_recuperacion")
            elif eleccion == 4:
                Menu._menu_mod_cualidades(personaje, "modificador_iniciativa")
            elif eleccion == 5:
                Menu._menu_mod_cualidades(personaje, "modificador_luz")
            elif eleccion == 6:
                Menu._menu_mod_cualidades(personaje, "modificador_oscuridad")
            elif eleccion == 7:
                Menu._menu_mod_cualidades(personaje, "modificador_elemental")
            elif eleccion == 8:
                Menu._menu_mod_cualidades(personaje, "modificador_escudo_sobrenatural")

    @staticmethod
    def _menu_mod_cualidades(personaje, nombre_metodo):
        while True:
            (opc_menu, valor) = Menu._input_eleccion_menu_comando("\nElija si sumar o restar seguido del valor que sumar o restar. Ejemplo [2 3]\n1. Sumar\n2. Restar\n0. Atrás\n: ",
                                                         "Formato inválido. Debes ingresar <Opción de menú> <Valor a sumar o restar>",
                                                         [0, 1, 2])

            if opc_menu == 0:
                break
            elif opc_menu == 1 or opc_menu == 2:
                metodo = getattr(personaje, nombre_metodo, None) # Llama al método pasado por argumento
                if not metodo:
                    print(f"Error: el método '{nombre_metodo}' no existe en el objeto personaje.")
                    return

                metodo(opc_menu, valor)
                break

    # @staticmethod
    # def _menu_administrar_equipo():
    #     """Abre el menú para administrar armas, armaduras y escudos."""
    #     while True:
    #         print("\n-------------------------------- Administrar equipo --------------------------------")
    #         eleccion = Menu._input_eleccion_menu("\n1. Armas\n2. Armaduras\n3. Escudos\n0. Atrás\n: ",
    #                                             "Seleccione una de las opciones del menú.", [0, 1, 2, 3])

    #         if eleccion == 0:
    #             break
    #         elif eleccion == 1:
    #             Menu._menu_administrar_armas()
    #         elif eleccion == 2:
    #             Menu._menu_administrar_armaduras()
    #         elif eleccion == 3:
    #             Menu._menu_administrar_escudos()

    # @staticmethod
    # def _menu_administrar_armas():
    #     """Abre el menú para agregar o eliminar armas."""
    #     armas = Arma.leer_datos_armas()

    #     while True:
    #         print("\n-------------------------------- Administrar armas --------------------------------")
    #         Menu._mostrar_armas()

    #         eleccion = input("\nPara eliminar un arma ingrese <Opción de menú> <ID de arma>. Ejemplo [2 38]\n1. Agregar arma\n2. Eliminar arma\n0. Atrás\n: ")
    #         print("")

    #         if len(eleccion) > 1:
    #             entrada = eleccion.strip().split()
    #             if len(entrada) != 2:
    #                 print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de arma>")
    #             else:
    #                 try:
    #                     opc_menu = int(entrada[0])
    #                     id = int(entrada[1])

    #                     if opc_menu != 2:
    #                         print("\nPara eliminar un arma debes ingresar <Opción de menú> <ID de arma>. Ejemplo [2 38]")
    #                     elif opc_menu == 2:
    #                         Arma.eliminar_arma(id)
    #                 except ValueError:
    #                     print("\nPor favor, ingresa solo números válidos.")
    #         else:
    #             try:
    #                 eleccion = int(eleccion)

    #                 if eleccion == 0:
    #                     break
    #                 elif eleccion != 1:
    #                     print("\nPara agregar un arma elija la opción 1 del menú.")
    #                 elif eleccion == 1:
    #                     Menu.menu_agregar_arma(armas)
    #             except ValueError:
    #                 print("\nPor favor, ingresa solo números válidos.")

    # @staticmethod
    # def _menu_administrar_armaduras():
    #     """Abre el menú para agregar o eliminar armaduras."""
    #     armaduras = Armadura.leer_datos_armaduras()

    #     while True:
    #         print("\n-------------------------------- Administrar armaduras --------------------------------")
    #         Menu._mostrar_armaduras()

    #         eleccion = input("\nPara eliminar una armadura ingrese <Opción de menú> <ID de armadura>. Ejemplo [2 38]\n1. Agregar armadura\n2. Eliminar armadura\n0. Atrás\n: ")
    #         print("")

    #         if len(eleccion) > 1:
    #             entrada = eleccion.strip().split()
    #             if len(entrada) != 2:
    #                 print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de armadura>")
    #             else:
    #                 try:
    #                     opc_menu = int(entrada[0])
    #                     id = int(entrada[1])

    #                     if opc_menu != 2:
    #                         print("\nPara eliminar una armadura debes ingresar <Opción de menú> <ID de armadura>. Ejemplo [2 38]")
    #                     elif opc_menu == 2:
    #                         Armadura.eliminar_armadura(id)
    #                 except ValueError:
    #                     print("\nPor favor, ingresa solo números válidos.")
    #         else:
    #             try:
    #                 eleccion = int(eleccion)

    #                 if eleccion == 0:
    #                     break
    #                 elif eleccion != 1:
    #                     print("\nPara agregar una armadura elija la opción 1 del menú.")
    #                 elif eleccion == 1:
    #                     Menu.menu_agregar_armadura(armaduras)
    #             except ValueError:
    #                 print("\nPor favor, ingresa solo números válidos.")

    # @staticmethod
    # def _menu_administrar_escudos():
    #     """Abre el menú para agregar o eliminar escudos."""
    #     escudos = Escudo.leer_datos_escudos()

    #     while True:
    #         print("\n-------------------------------- Administrar escudos --------------------------------")
    #         Menu._mostrar_escudos()

    #         eleccion = input("\nPara eliminar un escudo ingrese <Opción de menú> <ID de escudo>. Ejemplo [2 38]\n1. Agregar escudo\n2. Eliminar escudo\n0. Atrás\n: ")
    #         print("")

    #         if len(eleccion) > 1:
    #             entrada = eleccion.strip().split()
    #             if len(entrada) != 2:
    #                 print("\nFormato inválido. Debes escribir una opción del menú o <Opción de menú> <ID de escudo>")
    #             else:
    #                 try:
    #                     opc_menu = int(entrada[0])
    #                     id = int(entrada[1])

    #                     if opc_menu != 2:
    #                         print("\nPara eliminar un escudo debes ingresar <Opción de menú> <ID de escudo>. Ejemplo [2 38]")
    #                     elif opc_menu == 2:
    #                         Escudo.eliminar_escudo(id)
    #                 except ValueError:
    #                     print("\nPor favor, ingresa solo números válidos.")
    #         else:
    #             try:
    #                 eleccion = int(eleccion)

    #                 if eleccion == 0:
    #                     break
    #                 elif eleccion != 1:
    #                     print("\nPara agregar un escudo elija la opción 1 del menú.")
    #                 elif eleccion == 1:
    #                     Menu.menu_agregar_escudo(escudos)
    #             except ValueError:
    #                 print("\nPor favor, ingresa solo números válidos.")

    # @staticmethod
    # def _mostrar_armas():
    #     """Muestra todas las armas guardadas."""
    #     armas = Arma.json_a_arma()
    #     equipo_max_len = Equipo._equipo_max_longitud()

    #     if armas:
    #         print("\nArmas guardadas:")
    #         for arma in armas:
    #             espacios_id = ""
    #             espacios_nom = ""
    #             espacios_dano = ""
    #             espacios_tipo_dano = ""
    #             espacios_peso = ""
    #             espacios_tipo_arma = ""
    #             if arma.id < 10:
    #                 espacios_id += " "
    #             for i in range(Menu._num_dif_palabras(arma.nombre, equipo_max_len)):
    #                 espacios_nom += " "
    #             for i in range(Menu._num_dif_palabras(arma.tipo_dano, "Contundente")):
    #                 espacios_tipo_dano += " "
    #             if arma.dano < 10:
    #                 espacios_dano += " "
    #             if len(str(arma.peso)) == 1:
    #                 espacios_peso += "   "
    #             elif len(str(arma.peso)) == 3:
    #                 espacios_peso += " "
    #             for i in range(Menu._num_dif_palabras(arma.tipo_arma, "Proyectiles")):
    #                 espacios_tipo_arma += " "
    #             print(f"{arma.id}.{espacios_id} {arma.nombre} {espacios_nom}| Impacto {arma.impacto} | Daño {arma.dano}{espacios_dano} | {arma.tipo_dano}{espacios_tipo_dano} | Estructura {arma.estructura} | Peso {arma.peso}{espacios_peso} | Alcance {arma.alcance} | Tipo arma '{arma.tipo_arma}'{espacios_tipo_arma}")

    # @staticmethod
    # def _mostrar_armaduras():
    #     """Muestra todas las armaduras guardadas."""
    #     armaduras = Armadura.json_a_armadura()
    #     equipo_max_len = Equipo._equipo_max_longitud()

    #     if armaduras:
    #         print("\nArmaduras:")
    #         for armadura in armaduras:
    #             espacios_id = ""
    #             espacios_nom = ""
    #             espacios_est = ""
    #             espacios_peso = ""
    #             if armadura.id < 10:
    #                 espacios_id += " "
    #             if armadura.estructura < 10:
    #                 espacios_est += " "
    #             if armadura.peso < 10:
    #                 espacios_peso += " "
    #             for i in range(Menu._num_dif_palabras(armadura.nombre, equipo_max_len)):
    #                 espacios_nom += " "
    #             print(f"{armadura.id}.{espacios_id} {armadura.nombre} {espacios_nom}| Contundente {armadura.contundente} | Cortante {armadura.cortante} | Perforante {armadura.perforante} | Cobertura {armadura.cobertura} | Evasion {armadura.evasion} | Estructura {armadura.estructura}{espacios_est} | Peso {armadura.peso}{espacios_peso} | Penalizador {armadura.penalizador}")

    # @staticmethod
    # def _mostrar_escudos():
    #     """Muestra todos los escudos guardados."""
    #     escudos = Escudo.json_a_escudo()
    #     equipo_max_len = Equipo._equipo_max_longitud()

    #     if escudos:
    #         print("\nEscudos:")
    #         for escudo in escudos:
    #             espacios_id = ""
    #             espacios_nom = ""
    #             espacios_peso = ""
    #             for i in range(Menu._num_dif_palabras(escudo.nombre, equipo_max_len)):
    #                 espacios_nom += " "
    #             if escudo.id < 10:
    #                 espacios_id += " "
    #             if len(str(escudo.peso)) < 2:
    #                 espacios_peso += "  "
    #             print(f"{escudo.id}.{espacios_id} {escudo.nombre} {espacios_nom}| Contundente {escudo.contundente} | Cortante {escudo.cortante} | Perforante {escudo.perforante} | Cobertura {escudo.cobertura} | Evasion {escudo.evasion} | Estructura {escudo.estructura} | Peso {escudo.peso}{espacios_peso} | Penalizador {escudo.penalizador}")

    # @staticmethod
    # def menu_agregar_arma(armas):
    #     """Abre el menú para agregar un arma."""
    #     nombre = Menu._asignar_nombre_equipo()
    #     if nombre is None:
    #         return

    #     impacto = Menu._asignar_num("Impacto: ")
    #     if impacto is None:
    #         return

    #     dano = Menu._asignar_num("Daño: ")
    #     if dano is None:
    #         return

    #     alcance = Menu._asignar_num("Alcance: ")
    #     if alcance is None:
    #         return

    #     tipo_dano = Menu._asignar_texto_personalizado("Los tipos de daño pueden ser 'Contundente', 'Cortante' o 'Perforante'.\nTipo de daño: ", ["Contundente", "Cortante", "Perforante"])
    #     if tipo_dano is None:
    #         return

    #     tipo_arma = Menu._asignar_texto_personalizado("Los tipos de arma pueden ser 'Espada', 'Maza', 'Mangual', 'Lanza', 'Alabarda', 'Pico', 'Hacha' o 'Proyectiles'.\nTipo de arma: ", ["Espada", "Maza", "Mangual", "Lanza", "Alabarda", "Pico", "Hacha", "Proyectiles"])
    #     if tipo_arma is None:
    #         return

    #     estructura = Menu._asignar_num("Estructura: ")
    #     if estructura is None:
    #         return

    #     peso = Menu._asignar_num("Peso: ")
    #     if peso is None:
    #         return

    #     arma = Arma(nombre, estructura, peso, impacto, dano, alcance, tipo_dano, tipo_arma)
    #     arma.guardar_armas(armas)

    # @staticmethod
    # def menu_agregar_armadura(armaduras):
    #     """Abre el menú para agregar una armadura."""
    #     nombre = Menu._asignar_nombre_equipo()
    #     if nombre is None:
    #         return

    #     contundente = Menu._asignar_num("Contundente: ")
    #     if contundente is None:
    #         return

    #     cortante = Menu._asignar_num("Cortante: ")
    #     if cortante is None:
    #         return

    #     perforante = Menu._asignar_num("Perforante: ")
    #     if perforante is None:
    #         return

    #     cobertura = Menu._asignar_num("Cobertura: ")
    #     if cobertura is None:
    #         return

    #     evasion = Menu._asignar_num("Evasión: ")
    #     if evasion is None:
    #         return

    #     penalizador = Menu._asignar_num("Penalizador: ")
    #     if penalizador is None:
    #         return

    #     estructura = Menu._asignar_num("Estructura: ")
    #     if estructura is None:
    #         return

    #     peso = Menu._asignar_num("Peso: ")
    #     if peso is None:
    #         return

    #     armadura = Armadura(nombre, estructura, peso, contundente, cortante, perforante, cobertura, evasion, penalizador)
    #     armadura.guardar_armaduras(armaduras)

    # @staticmethod
    # def menu_agregar_escudo(escudos):
    #     """Abre el menú para agregar un escudo."""
    #     nombre = Menu._asignar_nombre_equipo()
    #     if nombre is None:
    #         return

    #     contundente = Menu._asignar_num("Contundente: ")
    #     if contundente is None:
    #         return

    #     cortante = Menu._asignar_num("Cortante: ")
    #     if cortante is None:
    #         return

    #     perforante = Menu._asignar_num("Perforante: ")
    #     if perforante is None:
    #         return

    #     cobertura = Menu._asignar_num("Cobertura: ")
    #     if cobertura is None:
    #         return

    #     evasion = Menu._asignar_num("Evasión: ")
    #     if evasion is None:
    #         return

    #     penalizador = Menu._asignar_num("Penalizador: ")
    #     if penalizador is None:
    #         return

    #     estructura = Menu._asignar_num("Estructura: ")
    #     if estructura is None:
    #         return

    #     peso = Menu._asignar_num("Peso: ")
    #     if peso is None:
    #         return

    #     escudo = Escudo(nombre, estructura, peso, contundente, cortante, perforante, cobertura, evasion, penalizador)
    #     escudo.guardar_escudos(escudos)

    # @staticmethod
    # def _asignar_nombre_equipo():
    #     """El usuario asigna el nombre del equipo."""
    #     while True:
    #         print("\nIngrese 'q' para salir.")
    #         nombre = input("Nombre del equipo: ")

    #         if nombre.lower() == "q":
    #             return False

    #         if len(nombre) > 0:
    #             return nombre
    #         else:
    #             print("El nombre del equipo no puede estar vacío.")

    # @staticmethod
    # def _asignar_num(texto):
    #     """El usuario ingresa un número."""
    #     while True:
    #         print("\nIngrese 'q' para salir.")
    #         num = input(texto)

    #         if num.lower() == 'q':
    #             return False

    #         try:
    #             return int(num)
    #         except ValueError:
    #             print("\nIngrese un número válido.")

    # @staticmethod
    # def _asignar_texto_personalizado(texto, lista_opciones):
    #     """El usuario asigna un texto que debe estar entre unas opciones personalizadas."""
    #     while True:
    #         print("\nIngrese 'q' para salir.")
    #         tipo_personalizado = input(texto)

    #         if tipo_personalizado.lower() == "q":
    #             return False

    #         if tipo_personalizado.title() in lista_opciones:
    #             return tipo_personalizado.title()
    #         else:
    #             print(f"\nEl texto debe coincidir con alguno de los siguientes:\n{lista_opciones}")

    @staticmethod
    def _input_eleccion_menu(texto, texto_error, lista_opciones):
        """Método genérico para plantear un menú al usuario con opciones."""
        while True:
            try:
                eleccion = int(input(texto))
                if eleccion in lista_opciones:
                    return eleccion
                else:
                    print(texto_error)
            except ValueError:
                print(texto_error)

    @staticmethod
    def _input_eleccion_menu_comando(texto, texto_error, lista_opciones_menu):
        """Método genérico para plantear un menú al usuario con opciones para crear un comando."""
        while True:
            try:
                eleccion = input(texto).strip().split()

                if int(eleccion[0]) == 0:
                    return (0, 0)

                if len(eleccion) != 2:
                    print("\nFormato inválido. Debes escribir: <número 1> <número 2>")
                else:
                    try:
                        opc_menu = int(eleccion[0])
                        comando = int(eleccion[1])

                        if opc_menu in lista_opciones_menu:
                            return (opc_menu, comando)
                    except ValueError:
                        print("\nPor favor, ingresa solo números válidos.")
            except ValueError:
                print(texto_error)

    @staticmethod
    def _num_dif_palabras(p1, p2):
        """Devuele el número de diferencia de caracteres entre dos palabras pasadas por parámetros."""
        if len(p1) > len(p2):
            return len(p1) - len(p2)
        elif len(p2) > len(p1):
            return len(p2) - len(p1)
        else:
            return 0