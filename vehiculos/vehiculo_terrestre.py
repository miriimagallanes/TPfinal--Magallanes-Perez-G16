from vehiculos.vehiculos import Vehiculos



class Vehiculo_terrestre(Vehiculos):
    """
    Representa un vehículo terrestre como una ambulancia.
    """
    

    def __init__(self, velocidad):
        """
        Inicializa un vehículo terrestre con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia, trafico):
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
    








 

