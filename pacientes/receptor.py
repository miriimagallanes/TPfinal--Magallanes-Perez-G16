import random
from pacientes.pacientes import Pacientes
from datetime import datetime
from typing import Optional
from centro_salud import Centro_Salud


class Receptor(Pacientes):
    """
    Representa a un paciente receptor que espera un órgano compatible.

    """
    def __init__(self, nombre: str, dni: int, fecha_nacimiento: datetime, sexo: str,
                 telefono: str, tipo_sangre: str, centro_salud_asociado: 'Centro_Salud',
                 organo_necesario: str, fecha_ingreso_lista: datetime,
                 prioridad: Optional[int] = None, estado: str = "estable"):
        """
        Inicializa un receptor con órgano requerido y prioridad (puede ser aleatoria).

        Params:
            organo_necesario (str): Órgano requerido por el receptor.
            fecha_ingreso_lista (datetime): Fecha en que fue añadido a la lista de espera.
            prioridad (int, optional): Nivel de urgencia (1 a 5).
            estado (str): Estado actual del paciente.
        """
        super().__init__(nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado)
        self.organo_necesario = organo_necesario
        self.fecha_ingreso_lista = fecha_ingreso_lista
        self.estado = estado
        self.prioridad = prioridad if prioridad is not None else self._generar_prioridad_aleatoria()
        self.patologia = None # Podemos agregar patología si es necesario

    def mostrar_estado(self) -> None:
        """
        Imprime el estado actual y la prioridad del receptor.

        Effects:
            Muestra información por consola.
        """
        print(f"Estado del receptor {self.nombre}: {self.estado}")
        print(f"Prioridad de {self.nombre}: {self.prioridad}")

    def _generar_prioridad_aleatoria(self) -> int:
        """
        Genera una prioridad aleatoria entre 1 y 5.

        Returns:
            int: Prioridad generada como entero.
        """
        return random.randint(1, 5)

    def trasplante_fallido(self) -> None:
        """
        Actualiza la prioridad y estado tras un trasplante fallido.

        Effects:
            La prioridad se establece en 5 y el estado en "Inestable".
        """
        self.prioridad = 5 # Se setea a la mayor prioridad (según enunciado)
        self.estado = "Inestable"
        print(f"Trasplante fallido para el receptor {self.nombre}. Prioridad ahora es {self.prioridad}, estado Inestable.")

    def renovar_estado(self, nuevo_estado: str) -> None:
        """
        Cambia el estado del receptor si su prioridad es mayor a 3.

        Params:
            nuevo_estado (str): Nuevo estado a establecer (no se usa directamente).

        Effects:
            Cambia el estado a "inestable" si la prioridad es mayor a 3.
        """
        if self.prioridad > 3:
            self.estado = "inestable"

    # Podemos agregar un método para establecer la patología si es necesario
    def establecer_patologia(self, patologia: str) -> None:
        """
        Establece la patología del paciente receptor.

        Params:
            patologia (str): Descripción de la patología del receptor.

        Effects:
            Asigna la patología al receptor.
        """
        self.patologia = patologia


  


