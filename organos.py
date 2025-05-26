from datetime import datetime

class Organo:
    TIPOS_VALIDOS = ["corazon", "higado", "riñon", "pulmon", "pancreas", "piel", "huesos", "intestino", "corneas"]

    def __init__(self, tipo_org):
        if tipo_org not in self.TIPOS_VALIDOS:
            raise ValueError(f"Tipo de órgano inválido: {tipo_org}. Los tipos válidos son: {self.TIPOS_VALIDOS}")
        self.tipo_org = tipo_org
        self.fecha_hora_ablacion = None # Se asigna cuando se realice la ablacion

    def asignar_fecha_hora_ablacion(self, fecha_hora: datetime):
        self.fecha_hora_ablacion = fecha_hora

    def __str__(self):
        if self.fecha_hora_ablacion:
            ablacion_info = self.fecha_hora_ablacion.strftime('%Y-%m-%d %H:%M') # Cadena de texto de deletime
        else:
            ablacion_info = "No ablacionado"
        return f"{self.tipo_org} (Ablación: {ablacion_info})"


    def es_compatible(self, receptor, donante): 
        if self.tipo_org != receptor.organo_necesario:
            return False

        # Lógica de compatibilidad ABO
        donante_tipo = donante.tipo_sangre
        receptor_tipo = receptor.tipo_sangre

        if donante_tipo == receptor_tipo:
            return True
        elif donante_tipo == 'O':
            return True
        elif receptor_tipo == 'AB':
            return True
        elif donante_tipo == 'A' and receptor_tipo == 'AB':
            return True
        elif donante_tipo == 'B' and receptor_tipo == 'AB':
            return True
        else:
            return False

    def esta_disponible(self): # Para saber si el órgano ya ha sido ablacionado.
        return self.fecha_hora_ablacion is None
    
    def __repr__(self):
        if self.fecha_hora_ablacion:
            ablacion_estado = "Ablacionado"
        else:
            ablacion_estado = "Pendiente"
        return f"Organo(tipo:{self.tipo_org}, estado: {ablacion_estado}"

    def __bool__(self):
    # Un órgano listo para trasplante si ha sido ablacionado.
        return self.fecha_hora_ablacion is not None








