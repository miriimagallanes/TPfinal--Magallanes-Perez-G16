from __future__ import annotations
from math import radians, cos, sin, atan2, sqrt
from datetime import datetime, timedelta
from typing import Optional, List, TYPE_CHECKING
from excepciones.excepciones import RecursoNoDisponibleError
from pacientes.donantes import Donante
from pacientes.receptor import Receptor
from organos.organos import Organo
from cirujanos.cirujanos import Cirujano
from vehiculos.vehiculos import Vehiculos
from vehiculos.vehiculoterrestre import VehiculoTerrestre
from vehiculos.helicoptero import Helicoptero
from vehiculos.avion import Avion


 
class CentroSalud:
    """
    Representa un centro de salud donde trabajan cirujanos y se alojan vehículos médicos.

    Permite registrar recursos, realizar ablaciones, trasplantes y seleccionar personal y vehículos.
    """


    def __init__(self, nombre: str, direccion: str, partido: str, provincia: str, telefono: str, latitud: Optional[float] = None, longitud: Optional[float] = None):
        
        """
        Inicializa un centro de salud.

        Params:
            nombre (str): Nombre del centro.
            direccion (str): Dirección del centro.
            partido (str): Partido al que pertenece.
            provincia (str): Provincia del centro.
            telefono (str): Teléfono de contacto.
            latitud (float, optional): Coordenada geográfica.
            longitud (float, optional): Coordenada geográfica.
        """
        self.nombre = nombre
        self.direccion = direccion
        self.partido = partido
        self.provincia = provincia
        self.telefono = telefono
        self.cirujanos = []
        self.vehiculos = []
        self.latitud = latitud
        self.longitud = longitud

    def agregar_cirujano(self, cirujano: 'Cirujano') -> None:
        
        """
        Agrega un cirujano al centro.

        Effects:
            Modifica la lista interna de cirujanos.
        """
        self.cirujanos.append(cirujano)

    def agregar_vehiculo(self, vehiculo: 'Vehiculos') -> None:
        
        """
        Agrega un vehículo al centro.

        Effects:
            Modifica la lista interna de vehículos.
        """
        self.vehiculos.append(vehiculo)

    def buscar_pacientes(self, tipo: str, lista_pacientes: list) -> list:
        
        """
        Filtra pacientes asociados al centro de acuerdo al tipo.

        Params:
            tipo (str): "donante" o "receptor"
            lista_pacientes (list): Lista general de pacientes.

        Returns:
            list: Lista de pacientes del tipo dado asociados a este centro.
        """
        pacientes_encontrados = []
        for paciente in lista_pacientes:
            if paciente.centro_salud_asociado == self and \
               ((tipo == "donante" and isinstance(paciente, Donante)) or \
                (tipo == "receptor" and isinstance(paciente, Receptor))):
                pacientes_encontrados.append(paciente)
        return pacientes_encontrados

    def seleccionar_vehiculo_para_traslado(self, centro_receptor: CentroSalud) -> Vehiculos:
        
        """
        Selecciona el vehículo más adecuado según la distancia al centro receptor.

        Params:
            centro_receptor (Centro_Salud): Centro de destino.

        Returns:
            Vehiculos: Vehículo seleccionado.

        Raises:
            RecursoNoDisponibleError: Si no hay vehículos adecuados o falta información.
        """

        vehiculo_seleccionado = None
        distancia = self.obtener_distancia(centro_receptor)

        if distancia is None:
           raise RecursoNoDisponibleError(f"No se pueden calcular distancias entre el centro {self.nombre} y el centro {centro_receptor.nombre} para seleccionar un vehículo. Faltan coordenadas.")
        else:
            if distancia <= 100:
                vehiculos_terrestres_disponibles = [v for v in self.vehiculos if isinstance(v, VehiculoTerrestre) and v.disponible]
                if vehiculos_terrestres_disponibles:
                    vehiculo_seleccionado = max(vehiculos_terrestres_disponibles, key=lambda v: v.velocidad)
            elif distancia <= 500: 
                helicopteros_disponibles = [v for v in self.vehiculos if isinstance(v, Helicoptero) and v.disponible]
                if helicopteros_disponibles:
                    vehiculo_seleccionado = helicopteros_disponibles[0]
            else: 
                aviones_disponibles = [v for v in self.vehiculos if isinstance(v, Avion) and v.disponible]
                if aviones_disponibles:
                    vehiculo_seleccionado = aviones_disponibles[0]

        if vehiculo_seleccionado:
            vehiculo_seleccionado.marcar_no_disponible()
            print(f"Centro {self.nombre}: Se ha seleccionado un vehículo ({type(vehiculo_seleccionado).__name__}) para el traslado (distancia: {distancia:.2f} km).")
        else:
            raise RecursoNoDisponibleError(f"No hay vehiculos disponibles en el centro {self.nombre} para el traslado (distancia: {distancia: .2f}km).)")

        return vehiculo_seleccionado

    def seleccionar_cirujano_para_operacion(self, organo: str) -> Cirujano:
        
        """
        Selecciona un cirujano disponible que pueda operar el órgano.

        Params:
            organo (str): Tipo de órgano que requiere intervención.

        Returns:
            Cirujano: Cirujano disponible.

        Raises:
            RecursoNoDisponibleError: Si no hay cirujanos disponibles.
        """
        cirujano_seleccionado = None
        especialidad_requerida = self._obtener_especialidad_para_organo(organo)

        if especialidad_requerida:
            for cirujano in self.cirujanos:
                if especialidad_requerida in cirujano.especialidades and cirujano.esta_disponible():
                    cirujano_seleccionado = cirujano
                    cirujano.marcar_como_no_disponible()
                    break

        if not cirujano_seleccionado:
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
    
    def realizar_ablacion(self, donante: 'Donante', organo_a_ablacion: 'Organo') -> Optional['Organo']:
        
        """
        Asigna fecha de ablación a un órgano y lo remueve del donante.

        Params:
            donante (Donante): Donante al que se le realiza la ablación.
            organo_a_ablacion (Organo): Órgano a ablacionar.

        Returns:
            Organo: El órgano ablacionado si fue exitoso, None en caso contrario.

        Effects:
            Modifica lista de órganos del donante y marca fecha de ablación.
        """
        if organo_a_ablacion in donante.organos_a_donar and organo_a_ablacion.fecha_hora_ablacion is None:
            organo_a_ablacion.asignar_fecha_hora_ablacion(datetime.now())
            donante.organos_a_donar.remove(organo_a_ablacion)
            donante.organos_ablacionados.append(organo_a_ablacion) 
            print(f"Ablación de {organo_a_ablacion.tipo_org} realizada.")
            return organo_a_ablacion
    
        elif organo_a_ablacion not in donante.organos_a_donar:
            print(f"Centro {self.nombre}: El órgano {organo_a_ablacion.tipo_org} no está en la lista de donación de {donante.nombre}.")
            return None
        else:
            print(f"Centro {self.nombre}: El órgano {organo_a_ablacion.tipo_org} ya ha sido ablacionado del donante {donante.nombre}.")
            return None

    def realizar_trasplante(self, receptor: 'Receptor', organo: 'Organo', cirujano: 'Cirujano') -> bool:
        
        """
        Realiza un trasplante en caso de que el órgano siga siendo viable.

        Params:
            receptor (Receptor): Receptor del órgano.
            organo (Organo): Órgano a trasplantar.
            cirujano (Cirujano): Cirujano encargado.

        Returns:
            bool: True si fue exitoso, False si falló o no es viable.

        Effects:
            Puede modificar el estado del receptor y registrar operación en el cirujano.
        """
        if organo.fecha_hora_ablacion:
            tiempo_transcurrido = datetime.now() - organo.fecha_hora_ablacion
            if tiempo_transcurrido <= timedelta(hours=20):
                print(f"Centro {self.nombre}: Iniciando trasplante de {organo.tipo_org} al receptor {receptor.nombre} con el cirujano {cirujano.nombre}.")
                exito = cirujano.realizar_operacion(organo.tipo_org)
                cirujano.resetear_disponibilidad() 
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
        
    def _obtener_especialidad_para_organo(self, organo: str) -> Optional[str]:
        
        """
        Devuelve la especialidad médica requerida para operar un órgano.

        Params:
            organo (str): Tipo de órgano.

        Returns:
            str: Especialidad requerida o None si no hay coincidencia.
        """
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

    def obtener_distancia(self, otro_centro: 'CentroSalud') -> Optional[float]:
        
        """
        Calcula la distancia geográfica en km al otro centro usando fórmula de Haversine.

        Params:
            otro_centro (Centro_Salud): Centro de destino.

        Returns:
            float: Distancia en kilómetros o None si faltan coordenadas.
        """
        if self.latitud is None or self.longitud is None or otro_centro.latitud is None or otro_centro.longitud is None:
            return None  

        R = 6371  

        lat1 = radians(self.latitud)
        lon1 = radians(self.longitud)
        lat2 = radians(otro_centro.latitud)
        lon2 = radians(otro_centro.longitud)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distancia = R * c

        return distancia  



