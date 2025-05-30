import random



class Cirujano:
    """
    Representa un cirujano que puede realizar operaciones médicas.

    Tiene especialidades, historial de operaciones y estado de disponibilidad.
    """
    def __init__(self, nombre: str, especialidades: list = None, matricula: str = None):
        """
        Inicializa un cirujano.

        Params:
            nombre (str): Nombre completo.
            especialidades (list[str], optional): Lista de especialidades médicas.
            matricula (str, optional): Matrícula profesional.
        """
        self.nombre = nombre
        self.especialidades = especialidades if especialidades is not None else []
        self.operaciones_realizadas = []
        self.matricula = matricula
        self.disponible = True

    def tiene_especialidad(self, especialidad: str) -> bool:
        """
        Verifica si el cirujano posee una especialidad dada.

        Params:
            especialidad (str): Nombre de la especialidad.

        Returns:
            bool: True si posee la especialidad, False si no.
        """
        return especialidad in self.especialidades

    def esta_disponible(self) -> bool:
        """
        Verifica si el cirujano está disponible para operar.

        Returns:
            bool: True si está disponible, False si no.
        """
        return self.disponible

    def marcar_como_no_disponible(self) -> None:
        """
        Marca al cirujano como no disponible.

        Effects:
            Cambia su estado interno.
        """
        self.disponible = False

    def realizar_operacion(self, organo: str) -> bool:
        """
        Simula la realización de una operación sobre un órgano.

        Params:
            organo (str): Tipo de órgano operado.

        Returns:
            bool: True si fue exitosa, False si falló (según probabilidad).

        Effects:
            Registra la operación e impacta la disponibilidad.
        """
        self.operaciones_realizadas.append(organo)
        self.marcar_como_no_disponible()
        exito = self._determinar_exito(organo)
        print(f"El cirujano {self.nombre} ha realizado una operación de {organo}. Éxito: {exito}.")
        return exito

    def _determinar_exito(self, organo: str) -> bool:
        """
        Lógica para determinar el éxito de la operación.

        Params:
            organo (str): Tipo de órgano operado.

        Returns:
            bool: True si fue exitosa, False si falló.
        """

        especialidades_por_organo = {
            "corazon": "cardiovascular",
            "pulmon": "pulmonar",
            "piel": "plástico",
            "corneas": "plástico",
            "huesos": "traumatólogo",
            "intestino": "gastroenterólogo",
            "riñon": "gastroenterólogo",
            "hígado": "gastroenterólogo",
            "pancreas": "gastroenterólogo"
        }
        especialidad_requerida = especialidades_por_organo.get(organo)

        if not self.especialidades: # Cirujano general
            return random.randint(1, 10) > 5
        else: # Cirujano con especialidad
            if especialidad_requerida in self.especialidades:
                return random.randint(1, 10) >= 3
            else: # No tiene la especialidad requerida, se considera como general
                return random.randint(1, 10) > 5

    def resetear_disponibilidad(self) -> None:
        """
        Marca al cirujano como disponible nuevamente.

        Effects:
            Cambia el estado a disponible.
        """
        self.disponible = True







