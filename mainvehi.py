from vehiculo_terrestre import Vehiculo_terrestre
from helicoptero import Helicoptero
from avion import Avion

def main():

# ------ VEHICULOS(V.TERRESTRES, HELICOPTERO, AVION) ------ #


    # Crear instancias de los vehículos
    ambulancia = Vehiculo_terrestre(velocidad=60)     # km/h
    heli = Helicoptero(velocidad=200)                 # km/h
    avion = Avion(velocidad=800)                      # km/h

    # Parámetros del viaje
    distancia = 300  # km
    trafico = 1.5    # horas de demora por tráfico

    # Vehículo terrestre
    tiempo_amb = ambulancia.calcular_tiempo(distancia, trafico)
    ambulancia.registrar_viaje(distancia, trafico, tiempo_amb)
    print(f"Ambulancia tardará {tiempo_amb:.2f} horas.")

    # Helicóptero
    tiempo_heli = heli.calcular_tiempo(distancia)
    heli.registrar_viaje(distancia, None, tiempo_heli)
    print(f"Helicóptero tardará {tiempo_heli:.2f} horas.")

    # Avión
    tiempo_avion = avion.calcular_tiempo(distancia)
    avion.registrar_viaje(distancia, None, tiempo_avion)
    print(f"Avión tardará {tiempo_avion:.2f} horas.")

    print("\nResumen de viajes realizados:")
    print("Ambulancia:")
    ambulancia.mostrar_viajes()

    print("Helicóptero:")
    heli.mostrar_viajes()

    print("Avión:")
    avion.mostrar_viajes()















if __name__ == "__main__":
    main()



