class Color:
    """Clase diseñada para colorear texto en la consola"""

    FIN = "\033[0m"
    NEGRITA = "\033[1m"
    SUBRRAYADO = "\033[4m"

    NEGRO = "\033[38;2;0;0;0m"
    ROJO = "\033[38;2;255;0;0m"
    VERDE = "\033[38;2;0;255;0m"
    AMARILLO = "\033[38;2;255;255;0m"
    AZUL = "\033[34m"
    VIOLETA = "\033[38;2;200;0;200m"
    CELESTE = "\033[38;2;73;216;230m"
    GRIS = "\033[38;2;120;120;120m"
    GRIS_CLARO = "\033[38;2;220;220;220m"
    NARANJA = "\033[38;2;255;100;0m"
    NARANJA_CLARO = "\033[38;2;255;172;66m"
    MARRON = "\033[38;2;143;103;0m"

    FONDO_MARRON = "\033[48;2;143;103;0m"
    FONDO_CELESTE = "\033[48;2;73;216;230m"