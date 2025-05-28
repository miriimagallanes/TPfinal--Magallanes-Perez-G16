from datetime import datetime, timedelta
from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from vehiculos.vehiculo_terrestre import Vehiculo_terrestre
from vehiculos.avion import Avion
from vehiculos.helicoptero import Helicoptero
from math import radians, cos, sin, atan2, sqrt
from excepciones import RecursoNoDisponibleError
from cirujanos import Cirujano 
 
class Centro_Salud:
    def __init__(self, nombre, direccion, partido, provincia, telefono, latitud=None, longitud=None):
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.telefono = telefono
        self.cirujanos = []
        self.vehiculos = []
        self.latitud = latitud
        self.longitud = longitud

    def agregar_cirujano(self, cirujano):
        self.cirujanos.append(cirujano)

    def agregar_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def buscar_pacientes(self, tipo, lista_pacientes):
        pacientes_encontrados = []
        for paciente in lista_pacientes:
            if paciente.centro_salud_asociado == self and \
               ((tipo == "donante" and isinstance(paciente, Donante)) or \
                (tipo == "receptor" and isinstance(paciente, Receptor))):
                pacientes_encontrados.append(paciente)
        return pacientes_encontrados

    def seleccionar_vehiculo_para_traslado(self, centro_receptor):
        vehiculo_seleccionado = None
        distancia = self.obtener_distancia(centro_receptor)

        if distancia is None:
           raise RecursoNoDisponibleError(f"No se pueden calcular distancias entre el centro {self.nombre} y el centro {centro_receptor.nombre} para seleccionar un vehículo. Faltan coordenadas.")
        else:
            # Lógica de selección basada en la distancia
            if distancia <= 100: # Distancias cortas, usar terrestre
                vehiculos_terrestres_disponibles = [v for v in self.vehiculos if isinstance(v, Vehiculo_terrestre) and v.disponible]
                if vehiculos_terrestres_disponibles:
                    vehiculo_seleccionado = max(vehiculos_terrestres_disponibles, key=lambda v: v.velocidad)
            elif distancia <= 500: #  Distancias medias, usar helicóptero
                helicopteros_disponibles = [v for v in self.vehiculos if isinstance(v, Helicoptero) and v.disponible]
                if helicopteros_disponibles:
                    vehiculo_seleccionado = helicopteros_disponibles[0]
            else: # Distancias largas, usar avión
                aviones_disponibles = [v for v in self.vehiculos if isinstance(v, Avion) and v.disponible]
                if aviones_disponibles:
                    vehiculo_seleccionado = aviones_disponibles[0]

        if vehiculo_seleccionado:
            vehiculo_seleccionado.marcar_no_disponible()
            print(f"Centro {self.nombre}: Se ha seleccionado un vehículo ({type(vehiculo_seleccionado).__name__}) para el traslado (distancia: {distancia:.2f} km).")
        else:
            raise RecursoNoDisponibleError(f"No hay vehiculos disponibles en el centro {self.nombre} para el traslado (distancia: {distancia: .2f}km).)")

        return vehiculo_seleccionado

    def seleccionar_cirujano_para_operacion(self, organo):
        cirujano_seleccionado = None
        especialidad_requerida = self._obtener_especialidad_para_organo(organo)

        if especialidad_requerida:
            for cirujano in self.cirujanos:
                if especialidad_requerida in cirujano.especialidades and cirujano.esta_disponible():
                    cirujano_seleccionado = cirujano
                    cirujano.marcar_como_no_disponible()
                    break

        if not cirujano_seleccionado:
            #Si no se encontro un cirujano especialista, buscamos uno general
            for cirujano in self.cirujanos:
                if not cirujano.especialidades and cirujano.esta_disponible():
                    cirujano_seleccionado = cirujano
                    cirujano.marcar_como_no_disponible()
                    break

        if cirujano_seleccionado:
            print(f"Centro {self.nombre}: Se ha seleccionado al cirujano {cirujano_seleccionado.nombre} para la operación de {organo}.")
        else:
           raise RecursoNoDisponibleError(f"No hay cirujano disponible en el centro {self.nombre} para la operación de {organo}.")
        return cirujano_seleccionado
    
    def realizar_ablacion(self, donante, organo_a_ablacion):
        if organo_a_ablacion in donante.organos_a_donar and organo_a_ablacion.fecha_hora_ablacion is None:
            organo_a_ablacion.asignar_fecha_hora_ablacion(datetime.now())
            donante.organos_a_donar.remove(organo_a_ablacion)
            donante.organos_ablacionados.append(organo_a_ablacion)  # Agregar aquí
            print(f"Ablación de {organo_a_ablacion.tipo_org} realizada.")
            return organo_a_ablacion
    

        elif organo_a_ablacion not in donante.organos_a_donar:
            print(f"Centro {self.nombre}: El órgano {organo_a_ablacion.tipo_org} no está en la lista de donación de {donante.nombre}.")
            return None
        else:
            print(f"Centro {self.nombre}: El órgano {organo_a_ablacion.tipo_org} ya ha sido ablacionado del donante {donante.nombre}.")
            return None

    def realizar_trasplante(self, receptor, organo, cirujano):
        if organo.fecha_hora_ablacion:
            tiempo_transcurrido = datetime.now() - organo.fecha_hora_ablacion
            if tiempo_transcurrido <= timedelta(hours=20):
                print(f"Centro {self.nombre}: Iniciando trasplante de {organo.tipo_org} al receptor {receptor.nombre} con el cirujano {cirujano.nombre}.")
                exito = cirujano.realizar_operacion(organo.tipo_org)
                cirujano.resetear_disponibilidad() # Liberar al cirujano después de la operación
                if exito:
                    print(f"Centro {self.nombre}: El trasplante de {organo.tipo_org} al receptor {receptor.nombre} ha sido exitoso.")
                    return True
                else:
                    receptor.prioridad = 1
                    receptor.estado = "Inestable"
                    print(f"Centro {self.nombre}: El trasplante de {organo.tipo_org} al receptor {receptor.nombre} ha fallado.")
                    return False
            else:
                print(f"Centro {self.nombre}: No se puede realizar el trasplante de {organo.tipo_org} al receptor {receptor.nombre}. Han pasado más de 20 horas desde la ablación.")
                return False
        else:
            print(f"Centro {self.nombre}: El órgano {organo.tipo_org} no tiene fecha y hora de ablación registrada.")
            return False
        
    def _obtener_especialidad_para_organo(self, organo):
        especialidades_por_organo = {
            "corazon": "cardiovascular",
            "pulmon": "pulmonar",
            "piel": "plástico",
            "corneas": "plástico",
            "huesos": "traumatólogo",
            "intestino": "gastroenterólogo",
            "riñon": "gastroenterólogo",
            "hígado": "gastroenterólogo",
            "pancreas": "gastroenterólogo"
        }
        return especialidades_por_organo.get(organo)

    def obtener_distancia(self, otro_centro):
        if self.latitud is None or self.longitud is None or otro_centro.latitud is None or otro_centro.longitud is None:
            return None  # No se pueden calcular distancias si faltan coordenadas

        R = 6371  # Radio de la Tierra en km

        lat1 = radians(self.latitud)
        lon1 = radians(self.longitud)
        lat2 = radians(otro_centro.latitud)
        lon2 = radians(otro_centro.longitud)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distancia = R * c

        return distancia  # en kilómetros