from vehiculos import Vehiculos

class Vehiculo_terrestre(Vehiculos):
    def __init__(self, velocidad):
        super().__init__(velocidad)
        self.velocidad = velocidad 

    def calcular_tiempo(self, distancia, trafico):

        tiempo = distancia / self.velocidad + trafico # Tiempo de viaje # t=100km/(50km/h) + 1h = 2hs +1h = 3hs
        return tiempo
    







 

