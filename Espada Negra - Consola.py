from menu import Menu
from colorama import init


if __name__ == "__main__":
    init() # Para que funcionen los colores en Windows
    menu = Menu()

    while True:
        menu.menu_principal()