from vehiculos.vehiculos import Vehiculos



class Helicoptero(Vehiculos):
    """
    Representa un helicóptero utilizado para el transporte de órganos.
    """


    def __init__(self, velocidad):
        """
        Inicializa un helicóptero con velocidad dada.
        """
        super().__init__(velocidad)

    def calcular_tiempo(self, distancia, trafico):
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



