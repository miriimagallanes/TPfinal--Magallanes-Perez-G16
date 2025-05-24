import random
from pacientes.pacientes import Pacientes


class Receptor(Pacientes):
    def __init__(self, nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado,
                 organo_necesario, fecha_ingreso_lista, prioridad=None, estado="estable"):
        super().__init__(nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado)
        self.organo_necesario = organo_necesario
        self.fecha_ingreso_lista = fecha_ingreso_lista
        self.estado = estado
        self.prioridad = prioridad if prioridad is not None else self._generar_prioridad_aleatoria()
        self.patologia = None # Podemos agregar patología si es necesario

    def mostrar_estado(self):
        print(f"Estado del receptor {self.nombre}: {self.estado}")
        print(f"Prioridad de {self.nombre}: {self.prioridad}")

    def _generar_prioridad_aleatoria(self):
        return random.randint(1, 5)

    def trasplante_fallido(self):
        self.prioridad = 1 # Se setea a la mayor prioridad (según enunciado)
        self.estado = "Inestable"
        print(f"Trasplante fallido para el receptor {self.nombre}. Prioridad ahora es {self.prioridad}, estado Inestable.")

    def renovar_estado(self, nuevo_estado):
        if self.prioridad > 3:
            self.estado = "inestable"

    # Podemos agregar un método para establecer la patología si es necesario
    def establecer_patologia(self, patologia):
        self.patologia = patologia


  


