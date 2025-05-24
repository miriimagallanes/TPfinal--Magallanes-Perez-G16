from pacientes.pacientes import Pacientes
import random 
from datetime import datetime
from organos import Organo

class Donante(Pacientes):
    def __init__(self, nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado,
                 fecha_fallecimiento, hora_fallecimiento, fecha_inicio_ablacion, hora_inicio_ablacion,
                 organos_a_donar_str=None): 
        super().__init__(nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado)
        self.fecha_fallecimiento = fecha_fallecimiento
        self.hora_fallecimiento = hora_fallecimiento
        self.fecha_inicio_ablacion = fecha_inicio_ablacion
        self.hora_inicio_ablacion = hora_inicio_ablacion
        self.organos_a_donar = [] # Inicializamos como lista vacía
        if organos_a_donar_str is not None:
            self._crear_objetos_organo(organos_a_donar_str)
        else:
            self._generar_organos_aleatorios()

    def _crear_objetos_organo(self, lista_organos_str):
        for organo_str in lista_organos_str:
            try:
                organo = Organo(organo_str)
                self.organos_a_donar.append(organo)
            except ValueError as e:
                print(f"Error: El tipo de órgano '{organo_str}' no es válido para el donante {self.nombre}. Tipos válidos: {Organo.TIPOS_VALIDOS}")


    def _generar_organos_aleatorios(self):
        organos_posibles = Organo.TIPOS_VALIDOS
        cantidad_organos = random.randint(1, len(organos_posibles))
        organos_aleatorios_str = random.sample(organos_posibles, cantidad_organos)
        self._crear_objetos_organo(organos_aleatorios_str)

    def mostrar_organos_a_donar(self):
        print(f"Órganos a donar por {self.nombre}: {', '.join(self.organos_a_donar)}")

    def remover_organo_donado(self, organo):
        if organo in self.organos_a_donar:
            self.organos_a_donar.remove(organo)
            print(f"Órgano {organo} removido de la lista de donación de {self.nombre}.")
        else:
            print(f"El órgano {organo} no está en la lista de donación de {self.nombre}.")

