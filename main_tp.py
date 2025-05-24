
from pacientes.pacientes import Pacientes
from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from organos import Organo
from vehiculos.vehiculo_terrestre import Vehiculo_terrestre
from vehiculos.avion import Avion
from vehiculos.helicoptero import Helicoptero
from cirujanos import Cirujano
from centro_salud import Centro_Salud
from incucai import INCUCAI
from excepciones import RecursoNoDisponibleError, RecursosInsuficientesError, CentroSaludNoEncontradoError, PacienteNoEncontradoError
from datetime import datetime, timedelta

def main():
    # 1. Crear centros de salud con coordenadas
    centro_salud_donante = Centro_Salud("Hospital Donante", "Dir 1", "Partido A", "Provincia X", "111", -34.6037, -58.3816)
    centro_salud_receptor = Centro_Salud("Hospital Receptor", "Dir 2", "Partido B", "Provincia Y", "222", -33.0000, -60.0000)

    # 2. Crear vehículos y asignarlos al centro receptor
    centro_salud_receptor.agregar_vehiculo(Vehiculo_terrestre(60))
    centro_salud_receptor.agregar_vehiculo(Helicoptero(200))
    centro_salud_receptor.agregar_vehiculo(Avion(800))

    # 3. Crear cirujanos y asignarlos al centro receptor
    centro_salud_receptor.agregar_cirujano(Cirujano("Dr. López", ["cardiovascular"]))
    centro_salud_receptor.agregar_cirujano(Cirujano("Dra. Pérez", ["gastroenterólogo"]))
    centro_salud_receptor.agregar_cirujano(Cirujano("Dr. García"))  # General

    # 4. Crear donante
    donante_1 = Donante(
        nombre="Juan",
        dni=12345678,
        fecha_nacimiento=datetime(1980, 5, 15),
        sexo="M",
        telefono="123",
        tipo_sangre="A+",
        centro_salud_asociado=centro_salud_donante,
        fecha_fallecimiento=datetime(2025, 5, 18),
        hora_fallecimiento=datetime(2025, 5, 18, 2, 0),
        fecha_inicio_ablacion=datetime(2025, 5, 18),
        hora_inicio_ablacion=datetime(2025, 5, 18, 3, 0),
        organos_a_donar_str=["corazón", "riñón"]
    )

    # 5. Crear receptor
    receptor_1 = Receptor(
        nombre="María",
        dni=87654321,
        fecha_nacimiento=datetime(1975, 10, 20),
        sexo="F",
        telefono="456",
        tipo_sangre="A+",
        centro_salud_asociado=centro_salud_receptor,
        organo_necesario="corazón",
        fecha_ingreso_lista=datetime(2025, 4, 1)
    )

    # 6. Crear instancia de INCUCAI
    incucai_sistema = INCUCAI()
    incucai_sistema.registrar_centro_salud(centro_salud_donante)
    incucai_sistema.registrar_centro_salud(centro_salud_receptor)
    incucai_sistema.registrar_paciente(donante_1)
    incucai_sistema.registrar_paciente(receptor_1)

    # 7. Buscar coincidencias
    coincidencias = incucai_sistema.buscar_match_donante(donante_1)
    if coincidencias:
        print("\nCoincidencias encontradas:")
        for organo, receptor_match in coincidencias:
            print(f"\u25CF Órgano: {organo.tipo_org}, Receptor: {receptor_match.nombre}")
            incucai_sistema.realizar_proceso_trasplante(donante_1, receptor_match, organo)
    else:
        print("\nNo se encontraron coincidencias para este donante.")

    # 8. Actualizar listas
    incucai_sistema.actualizar_listas()

if __name__ == "__main__":
    main()
