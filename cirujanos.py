import random

class Cirujano:
    def __init__(self, nombre, especialidades=None, matricula=None):
        self.nombre = nombre
        self.especialidades = especialidades if especialidades is not None else []
        self.operaciones_realizadas = []
        self.matricula = matricula
        self.disponible = True

    def tiene_especialidad(self, especialidad):
        return especialidad in self.especialidades

    def esta_disponible(self):
        return self.disponible

    def marcar_como_no_disponible(self):
        self.disponible = False

    def realizar_operacion(self, organo):
        self.operaciones_realizadas.append(organo)
        self.marcar_como_no_disponible()
        exito = self._determinar_exito(organo)
        print(f"El cirujano {self.nombre} ha realizado una operación de {organo}. Éxito: {exito}.")
        return exito

    def _determinar_exito(self, organo):
        especialidades_por_organo = {
            "corazón": "cardiovascular",
            "pulmon": "pulmonar",
            "piel": "plástico",
            "córneas": "plástico",
            "huesos": "traumatólogo",
            "intestino": "gastroenterólogo",
            "riñón": "gastroenterólogo",
            "hígado": "gastroenterólogo",
            "páncreas": "gastroenterólogo"
        }
        especialidad_requerida = especialidades_por_organo.get(organo)

        if not self.especialidades: # Cirujano general
            return random.randint(1, 10) > 5
        else: # Cirujano con especialidad
            if especialidad_requerida in self.especialidades:
                return random.randint(1, 10) >= 3
            else: # No tiene la especialidad requerida, se considera como general
                return random.randint(1, 10) > 5

    def resetear_disponibilidad(self):
        self.disponible = True







