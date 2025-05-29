from datetime import datetime
from pacientes.donantes import Donante
from pacientes.receptor import Receptor


class Organo:
    """
    Representa un órgano humano potencialmente disponible para trasplante.
    """
    TIPOS_VALIDOS = ["corazon", "higado", "riñones", "pulmones", "pancreas", "piel", "huesos", "intestino", "corneas"]

    def __init__(self, tipo_org: str):
        """
        Inicializa un órgano con su tipo.

        Params:
            tipo_org (str): Tipo de órgano. Debe estar en TIPOS_VALIDOS.

        Raises:
            ValueError: Si el tipo no es válido.
        """
        if tipo_org not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de órgano inválido: {tipo_org}. Los tipos válidos son: {self.TIPOS_VALIDOS}")
        self.tipo_org = tipo_org
        self.fecha_hora_ablacion = None # Se asigna cuando se realice la ablacion

    def asignar_fecha_hora_ablacion(self, fecha_hora: datetime) -> None:
        """
        Asigna la fecha y hora en que fue realizada la ablación.

        Params:
            fecha_hora (datetime): Fecha y hora de ablación.

        Effects:
            Cambia el estado interno del órgano.
        """
        self.fecha_hora_ablacion = fecha_hora

    def __str__(self) -> str:
        """
        Retorna una cadena con el tipo de órgano y su estado de ablación.

        Returns:
            str: Representación legible en texto.
        """
        if self.fecha_hora_ablacion:
            ablacion_info = self.fecha_hora_ablacion.strftime('%Y-%m-%d %H:%M') # Cadena de texto de deletime
        else:
            ablacion_info = "No ablacionado"
        return f"{self.tipo_org} (Ablación: {ablacion_info})"


    def es_compatible(self, receptor: 'Receptor', donante: 'Donante') -> bool:

        """
        Determina si el órgano es compatible entre un donante y un receptor.

        Params:
            receptor (Receptor): Objeto receptor.
            donante (Donante): Objeto donante.

        Returns:
            bool: True si hay compatibilidad, False si no.
        """
        if self.tipo_org != receptor.organo_necesario:
            return False

        # Lógica de compatibilidad ABO
        donante_tipo = donante.tipo_sangre
        receptor_tipo = receptor.tipo_sangre

        if donante_tipo == receptor_tipo:
            return True
        elif donante_tipo == 'O':
            return True
        elif receptor_tipo == 'AB':
            return True
        elif donante_tipo == 'A' and receptor_tipo == 'AB':
            return True
        elif donante_tipo == 'B' and receptor_tipo == 'AB':
            return True
        else:
            return False

    def esta_disponible(self) -> bool: # Para saber si el órgano ya ha sido ablacionado.
        """
        Indica si el órgano aún no fue ablacionado.

        Returns:
            bool: True si está disponible, False si ya fue ablacionado.
        """ 
        return self.fecha_hora_ablacion is None
    
    def __repr__(self) -> str:
        """
        Representación técnica del órgano, indicando su estado.

        Returns:
            str: Cadena tipo Organo(tipo:..., estado:...)
        """
        if self.fecha_hora_ablacion:
            ablacion_estado = "Ablacionado"
        else:
            ablacion_estado = "Pendiente"
        return f"Organo(tipo:{self.tipo_org}, estado: {ablacion_estado}"

    def __bool__(self) -> bool:
        """
        Permite usar el órgano como valor booleano.

        Returns:
            bool: True si fue ablacionado, False si no.
        """
    # Un órgano listo para trasplante si ha sido ablacionado.
        return self.fecha_hora_ablacion is not None








