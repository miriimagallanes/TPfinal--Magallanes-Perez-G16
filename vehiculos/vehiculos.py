from abc import ABC , abstractmethod

class Vehiculos(ABC):
    def __init__(self, velocidad):
        if velocidad <= 0:
            raise ValueError("La velocidad del vehiculo debe ser un valor positivo")
        self.velocidad = velocidad
        self.viajes_realizados = []
        self.disponible = True

    @abstractmethod
    def calcular_tiempo(self, distancia, trafico=None):
        pass 

    def registrar_viaje(self, distancia, trafico, tiempo_estimado):
        self.viajes_realizados.append({
            "distancia": distancia,
            "trafico": trafico,
            "tiempo_estimado": tiempo_estimado
        })

    def mostrar_viajes(self):
        for viaje in self.viajes_realizados:
            print(viaje)

    def marcar_no_disponible(self):
        self.disponible = False

    def marcar_disponible(self):
        self.disponible = True












