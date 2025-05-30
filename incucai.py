from __future__ import annotations
from datetime import datetime, timedelta
from typing import Optional, Any, TYPE_CHECKING

from excepciones import PacienteNoEncontradoError, CentroSaludNoEncontradoError, RecursosInsuficientesError, RecursoNoDisponibleError, PacienteYaRegistradoError

# Solo para verificación de tipo, no para ejecución

from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from centrosalud import CentroSalud
from organos import Organo
from vehiculos.vehiculos import Vehiculos
from cirujanos import Cirujano



class INCUCAI:
    """
    Clase que representa el sistema nacional de coordinación de trasplantes.

    Administra registros de donantes, receptores y centros de salud, y coordina los procesos de ablación y trasplante.
    """


    def __init__(self):
        """
        Inicializa el sistema con listas vacías de donantes, receptores, centros de salud y trasplantes realizados.
        """
        self.donantes: list[Donante] = []
        self.receptores: list[Receptor] = []
        self.centros_salud: list[CentroSalud] = []
        self.trasplantes_realizados: list[dict] = []

    
    def registrar_paciente(self, paciente: 'Donante' | 'Receptor') -> None:
        """
        Registra un paciente en el sistema (donante o receptor).

        Params:
            paciente: Objeto Donante o Receptor.

        Effects:
            Agrega el paciente a la lista correspondiente si no estaba registrado.
        """
        dni_nuevo = paciente.get_dni() 

        for d in self.donantes:

            if d.get_dni() == dni_nuevo:
                raise PacienteYaRegistradoError(f"Error: El DNI {dni_nuevo} ya está registrado como donante.")

        for r in self.receptores:

            if r.get_dni() == dni_nuevo:
                raise PacienteYaRegistradoError(f"Error: El DNI {dni_nuevo} ya está registrado como receptor.")

        if isinstance(paciente, Donante):
            self.donantes.append(paciente)
            print(f"Donante {paciente.nombre} (DNI: {dni_nuevo}) registrado con éxito.")

        elif isinstance(paciente, Receptor):
            self.receptores.append(paciente)
            print(f"Receptor {paciente.nombre} (DNI: {dni_nuevo}) registrado con éxito.")

        else:
            print("Tipo de paciente no reconocido y no puede ser registrado.")

    def registrar_centro_salud(self, centro: 'CentroSalud') -> None:
        """
        Registra un nuevo centro de salud.

        Params:
            centro: Objeto Centro_Salud.

        Effects:
            Agrega el centro a la lista si no estaba registrado.
        """
        if centro not in self.centros_salud:
            self.centros_salud.append(centro)
            print(f"Centro de salud {centro.nombre} registrado en el sistema.")

        else:
            print(f"El centro de salud {centro.nombre} ya está registrado.")

    def buscar_match_donante(self, donante: 'Donante') -> list[tuple['Organo', 'Receptor']]:
        """
        Busca receptores compatibles para cada órgano del donante.

        Params:
            donante: Objeto Donante.

        Returns:
            list: Lista de tuplas (órgano, receptor) compatibles.
        """
        coincidencias = []
        for organo_donado in donante.organos_ablacionados:

            for receptor in self.receptores:

                if organo_donado.es_compatible(receptor, donante): 
                    coincidencias.append((organo_donado, receptor))

        return coincidencias

    def buscar_match_receptor(self, receptor: 'Receptor') -> list[tuple['Donante', 'Organo']]:
        """
        Busca donantes compatibles con el receptor dado.

        Params:
            receptor: Objeto Receptor.

        Returns:
            list: Lista de tuplas (donante, órgano) compatibles.
        """
        coincidencias = []
        for donante in self.donantes:

            for organo_donado in donante.organos_a_donar:

                if organo_donado.es_compatible(receptor, donante): 
                    coincidencias.append((donante, organo_donado))

            for organo_extraido in donante.organos_ablacionados:

                if organo_extraido.es_compatible(receptor, donante):
                    coincidencias.append((donante, organo_extraido))
                                
        return coincidencias

    def iniciar_protocolo(self, donante: 'Donante', receptor: 'Receptor', organo: 'Organo') -> None:
        """
        Ejecuta el protocolo básico de trasplante.

        Params:
            donante: Donante involucrado.
            receptor: Receptor involucrado.
            organo: Órgano a trasplantar.

        Effects:
            Registra el resultado y modifica listas si el trasplante es exitoso.
        """

        print(f"Iniciando protocolo de trasplante de {organo.tipo_org} del donante {donante.nombre} al receptor {receptor.nombre}.")
        
        if not self.centros_salud:
             raise CentroSaludNoEncontradoError("No hay centros de salud registrados en el sistema INCUCAI")

        centro_receptor = receptor.centro_salud_asociado

        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado")

        try:
            vehiculo, cirujano = self.asignar_recursos(receptor, organo, donante.centro_salud_asociado)
        except RecursosInsuficientesError as e:
            print(f"No se pudo iniciar el protocolo por falta de recursos: {e}")
            return
        
        organo_extraido = centro_receptor.realizar_ablacion(donante, organo)
        if not organo_extraido:
            return
        exito = centro_receptor.realizar_trasplante(receptor, organo_extraido, cirujano)
        self.registrar_resultado_trasplante(receptor, organo_extraido, exito)

        if exito:
            self.receptores.remove(receptor)
            print(f"Receptor {receptor.nombre} removido de la lista después de un trasplante exitoso.")
   
    def actualizar_listas(self) -> None:
        """
        Recorre los receptores y aumenta su prioridad si llevan más de 30 días en la lista.

        Effects:
            Puede aumentar el valor de prioridad de los receptores.
        """
        print("\nActualizando listas de espera...")
        for receptor in self.receptores:
            tiempo_en_lista = datetime.now() - receptor.fecha_ingreso_lista

            if tiempo_en_lista > timedelta(days=30) and receptor.prioridad < 5:
                receptor.prioridad += 1
                print(f"Prioridad del receptor {receptor.nombre} (DNI: {receptor.get_dni()}) aumentada a {receptor.prioridad} después de {tiempo_en_lista.days} días en espera.")
        print("Listas de espera actualizadas.")

    def listar_pacientes(self, tipo: str) -> None:
        """
        Lista todos los pacientes registrados según el tipo dado.

        Params:
            tipo (str): "donante" o "receptor".

        Effects:
            Imprime por pantalla los pacientes correspondientes.
        """

        if tipo.lower() == "donante":
            for donante in self.donantes:
                print(donante)

        elif tipo.lower() == "receptor":
            for receptor in self.receptores:
                print(receptor)

        else:
            print("Tipo de paciente no válido.")

    def buscar_por_centro(self, nombre_centro: str) -> None:
        """
        Muestra los pacientes asociados a un centro de salud por nombre.

        Params:
            nombre_centro (str): Nombre textual del centro.

        Effects:
            Imprime la información encontrada o lanza una excepción.

        Raises:
            CentroSaludNoEncontradoError: Si no se encuentra el centro.
        """
        for centro in self.centros_salud:

            if centro.nombre.lower() == nombre_centro.lower():
                print(f"Información del Centro de Salud: {centro.nombre}")
                donantes_en_centro = [d for d in self.donantes if d.centro_salud_asociado == centro]
                receptores_en_centro = [r for r in self.receptores if r.centro_salud_asociado == centro]
                print(f"  Donantes asociados: {[d.nombre for d in donantes_en_centro]}")
                print(f"  Receptores asociados: {[r.nombre for r in receptores_en_centro]}")
                return
        raise CentroSaludNoEncontradoError(f"No se encontro ningun centro de salud con el nombre {nombre_centro}.")

    def buscar_prioridad_receptor(self, dni: int) -> None:
        """
        Busca la prioridad del receptor a partir de su DNI.

        Params:
            dni (str): Documento del paciente.

        Effects:
            Imprime la prioridad si lo encuentra.

        Raises:
            PacienteNoEncontradoError: Si no está en el sistema.
        """
        for receptor in self.receptores:
         
         if receptor.get_dni() == dni:
            print(f"Receptor: {receptor.nombre}")
            print(f"Prioridad: {receptor.prioridad}")
            print(f"Estado: {receptor.estado}")
            return
        raise PacienteNoEncontradoError(f"No se encontró ningún receptor con el DNI {dni}")

    def asignar_recursos(self, receptor: 'Receptor', organo: 'Organo', centro_donante: 'CentroSalud') -> tuple['Vehiculos', 'Cirujano']:
        """
        Asigna un vehículo y un cirujano al receptor desde su centro de salud asociado.

        Params:
            receptor: Objeto Receptor.
            organo: Objeto Organo.
            centro_donante: Centro_Salud del donante.

        Returns:
            tuple: (vehiculo, cirujano)

        Raises:
            RecursosInsuficientesError: Si no hay disponibilidad de recursos.
        """

        centro_receptor = receptor.centro_salud_asociado
        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado para la asignacion de recursos.")
        
        try:
            vehiculo_asignado = centro_receptor.seleccionar_vehiculo_para_traslado(centro_donante) 
        except RecursoNoDisponibleError as e:
            raise RecursosInsuficientesError(f"Fallo al asignar vehiculo: {e}"
                                             
            ) from e 
        try:
            cirujano_asignado = centro_receptor.seleccionar_cirujano_para_operacion(organo.tipo_org)
        except RecursoNoDisponibleError as e: 

            if vehiculo_asignado and not vehiculo_asignado.disponible:
                vehiculo_asignado.marcar_disponible()
                print(f"El vehículo ({type(vehiculo_asignado).__name__}) fue liberado debido a un error en la asignación del cirujano.")
            raise RecursosInsuficientesError(f"Error al asignar cirujano: {e}" 
            ) from e      

        print(f"Recursos asignados para el trasplante al receptor {receptor.nombre}:")
        print(f"Vehículo: {type(vehiculo_asignado).__name__}")
        print(f"Cirujano: {cirujano_asignado.nombre}")

        return vehiculo_asignado, cirujano_asignado

    def realizar_proceso_trasplante(self, donante: 'Donante', receptor: 'Receptor', organo_a_donar: 'Organo') -> None:
        """
        Ejecuta el proceso completo de ablación y trasplante con control de tiempo.

        Params:
            donante: Objeto Donante.
            receptor: Objeto Receptor.
            organo_a_donar: Objeto Organo.

        Effects:
            Asigna recursos, realiza ablación, calcula viabilidad y trasplanta si es posible.
            Libera recursos si el trasplante no es viable.
        """
        print(f"\nIniciando proceso de trasplante de {organo_a_donar.tipo_org} del donante {donante.nombre} al receptor {receptor.nombre}.")

        centro_donante = donante.centro_salud_asociado
        centro_receptor = receptor.centro_salud_asociado

        if not centro_donante:
            raise CentroSaludNoEncontradoError(f"El donante {donante.nombre} no tiene un centro de salud asociado.")
        
        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado.")
        
        if organo_a_donar.fecha_hora_ablacion is None:
            print(f"El órgano {organo_a_donar.tipo_org} aún no ha sido ablacionado. No se puede continuar con el trasplante.")
            return

        vehiculo_asignado = None
        cirujano_asignado = None

        try:
            vehiculo_asignado, cirujano_asignado = self.asignar_recursos(receptor, organo_a_donar, centro_donante)
        except RecursosInsuficientesError as e:
            print(f"No se pudo completar el proceso de trasnplante or falta de recursos: {e}")
            return

        distancia_km = centro_receptor.obtener_distancia(centro_donante)

        if distancia_km is None:
            print(f"Error: No se pudieron calcular las coordenadas de distancia entre el centro del donante ({centro_donante.nombre}) y el centro del receptor ({centro_receptor.nombre}). Proceso de trasplante abortado.")

            if vehiculo_asignado:
                vehiculo_asignado.marcar_disponible()
                print(f"El vehículo ({type(vehiculo_asignado).__name__}) se marca como disponible nuevamente.")

            if cirujano_asignado and not cirujano_asignado.esta_disponible(): 
                cirujano_asignado.resetear_disponibilidad()
                print(f"El cirujano ({cirujano_asignado.nombre}) se marca como disponible nuevamente.")
            return 

        tiempo_en_horas = vehiculo_asignado.calcular_tiempo(distancia_km)
        tiempo_de_viaje = timedelta(hours=tiempo_en_horas)
        print(f"Tiempo de viaje estimado: {tiempo_de_viaje}.")
        momento_llegada = organo_a_donar.fecha_hora_ablacion + tiempo_de_viaje

        vehiculo_asignado.registrar_viaje(distancia=distancia_km, trafico = None, tiempo_estimado=tiempo_de_viaje)

        tiempo_transcurrido_maximo = timedelta(hours=20)
        tiempo_hasta_llegada = momento_llegada - organo_a_donar.fecha_hora_ablacion


        if tiempo_hasta_llegada <= tiempo_transcurrido_maximo:
            print(f"El órgano llegará en {tiempo_hasta_llegada}, dentro del límite de viabilidad.")
            exito = centro_receptor.realizar_trasplante(receptor, organo_a_donar, cirujano_asignado)
            self.registrar_resultado_trasplante(receptor, organo_a_donar, exito)

            if exito:
                self.receptores.remove(receptor)
                print(f"Receptor {receptor.nombre} removido de la lista después del trasplante.")

            if not donante.organos_a_donar:  
                self.donantes.remove(donante)
                print(f"Donante {donante.nombre} eliminado del sistema. Ya no tiene más órganos disponibles.")

            vehiculo_asignado.marcar_disponible()
            print(f"El vehículo ({type(vehiculo_asignado).__name__}) ha llegado al centro receptor y está disponible nuevamente.")

        else:
            print(f"El tiempo estimado de llegada ({tiempo_hasta_llegada}) excede el límite de viabilidad del órgano ({tiempo_transcurrido_maximo}).Proceso del transplante abortado")
            vehiculo_asignado.marcar_disponible()

            print(f"El vehículo ({type(vehiculo_asignado).__name__}) se marca como disponible debido a la inviabilidad del órgano.")

            if cirujano_asignado and cirujano_asignado.esta_disponible() == False:
                 cirujano_asignado.resetear_disponibilidad()

                 print(f"El cirujano ({cirujano_asignado.nombre}) se marca como disponible nuevamente.")

    def registrar_resultado_trasplante(self, receptor: 'Receptor', organo: 'Organo', exito: bool) -> None:
        """
        Registra el resultado de un trasplante en el historial.

        Params:
            receptor: Objeto Receptor.
            organo: Objeto Organo.
            exito (bool): Indica si el trasplante fue exitoso.

        Effects:
            Agrega un diccionario con los datos del trasplante a la lista de resultados.
        """
        resultado = {
            "receptor": receptor.nombre,
            "dni": receptor.get_dni(),
            "organo": organo.tipo_org,
            "fecha": datetime.now(),
            "exito": exito
        }
        self.trasplantes_realizados.append(resultado)

        if exito:
            print(f"\n✔ Trasplante registrado exitosamente.")

        else:
            print(f"\n✘ Se registró un trasplante fallido.")
       

    

          


