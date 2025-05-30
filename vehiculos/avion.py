from __future__ import annotations
from .vehiculos import Vehiculos



class Avion(Vehiculos):
    """
    Representa un avión utilizado en el sistema de traslado de órganos.
    """

    
    def __init__(self, velocidad: float):
        
        """
        Inicializa un avión con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia: float, trafico: float | None = None) -> float:

        """
        Calcula el tiempo de viaje, ignorando tráfico.

        Params:
            distancia (float): Distancia en km.
            trafico (float, optional): (Ignorado)

        Returns:
            float: Tiempo estimado de viaje en horas.
        """
        tiempo = distancia / self.velocidad 
        return tiempo 
    
    





