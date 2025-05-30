from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from vehiculos.vehiculo_terrestre import Vehiculo_terrestre
from vehiculos.avion import Avion
from vehiculos.helicoptero import Helicoptero
from centro_salud import Centro_Salud
from incucai import INCUCAI
from cirujanos import Cirujano
from datetime import datetime, timedelta
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
    print("10. Realizar ablación de un órgano")
    print("0. Salir")

def registrar_donante(sistema, centro):
    try:
        nombre = input("Nombre: ")
        dni = int(input("DNI: "))
        fecha_nac = datetime.strptime(input("Fecha de nacimiento (YYYY-MM-DD): "), "%Y-%m-%d")
        sexo = input("Sexo: ")
        telefono = input("Teléfono: ")
        tipo_sangre = input("Tipo de sangre: ")

        fallecido = input("¿El donante ya ha fallecido? (s/n): ").lower()

        if fallecido == "s":
            fecha_falle = datetime.strptime(input("Fecha de fallecimiento (YYYY-MM-DD): "), "%Y-%m-%d")
            hora_falle = datetime.strptime(input("Hora de fallecimiento (HH:MM): "), "%H:%M")
            fecha_abl = datetime.strptime(input("Fecha de ablación (YYYY-MM-DD): "), "%Y-%m-%d")
            hora_abl = datetime.strptime(input("Hora de ablación (HH:MM): "), "%H:%M")
        else:
            fecha_falle = None
            hora_falle = None
            fecha_abl = None
            hora_abl = None

        organos = input("Órganos a donar (separados por coma): ").split(",")
        organos = [o.strip() for o in organos]

        donante = Donante(nombre, dni, fecha_nac, sexo, telefono, tipo_sangre, centro,
                          fecha_falle, hora_falle, fecha_abl, hora_abl, organos)

        sistema.registrar_paciente(donante)

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
    centro_donante = Centro_Salud("Hospital CABA", "Av. Cordoba 3456", "CABA", "CABA", "111", -34.6037, -58.3816)
    centro_receptor = Centro_Salud("Hospital General Belgrano", "Av. de los Incas 1234", "San Martín", "Buenos Aires", "222", -34.5705, -58.5296)
    centro_donante_1 = Centro_Salud("Hospital San Isidro", "Av. Centenario 123", "San Isidro", "Buenos Aires", "011-1111", latitud=-34.472, longitud=-58.523)
    centro_donante_2 = Centro_Salud("Hospital Rosario", "Bv. Oroño 456", "Rosario", "Santa Fe", "0341-2222", latitud=-32.9442, longitud=-60.6505)
    centro_receptor_1 = Centro_Salud("Hospital Mendoza", "Av. San Martín 789", "Capital", "Mendoza", "0261-3333", latitud=-32.8908, longitud=-68.8272)
    centro_receptor_2 = Centro_Salud("Hospital La Plata", "Calle 12 321", "La Plata", "Buenos Aires", "0221-4444", latitud=-34.9214, longitud=-57.9544)


    centro_receptor.agregar_vehiculo(Vehiculo_terrestre(60))
    centro_receptor.agregar_vehiculo(Helicoptero(200))
    centro_receptor.agregar_vehiculo(Avion(800))

    centro_receptor.agregar_cirujano(Cirujano("Dr. López", ["cardiovascular"], "MP19002" ))
    centro_receptor.agregar_cirujano(Cirujano("Dra. Pérez", ["gastroenterólogo"],"MP1234"))
    centro_receptor.agregar_cirujano(Cirujano("Dr. García",["cardiovascular"], "MP1034"))
    centro_donante_1.agregar_cirujano( Cirujano("Dr. Laura Respira",["pulmonar"],"MP1001"))         
    centro_donante_2.agregar_cirujano(Cirujano("Dr. Ernesto Dermis",["plástico"],"MP1002"))    
    centro_receptor_1.agregar_cirujano(Cirujano("Dra. Carla Huesos",["traumatólogo"],"MP1003"))        
    centro_receptor_2.agregar_cirujano(Cirujano("Dr. Pablo General", [],"MP0000"))         


    sistema = INCUCAI()

    print()
    sistema.registrar_centro_salud(centro_donante)
    sistema.registrar_centro_salud(centro_receptor)
    sistema.registrar_centro_salud(centro_donante_1)
    sistema.registrar_centro_salud(centro_donante_2)
    sistema.registrar_centro_salud(centro_receptor_1)
    sistema.registrar_centro_salud(centro_receptor_2)
    print()

    donante_demo = Donante(
        nombre="Juan Romero", dni=123, fecha_nacimiento=datetime(1980, 1, 1),
        sexo="M", telefono="111", tipo_sangre="A+",
        centro_salud_asociado=centro_donante,
        fecha_fallecimiento=datetime(2025, 5, 20),
        hora_fallecimiento=datetime(2025, 5, 20, 2, 0),
        fecha_inicio_ablacion=datetime(2025, 5, 20),
        hora_inicio_ablacion=datetime(2025, 5, 20, 3, 0),
        organos_a_donar_str=["corazon", "higado"]
    )

    donante_demo_1 = Donante(
        nombre="Miriam Gómez", dni=124, fecha_nacimiento=datetime(1975, 3, 10),
        sexo="F", telefono="222", tipo_sangre="B+",
        centro_salud_asociado=centro_donante_1,
        fecha_fallecimiento=datetime(2025, 5, 21),
        hora_fallecimiento=datetime(2025, 5, 21, 4, 30),
        fecha_inicio_ablacion=datetime(2025, 5, 21),
        hora_inicio_ablacion=datetime(2025, 5, 21, 6, 0),
        organos_a_donar_str=["pulmones", "riñones"]
    )
    
    donante_demo_2 = Donante(
        nombre="Carlos Pérez", dni=125, fecha_nacimiento=datetime(1965, 7, 15),
        sexo="M", telefono="333", tipo_sangre="O-",
        centro_salud_asociado=centro_donante_2,
        fecha_fallecimiento=datetime(2025, 5, 22),
        hora_fallecimiento=datetime(2025, 5, 22, 1, 0),
        fecha_inicio_ablacion=datetime(2025, 5, 22),
        hora_inicio_ablacion=datetime(2025, 5, 22, 2, 30),
        organos_a_donar_str=["pancreas", "piel"]
    )

    receptor_demo = Receptor(
        nombre="Ana Perla", dni=456, fecha_nacimiento=datetime(1990, 1, 1),
        sexo="F", telefono="222", tipo_sangre="A+",
        centro_salud_asociado=centro_receptor,
        organo_necesario="corazon", fecha_ingreso_lista=datetime(2025, 5, 1)
    )

    receptor_demo_1 = Receptor(
        nombre="María López", dni=457, fecha_nacimiento=datetime(1985, 6, 20),
        sexo="F", telefono="444", tipo_sangre="B+",
        centro_salud_asociado=centro_receptor_1,
        organo_necesario="rinon", fecha_ingreso_lista=datetime(2025, 4, 15)
    )

    receptor_demo_2 = Receptor(
        nombre="José Martínez", dni=458, fecha_nacimiento=datetime(2000, 9, 5),
        sexo="M", telefono="555", tipo_sangre="O-",
        centro_salud_asociado=centro_receptor_2,
        organo_necesario="higado", fecha_ingreso_lista=datetime(2025, 4, 20)
    )

    sistema.registrar_paciente(donante_demo)
    sistema.registrar_paciente(donante_demo_1)
    sistema.registrar_paciente(donante_demo_2)
    print()
    sistema.registrar_paciente(receptor_demo)
    sistema.registrar_paciente(receptor_demo_1)
    sistema.registrar_paciente(receptor_demo_2)
    print()

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

        # En el archivo del menú interactivo (por ejemplo main_tp.py)
