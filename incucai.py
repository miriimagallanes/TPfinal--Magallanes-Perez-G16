from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from datetime import datetime, timedelta
from excepciones import PacienteNoEncontradoError, CentroSaludNoEncontradoError, RecursosInsuficientesError, RecursoNoDisponibleError, PacienteYaRegistradoError

class INCUCAI:
    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.centros_salud = []
        self.trasplantes_realizados = []
    
    def registrar_paciente(self, paciente):
        dni_nuevo = paciente.get_dni() # Obtener el DNI del paciente a registrar

        # Verificar si el DNI ya existe en la lista de donantes
        for d in self.donantes:
            if d.get_dni() == dni_nuevo:
                raise PacienteYaRegistradoError(f"Error: El DNI {dni_nuevo} ya está registrado como donante.")

        # Verificar si el DNI ya existe en la lista de receptores
        for r in self.receptores:
            if r.get_dni() == dni_nuevo:
                raise PacienteYaRegistradoError(f"Error: El DNI {dni_nuevo} ya está registrado como receptor.")

        # Si el DNI es único, proceder con el registro
        if isinstance(paciente, Donante):
            self.donantes.append(paciente)
            print(f"Donante {paciente.nombre} (DNI: {dni_nuevo}) registrado con éxito.")
        elif isinstance(paciente, Receptor):
            self.receptores.append(paciente)
            print(f"Receptor {paciente.nombre} (DNI: {dni_nuevo}) registrado con éxito.")
        else:
            print("Tipo de paciente no reconocido y no puede ser registrado.")

    def registrar_centro_salud(self, centro):
        if centro not in self.centros_salud:
            self.centros_salud.append(centro)
            print(f"Centro de salud {centro.nombre} registrado en el sistema.")
        else:
            print(f"El centro de salud {centro.nombre} ya está registrado.")

    def buscar_match_donante(self, donante):
        coincidencias = []
        for organo_donado in donante.organos_a_donar:
            for receptor in self.receptores:
                if organo_donado.es_compatible(receptor, donante): # Pasamos el donante
                    coincidencias.append((organo_donado, receptor))
        return coincidencias

    def buscar_match_receptor(self, receptor):
        coincidencias = []
        for donante in self.donantes:
            for organo_donado in donante.organos_a_donar:
                if organo_donado.es_compatible(receptor, donante): # Metodo del objeto organo
                    coincidencias.append((donante, organo_donado))
        return coincidencias

    def iniciar_protocolo(self, donante, receptor, organo):
        print(f"Iniciando protocolo de trasplante de {organo.tipo_org} del donante {donante.nombre} al receptor {receptor.nombre}.")
        
        # 1. Seleccionar centro de salud 
        if not self.centros_salud:
             raise CentroSaludNoEncontradoError("No hay centros de salud registrados en el sistema INCUCAI")

        centro_receptor = receptor.centro_salud_asociado
        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado")

        # 2. Asignar vehículo y cirujano(llamamos a asignar_recursos que puede lanzar a RecursosInsuficientesError)
        try:
            vehiculo, cirujano = self.asignar_recursos(receptor, organo, donante.centro_salud_asociado)
        except RecursosInsuficientesError as e:
            print(f"No se pudo iniciar el protocolo por falta de recursos: {e}")
            return
        
        # 4. Realizar ablación (en el centro del donante - simplificado)
        organo_extraido = centro_receptor.realizar_ablacion(donante, organo)
        if not organo_extraido:
            return

        # 5. Realizar trasplante (en el centro del receptor)
        exito = centro_receptor.realizar_trasplante(receptor, organo_extraido, cirujano)
        self.registrar_resultado_trasplante(receptor, organo_extraido, exito)

        # 6. Actualizar listas (ej. remover receptor si el trasplante fue exitoso)
        if exito:
            self.receptores.remove(receptor)
            print(f"Receptor {receptor.nombre} removido de la lista después de un trasplante exitoso.")
   
    def actualizar_listas(self):
        print("\nActualizando listas de espera...")
        for receptor in self.receptores:
            tiempo_en_lista = datetime.now() - receptor.fecha_ingreso_lista
            # Ejemplo: Aumentar la prioridad si lleva más de 30 días en la lista
            if tiempo_en_lista > timedelta(days=30) and receptor.prioridad < 5:
                receptor.prioridad += 1
                print(f"Prioridad del receptor {receptor.nombre} (DNI: {receptor.get_dni()}) aumentada a {receptor.prioridad} después de {tiempo_en_lista.days} días en espera.")
        print("Listas de espera actualizadas.")

    def listar_pacientes(self, tipo):
        if tipo.lower() == "donante":
            for donante in self.donantes:
                print(donante)
        elif tipo.lower() == "receptor":
            for receptor in self.receptores:
                print(receptor)
        else:
            print("Tipo de paciente no válido.")

    def buscar_por_centro(self, nombre_centro):
        for centro in self.centros_salud:
            if centro.nombre.lower() == nombre_centro.lower():
                print(f"Información del Centro de Salud: {centro.nombre}")
                donantes_en_centro = [d for d in self.donantes if d.centro_salud_asociado == centro]
                receptores_en_centro = [r for r in self.receptores if r.centro_salud_asociado == centro]
                print(f"  Donantes asociados: {[d.nombre for d in donantes_en_centro]}")
                print(f"  Receptores asociados: {[r.nombre for r in receptores_en_centro]}")
                return
        raise CentroSaludNoEncontradoError(f"No se encontro ningun centro de salud con el nombre {nombre_centro}.")

    def buscar_prioridad_receptor(self, dni):
        for receptor in self.receptores:
         if receptor.get_dni() == dni:
            print(f"Receptor: {receptor.nombre}")
            print(f"Prioridad: {receptor.prioridad}")
            print(f"Estado: {receptor.estado}")
            return
        raise PacienteNoEncontradoError(f"No se encontró ningún receptor con el DNI {dni}")

    

    def asignar_recursos(self, receptor, organo, centro_donante):
        centro_receptor = receptor.centro_salud_asociado
        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado para la asignacion de recursos.")
        try:
            vehiculo_asignado = centro_receptor.seleccionar_vehiculo_para_traslado(centro_donante) 
        except RecursoNoDisponibleError as e:
            raise RecursosInsuficientesError(f"Fallo al asignar vehiculo: {e}"
            ) from e # Mejor depuracion, inf de ambas excepciones
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

    def realizar_proceso_trasplante(self, donante, receptor, organo_a_donar):
        print(f"\nIniciando proceso de trasplante de {organo_a_donar.tipo_org} del donante {donante.nombre} al receptor {receptor.nombre}.")

        centro_donante = donante.centro_salud_asociado
        centro_receptor = receptor.centro_salud_asociado

        #Compruebo que los centros esten asociados
        if not centro_donante:
            raise CentroSaludNoEncontradoError(f"El donante {donante.nombre} no tiene un centro de salud asociado.")
        if not centro_receptor:
            raise CentroSaludNoEncontradoError(f"El receptor {receptor.nombre} no tiene un centro de salud asociado.")

        # 0. Realizar ablación en el centro del donante
        organo_ablacionado = centro_donante.realizar_ablacion(donante, organo_a_donar)
        if not organo_ablacionado:
            print(f"Trasplante fallido, fallo la ablacion del organo {organo_a_donar.tipo_org}.")
            return

        # 1. Inicializar variables en 0 para asegurar que siempre existan
        vehiculo_asignado = None
        cirujano_asignado = None

        # 2. Asignar recursos (vehículo y cirujano) 
        try:
            vehiculo_asignado, cirujano_asignado = self.asignar_recursos(receptor, organo_ablacionado, centro_donante)
        except RecursosInsuficientesError as e:
            print(f"No se pudo completar el proceso de trasnplante or falta de recursos: {e}")
            return

        # 3. Calcular la distancia entre centros 
        distancia_km = centro_receptor.obtener_distancia(centro_donante)
        if distancia_km is None:
            print(f"Error: No se pudieron calcular las coordenadas de distancia entre el centro del donante ({centro_donante.nombre}) y el centro del receptor ({centro_receptor.nombre}). Proceso de trasplante abortado.")
            if vehiculo_asignado:
                vehiculo_asignado.marcar_disponible()
                print(f"El vehículo ({type(vehiculo_asignado).__name__}) se marca como disponible nuevamente.")
            if cirujano_asignado and not cirujano_asignado.esta_disponible(): # Pongo not para que este disponible
                cirujano_asignado.resetear_disponibilidad()
                print(f"El cirujano ({cirujano_asignado.nombre}) se marca como disponible nuevamente.")

            return 

        tiempo_en_horas = vehiculo_asignado.calcular_tiempo(distancia_km)
        tiempo_de_viaje = timedelta(hours=tiempo_en_horas)
        print(f"Tiempo de viaje estimado: {tiempo_de_viaje}.")
        momento_llegada = organo_ablacionado.fecha_hora_ablacion + tiempo_de_viaje

        vehiculo_asignado.registrar_viaje(distancia=distancia_km, trafico = None, tiempo_estimado=tiempo_de_viaje)

        # 5. Verificar viabilidad del órgano (20 horas desde la ablación)
        tiempo_transcurrido_maximo = timedelta(hours=20)
        tiempo_hasta_llegada = momento_llegada - organo_ablacionado.fecha_hora_ablacion

        if tiempo_hasta_llegada <= tiempo_transcurrido_maximo:
            print(f"El órgano llegará en {tiempo_hasta_llegada}, dentro del límite de viabilidad.")

            # 6. Realizar el trasplante en el centro del receptor
            exito = centro_receptor.realizar_trasplante(receptor, organo_ablacionado, cirujano_asignado)

            # 7. Registrar el resultado
            self.registrar_resultado_trasplante(receptor, organo_ablacionado, exito)

            # 8. Actualizar listas
            if exito:
                self.receptores.remove(receptor)
                print(f"Receptor {receptor.nombre} removido de la lista después del trasplante.")

            # 9. Liberar el vehículo después del traslado (al centro receptor)
            vehiculo_asignado.marcar_disponible()
            print(f"El vehículo ({type(vehiculo_asignado).__name__}) ha llegado al centro receptor y está disponible nuevamente.")

        else:
            print(f"El tiempo estimado de llegada ({tiempo_hasta_llegada}) excede el límite de viabilidad del órgano ({tiempo_transcurrido_maximo}).Proceso del transplante abortado")
            # liberar el vehículo si el traslado no se realiza
            vehiculo_asignado.marcar_disponible()
            print(f"El vehículo ({type(vehiculo_asignado).__name__}) se marca como disponible debido a la inviabilidad del órgano.")
            # Linerar al cirujano si se asigno pero no se realizo el trasplante
            if cirujano_asignado and cirujano_asignado.esta_disponible() == False:
                 cirujano_asignado.resetear_disponibilidad()
                 print(f"El cirujano ({cirujano_asignado.nombre}) se marca como disponible nuevamente.")

    def registrar_resultado_trasplante(self, receptor, organo, exito):
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
  

    






