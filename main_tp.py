from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from organos import Organo
from vehiculos.vehiculo_terrestre import Vehiculo_terrestre
from vehiculos.helicoptero import Helicoptero
from vehiculos.avion import Avion
from cirujanos import Cirujano
from centro_salud import Centro_Salud
from incucai import INCUCAI
from datetime import datetime



def main():

     # 1. Crear centros de salud con coordenadas
    centro_salud_donante = Centro_Salud("Hospital Donante", "Dir 1", "Partido A", "Provincia X", "111", -34.6037, -58.3816) # Ejemplo: Buenos Aires
    centro_salud_receptor = Centro_Salud("Hospital Receptor", "Dir 2", "Partido B", "Provincia Y", "222", -33.0000, -60.0000) # Ejemplo: Otra ubicación

    # 2. Crear vehículos y asignarlos a centros
    vehiculo_terrestre_1 = Vehiculo_terrestre(60)
    helicoptero_1 = Helicoptero(200)
    avion_1 = Avion(800)
    centro_salud_receptor.agregar_vehiculo(vehiculo_terrestre_1)
    centro_salud_receptor.agregar_vehiculo(helicoptero_1)
    centro_salud_receptor.agregar_vehiculo(avion_1)

    # 3. Crear cirujanos y asignarlos a centros
    cirujano_1 = Cirujano("Dr. López", ["cardiovascular"])
    cirujano_2 = Cirujano("Dra. Pérez", ["gastroenterólogo"])
    cirujano_general_1 = Cirujano("Dr. García")
    centro_salud_receptor.agregar_cirujano(cirujano_1)
    centro_salud_receptor.agregar_cirujano(cirujano_2)
    centro_salud_receptor.agregar_cirujano(cirujano_general_1)

    # 4. Crear donante
    donante_1 = Donante("Juan", 12345678, datetime(1980, 5, 15), "M", "123", "A+", centro_salud_donante,
                datetime(2025, 5, 18), datetime(2, 0, 0), datetime(2025, 5, 18), datetime(3, 0, 0),
                ["corazón", "riñón"]) # Donante específico de corazón y riñón

    # 5. Crear receptor
    receptor_1 = Receptor("María", 87654321, datetime(1975, 10, 20), "F", "456", "A+", centro_salud_receptor,
                "corazón", datetime(2025, 4, 1))

    # 6. Crear instancia de INCUCAI
    incucai_sistema = INCUCAI()

    # 7. Registrar centros, donante y receptor
    incucai_sistema.registrar_centro_salud(centro_salud_donante)
    incucai_sistema.registrar_centro_salud(centro_salud_receptor)
    incucai_sistema.registrar_paciente(donante_1)
    incucai_sistema.registrar_paciente(receptor_1)

    # 8. Buscar coincidencias
    coincidencias = incucai_sistema.buscar_match_donante(donante_1)
    if coincidencias:
        print("\nCoincidencias encontradas:")
        for organo, receptor_match in coincidencias:
            print(f"Órgano: {organo}, Receptor: {receptor_match.nombre}")
    # 9. Iniciar protocolo de trasplante para la primera coincidencia
        incucai_sistema.iniciar_protocolo(donante_1, receptor_match, organo)
    else:
        print("\nNo se encontraron coincidencias.")

    # 10. Actualizar listas de espera
    incucai_sistema.actualizar_listas() 

            

   

# Llamamos a la función principal para ejecutar el código

if __name__ == "__main__":
    main()