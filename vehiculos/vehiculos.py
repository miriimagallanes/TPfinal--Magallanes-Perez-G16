from abc import ABC , abstractmethod
from typing import Optional



class Vehiculos(ABC):
    """
    Clase abstracta que representa un vehículo usado para transportar órganos.

    Contiene información sobre velocidad, disponibilidad y viajes realizados.
    """

    
    def __init__(self, velocidad: float):
        """
        Inicializa un vehículo con una velocidad dada.

        Params:
            velocidad (float): Velocidad del vehículo (km/h). Debe ser mayor a 0.

        Precondiciones:
            velocidad > 0

        Effects:
            Inicializa el estado del vehículo y su disponibilidad.
        """
        if velocidad <= 0:
            raise ValueError("La velocidad del vehiculo debe ser un valor positivo")
        self.velocidad = velocidad
        self.viajes_realizados = []
        self.disponible = True

    @abstractmethod
    def calcular_tiempo(self, distancia: float, trafico: Optional[float] = None) -> float:
        """
        Calcula el tiempo estimado de viaje según el tipo de vehículo.

        Params:
            distancia (float): Distancia total del viaje en kilómetros.
            trafico (float, optional): Tiempo extra en horas debido al tráfico.

        Returns:
            float: Tiempo estimado de viaje en horas.
        """
        pass 

    def registrar_viaje(self, distancia: float, trafico: Optional[float], tiempo_estimado: float) -> None:
        """
        Registra un viaje realizado por el vehículo.

        Params:
            distancia (float): Distancia recorrida.
            trafico (float): Condición de tráfico durante el viaje.
            tiempo_estimado (float): Tiempo que tomó el viaje.

        Effects:
            Agrega un nuevo registro al historial de viajes.
        """
        self.viajes_realizados.append({
            "distancia": distancia,
            "trafico": trafico,
            "tiempo_estimado": tiempo_estimado
        })

    def mostrar_viajes(self) -> None:
        """
        Imprime en consola todos los viajes realizados por el vehículo.

        Effects:
            Muestra los viajes por pantalla.
        """
        for viaje in self.viajes_realizados:
            print(viaje)

    def marcar_no_disponible(self) -> None:
        """
        Marca al vehículo como no disponible.

        Effects:
            Cambia el estado interno a no disponible.
        """
        self.disponible = False

    def marcar_disponible(self) -> None:
        """
        Marca al vehículo como disponible.

        Effects:
            Cambia el estado interno a disponible.
        """
        self.disponible = True












