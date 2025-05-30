from __future__ import annotations
from .vehiculos import Vehiculos



class Helicoptero(Vehiculos):
    """
    Representa un helicóptero utilizado para el transporte de órganos.
    """


    def __init__(self, velocidad: float):

        """
        Inicializa un helicóptero con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia: float, trafico: float | None = None) -> float:

        """
        Calcula el tiempo de viaje. El tráfico no afecta al helicóptero.

        Params:
            distancia (float): Distancia en km.
            trafico (float, optional): (Ignorado)

        Returns:
            float: Tiempo estimado de viaje en horas.
        """
        tiempo = distancia / self.velocidad
        return tiempo



