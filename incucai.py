from donantes import Donante
from receptor import Receptor
from datetime import datetime, timedelta

class INCUCAI:
    def __init__(self):
        self.donantes = []
        self.receptores = []
        self.centros_salud = []
        self.trasplantes_realizados = []
    
    def registrar_paciente(self, paciente):
        if isinstance(paciente, Donante):
            if paciente not in self.donantes:
                self.donantes.append(paciente)
                print(f"Donante {paciente.nombre} registrado en el sistema.")
            else:
                print(f"El donante {paciente.nombre} ya está registrado.")
        elif isinstance(paciente, Receptor):
            if paciente not in self.receptores:
                self.receptores.append(paciente)
                print(f"Receptor {paciente.nombre} registrado en el sistema.")
            else:
                print(f"El receptor {paciente.nombre} ya está registrado.")
        else:
            print("Tipo de paciente no reconocido.")

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
        # Aquí la lógica sería buscar donantes con órganos compatibles con el receptor
        # Esto requeriría iterar sobre los donantes y sus órganos disponibles
        for donante in self.donantes:
            for organo_donado in donante.organos_a_donar:
                if receptor.es_compatible(donante) and receptor.organo_necesario == organo_donado:
                    coincidencias.append((donante, organo_donado))
        return coincidencias

    def iniciar_protocolo(self, donante, receptor, organo):
        print(f"Iniciando protocolo de trasplante de {organo} del donante {donante.nombre} al receptor {receptor.nombre}.")
        # 1. Seleccionar centro de salud (podríamos basarnos en la ubicación del receptor o donante)
        if not self.centros_salud:
            print("No hay centros de salud registrados.")
            return

        centro_receptor = receptor.centro_salud_asociado
        if not centro_receptor:
            print(f"El receptor {receptor.nombre} no tiene un centro de salud asociado.")
            return

        # 2. Asignar vehículo
        # Suponemos una distancia simbólica y usamos el centro del receptor como referencia
        vehiculo = centro_receptor.seleccionar_vehiculo_para_traslado(100, receptor.partido, receptor.provincia)
        if not vehiculo:
            print("No hay vehículo disponible.")
            return

        # 3. Seleccionar cirujano
        cirujano = centro_receptor.seleccionar_cirujano_para_operacion(organo)
        if not cirujano:
            print("No hay cirujano disponible.")
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
                # Aquí podríamos listar información del centro, sus pacientes, etc.
                print(f"Información del Centro de Salud: {centro.nombre}")
                donantes_en_centro = [d for d in self.donantes if d.centro_salud_asociado == centro]
                receptores_en_centro = [r for r in self.receptores if r.centro_salud_asociado == centro]
                print(f"  Donantes asociados: {[d.nombre for d in donantes_en_centro]}")
                print(f"  Receptores asociados: {[r.nombre for r in receptores_en_centro]}")
                return
        print(f"No se encontró ningún centro de salud con el nombre '{nombre_centro}'.")

    def buscar_prioridad_receptor(self, dni):
        for receptor in self.receptores:
            if receptor.get_dni() == dni:
                print(f"La prioridad del receptor con DNI {dni} es: {receptor.prioridad}")
                return
        print(f"No se encontró ningún receptor con el DNI '{dni}'.")
    

    def asignar_recursos(self, receptor, organo):
        centro_receptor = receptor.centro_salud_asociado
        if not centro_receptor:
            print(f"El receptor {receptor.nombre} no tiene un centro de salud asociado para la asignación de recursos.")
            return None, None  # No se pudo asignar vehículo ni cirujano

        # Simulación de la distancia (necesitaríamos una forma más realista en el futuro)
        distancia_simulada = 200  # Kilómetros (ejemplo)

        # Asignar vehículo desde el centro del receptor
        vehiculo_asignado = centro_receptor.seleccionar_vehiculo_para_traslado(
            distancia_simulada, receptor.partido, receptor.provincia
        )
        if not vehiculo_asignado:
            print(f"No se pudo asignar un vehículo desde el centro {centro_receptor.nombre}.")
            return None, None

        # Asignar cirujano desde el centro del receptor
        cirujano_asignado = centro_receptor.seleccionar_cirujano_para_operacion(organo.tipo_org)
        if not cirujano_asignado:
            print(f"No se pudo asignar un cirujano desde el centro {centro_receptor.nombre}.")
            return None, None

        print(f"Recursos asignados para el trasplante al receptor {receptor.nombre}:")
        print(f"  Vehículo: {type(vehiculo_asignado).__name__ if vehiculo_asignado else 'No asignado'}")
        print(f"  Cirujano: {cirujano_asignado.nombre if cirujano_asignado else 'No asignado'}")

        return vehiculo_asignado, cirujano_asignado

    def realizar_proceso_trasplante(self, donante, receptor, organo_a_donar):
        print(f"\nIniciando proceso de trasplante de {organo_a_donar} del donante {donante.nombre} al receptor {receptor.nombre}.")

        centro_donante = donante.centro_salud_asociado
        centro_receptor = receptor.centro_salud_asociado

        if not centro_donante or not centro_receptor:
            print("El donante o el receptor no tienen un centro de salud asociado.")
            return

        # 1. Realizar ablación en el centro del donante
        organo_ablacionado = centro_donante.realizar_ablacion(donante, organo_a_donar)
        if not organo_ablacionado:
            return

        # 2. Asignar recursos (vehículo y cirujano) desde el centro del receptor
        vehiculo_asignado, cirujano_asignado = self.asignar_recursos(receptor, organo_ablacionado)
        if not vehiculo_asignado or not cirujano_asignado:
            return

        # 3. Simular la distancia entre centros (necesitaríamos una forma más realista)
        distancia_km = 300  # Ejemplo: 300 km de distancia

        # 4. Calcular el tiempo de viaje
        tiempo_de_viaje = vehiculo_asignado.calcular_tiempo(distancia_km)
        print(f"Tiempo de viaje estimado: {tiempo_de_viaje}.")
        momento_llegada = organo_ablacionado.fecha_hora_ablacion + tiempo_de_viaje
        vehiculo_asignado.registrar_viaje(distancia=distancia_km, tiempo_estimado=tiempo_de_viaje)

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
            print(f"El tiempo estimado de llegada ({tiempo_hasta_llegada}) excede el límite de viabilidad del órgano ({tiempo_transcurrido_maximo}).")
            # También deberíamos liberar el vehículo si el traslado no se realiza
            vehiculo_asignado.marcar_disponible()
            print(f"El vehículo ({type(vehiculo_asignado).__name__}) se marca como disponible debido a la inviabilidad del órgano.")

        centro_donante = donante.centro_salud_asociado
        centro_receptor = receptor.centro_salud_asociado

        if not centro_donante or not centro_receptor:
            print("El donante o el receptor no tienen un centro de salud asociado.")
            return

        organo_ablacionado = centro_donante.realizar_ablacion(donante, organo_a_donar)
        if not organo_ablacionado:
            return

        # Modificamos la llamada a seleccionar_vehiculo_para_traslado
        vehiculo_asignado = centro_receptor.seleccionar_vehiculo_para_traslado(centro_donante)
        cirujano_asignado = self.asignar_recursos_local(receptor, organo_ablacionado, centro_receptor) # Usamos una versión local de asignar recursos

        if not vehiculo_asignado or not cirujano_asignado:
            return

        distancia = centro_receptor.obtener_distancia(centro_donante)

        if distancia:

            distancia_km = distancia  # Usamos la distancia calculada
        else:
            distancia_km = 100        # Usamos valor por defecto


        tiempo_de_viaje = vehiculo_asignado.calcular_tiempo(distancia_km)
        print(f"Tiempo de viaje estimado: {tiempo_de_viaje}.")
        momento_llegada = organo_ablacionado.fecha_hora_ablacion + tiempo_de_viaje
        vehiculo_asignado.registrar_viaje(distancia=distancia_km, trafico=None, tiempo_estimado=tiempo_de_viaje)

    def asignar_recursos_local(self, receptor, organo, centro): # Asignación desde un centro específico
        if not centro:
            print(f"No se puede asignar recursos, centro no especificado.")
            return None, None

        cirujano_asignado = centro.seleccionar_cirujano_para_operacion(organo.tipo_org)
        if not cirujano_asignado:
                print(f"No se pudo asignar un cirujano desde el centro {centro.nombre}.")
                return None

        print(f"Recurso asignado para el trasplante al receptor {receptor.nombre} en el centro {centro.nombre}:")
        print(f"  Cirujano: {cirujano_asignado.nombre if cirujano_asignado else 'No asignado'}")

        return cirujano_asignado, None # Solo devolvemos el cirujano aquí, el vehículo ya se seleccionó







