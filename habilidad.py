class Habilidad:
    """Representa una habilidad de un personaje."""

    def __init__(self, nombre, atributos_relacionados, tipo):
        """Inicializa los atributos de una habilidad."""
        self.nombre = nombre
        self.nivel = 0
        self.atributos_relacionados = atributos_relacionados
        self.xp = 0
        self.xp_max_req = None # Experiencia requerida para subir de nivel la habilidad
        self.tipo = tipo
    
    def set_atributos(self, nivel, xp, xp_max_req):
        """Asigna todos los valores pasados por argumentos a la habilidad."""
        self.nivel = nivel
        self.xp = xp
        self.xp_max_req = xp_max_req

    def convertir_a_diccionario(self):
        """Convierte una habilidad en diccionario."""
        return {
            "Nombre": self.nombre,
            "Nivel": self.nivel,
            "Atributos relacionados": self.atributos_relacionados,
            "XP": self.xp,
            "XP requerida": self.xp_max_req,
            "Tipo": self.tipo
            }