from vehiculos.vehiculos import Vehiculos


class Helicoptero(Vehiculos):
    def __init__(self, velocidad):
        super().__init__(velocidad)
        self.velocidad = velocidad

    def calcular_tiempo(self, distancia, trafico = None):

        tiempo = distancia / self.velocidad # No se ve afectado por el trafico
        return tiempo


