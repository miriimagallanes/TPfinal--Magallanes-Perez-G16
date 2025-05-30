from __future__ import annotations
from .vehiculos import Vehiculos



class VehiculoTerrestre(Vehiculos):
    """
    Representa un vehículo terrestre como una ambulancia.
    """


    def __init__(self, velocidad: float):

        """
        Inicializa un vehículo terrestre con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia: float, trafico: float) -> float:

        """
        Calcula el tiempo total de viaje considerando el tráfico.

        Params:
            distancia (float): Distancia en km.
            trafico (float): Tiempo extra en horas debido al tráfico.

        Returns:
            float: Tiempo total estimado en horas.
        """
        tiempo = distancia / self.velocidad + trafico 
        return tiempo


