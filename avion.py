from vehiculos import Vehiculos


class Avion(Vehiculos):
    def __init__(self, velocidad):
        super().__init__(velocidad)
        self.velocidad = velocidad 

    def calcular_tiempo(self, distancia, trafico = None):

        tiempo = distancia / self.velocidad 
        return tiempo 
    
    