# Agregar esta opción dentro del bucle principal del menú:

        elif opcion == "10":
            try:
                dni = int(input("DNI del donante para realizar ablación: "))
                donante = next(d for d in sistema.donantes if d.get_dni() == dni)

                # Mostrar órganos disponibles (no ablacionados)
                disponibles = [o for o in donante.organos_a_donar if o.fecha_hora_ablacion is None]
                if not disponibles:
                    print("Este donante no tiene órganos disponibles para ablación.")
                else:
                    print("\nÓrganos disponibles para ablación:")
                    for idx, o in enumerate(disponibles):
                        print(f"{idx+1}. {o.tipo_org}")

                    opcion_organo = int(input("Seleccione el número del órgano a ablacionar: "))
                    organo_elegido = disponibles[opcion_organo - 1]

                    centro = donante.centro_salud_asociado
                    if centro:
                        centro.realizar_ablacion(donante, organo_elegido)
                        # Si ya no quedan órganos ablacionables ni ablacionados, se elimina el donante
                        if not donante.organos_a_donar:
                            sistema.donantes.remove(donante)
                            print(f"Donante {donante.nombre} eliminado de la lista: sin órganos restantes.")
                    else:
                        print("El donante no tiene un centro de salud asociado.")

            except StopIteration:
                print("Donante no encontrado.")
            except (ValueError, IndexError):
                print("Entrada inválida. Selección cancelada.")



        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        
        
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
