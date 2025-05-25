from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from vehiculos.vehiculo_terrestre import Vehiculo_terrestre
from vehiculos.avion import Avion
from vehiculos.helicoptero import Helicoptero
from centro_salud import Centro_Salud
from incucai import INCUCAI
from cirujanos import Cirujano
from datetime import datetime
from excepciones import *

def mostrar_menu():
    print("\n--- MENU INTERACTIVO INCUCAI ---")
    print("1. Ver lista de donantes")
    print("2. Ver lista de receptores")
    print("3. Buscar coincidencias para un donante")
    print("4. Iniciar protocolo de trasplante")
    print("5. Ver órganos restantes de un donante")
    print("6. Consultar prioridad de receptor por DNI")
    print("7. Buscar pacientes por centro de salud")
    print("8. Registrar nuevo donante")
    print("9. Registrar nuevo receptor")
    print("0. Salir")

def registrar_donante(sistema, centro):
    try:
        nombre = input("Nombre: ")
        dni = int(input("DNI: "))
        fecha_nac = datetime.strptime(input("Fecha de nacimiento (YYYY-MM-DD): "), "%Y-%m-%d")
        sexo = input("Sexo: ")
        telefono = input("Teléfono: ")
        tipo_sangre = input("Tipo de sangre: ")
        fecha_falle = datetime.strptime(input("Fecha de fallecimiento (YYYY-MM-DD): "), "%Y-%m-%d")
        hora_falle = datetime.strptime(input("Hora de fallecimiento (HH:MM): "), "%H:%M")
        fecha_abl = datetime.strptime(input("Fecha de ablación (YYYY-MM-DD): "), "%Y-%m-%d")
        hora_abl = datetime.strptime(input("Hora de ablación (HH:MM): "), "%H:%M")
        organos = input("Órganos a donar (separados por coma): ").split(",")
        organos = [o.strip() for o in organos]
        d = Donante(nombre, dni, fecha_nac, sexo, telefono, tipo_sangre, centro,
                   fecha_falle, hora_falle, fecha_abl, hora_abl, organos)
        sistema.registrar_paciente(d)
    except Exception as e:
        print(f"Error al registrar donante: {e}")

def registrar_receptor(sistema, centro):
    try:
        nombre = input("Nombre: ")
        dni = int(input("DNI: "))
        fecha_nac = datetime.strptime(input("Fecha de nacimiento (YYYY-MM-DD): "), "%Y-%m-%d")
        sexo = input("Sexo: ")
        telefono = input("Teléfono: ")
        tipo_sangre = input("Tipo de sangre: ")
        organo = input("Órgano que necesita: ")
        fecha_lista = datetime.strptime(input("Fecha de ingreso a la lista (YYYY-MM-DD): "), "%Y-%m-%d")
        r = Receptor(nombre, dni, fecha_nac, sexo, telefono, tipo_sangre, centro,
                   organo, fecha_lista)
        sistema.registrar_paciente(r)
    except Exception as e:
        print(f"Error al registrar receptor: {e}")

def main():
    centro_donante = Centro_Salud("Hospital Donante", "Calle 1", "Partido A", "Provincia X", "111", -34.60, -58.38)
    centro_receptor = Centro_Salud("Hospital Receptor", "Calle 2", "Partido B", "Provincia Y", "222", -33.0, -60.0)

    centro_receptor.agregar_vehiculo(Vehiculo_terrestre(60))
    centro_receptor.agregar_vehiculo(Helicoptero(200))
    centro_receptor.agregar_vehiculo(Avion(800))

    centro_receptor.agregar_cirujano(Cirujano("Dr. López", ["cardiovascular"]))
    centro_receptor.agregar_cirujano(Cirujano("Dra. Pérez", ["gastroenterólogo"]))
    centro_receptor.agregar_cirujano(Cirujano("Dr. García"))

    sistema = INCUCAI()

    sistema.registrar_centro_salud(centro_donante)
    sistema.registrar_centro_salud(centro_receptor)

    # Crear pacientes por defecto
    donante_demo = Donante(
        nombre="Juan Demo", dni=123, fecha_nacimiento=datetime(1980, 1, 1),
        sexo="M", telefono="111", tipo_sangre="A+",
        centro_salud_asociado=centro_donante,
        fecha_fallecimiento=datetime(2025, 5, 20),
        hora_fallecimiento=datetime(2025, 5, 20, 2, 0),
        fecha_inicio_ablacion=datetime(2025, 5, 20),
        hora_inicio_ablacion=datetime(2025, 5, 20, 3, 0),
        organos_a_donar_str=["corazón", "hígado"]
    )

    receptor_demo = Receptor(
        nombre="Ana Demo", dni=456, fecha_nacimiento=datetime(1990, 1, 1),
        sexo="F", telefono="222", tipo_sangre="A+",
        centro_salud_asociado=centro_receptor,
        organo_necesario="corazón", fecha_ingreso_lista=datetime(2025, 5, 1)
    )

    sistema.registrar_paciente(donante_demo)
    sistema.registrar_paciente(receptor_demo)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            sistema.listar_pacientes("donante")
        elif opcion == "2":
            sistema.listar_pacientes("receptor")
        elif opcion == "3":
            for d in sistema.donantes:
                print(f"\nDonante: {d.nombre} - DNI: {d.get_dni()}")
                coincidencias = sistema.buscar_match_donante(d)
                for o, r in coincidencias:
                    print(f"- Órgano: {o.tipo_org}, Receptor: {r.nombre}")
        elif opcion == "4":
            try:
                dni = int(input("DNI del donante: "))
                donante = next(d for d in sistema.donantes if d.get_dni() == dni)
                coincidencias = sistema.buscar_match_donante(donante)
                if coincidencias:
                    organo, receptor = coincidencias[0]
                    sistema.realizar_proceso_trasplante(donante, receptor, organo)
                else:
                    print("No hay coincidencias disponibles.")
            except StopIteration:
                print("Donante no encontrado.")
        elif opcion == "5":
            try:
                dni = int(input("DNI del donante: "))
                donante = next(d for d in sistema.donantes if d.get_dni() == dni)
                for o in donante.organos_a_donar:
                    print(f"- {o.tipo_org}")
            except StopIteration:
                print("Donante no encontrado.")
        elif opcion == "6":
            try:
                dni = int(input("Ingrese el DNI del receptor: "))
                sistema.buscar_prioridad_receptor(dni)
            except ValueError:
                print("DNI inválido.")
            except PacienteNoEncontradoError as e:
                print(e)
        elif opcion == "7":
            nombre = input("Ingrese el nombre del centro de salud: ")
            try:
                sistema.buscar_por_centro(nombre)
            except CentroSaludNoEncontradoError as e:
                print(e)
        elif opcion == "8":
            registrar_donante(sistema, centro_donante)
        elif opcion == "9":
            registrar_receptor(sistema, centro_receptor)
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
