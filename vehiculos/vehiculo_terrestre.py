from vehiculos.vehiculos import Vehiculos
from typing import Optional


class Vehiculo_terrestre(Vehiculos):
    """
    Representa un vehículo terrestre como una ambulancia.
    """
    def __init__(self, velocidad: float):
        """
        Inicializa un vehículo terrestre con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia: float, trafico: Optional[float]) -> float:
        """
        Calcula el tiempo total de viaje considerando el tráfico.

        Params:
            distancia (float): Distancia en km.
            trafico (float): Tiempo extra en horas debido al tráfico.

        Returns:
            float: Tiempo total estimado en horas.
        """
        tiempo = distancia / self.velocidad + trafico # Tiempo de viaje # t=100km/(50km/h) + 1h = 2hs +1h = 3hs
        return tiempo
    








 

