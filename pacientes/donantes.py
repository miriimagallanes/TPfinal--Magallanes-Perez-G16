from pacientes.pacientes import Pacientes
import random 
from datetime import datetime
from organos import Organo
from typing import List , Optional
from centro_salud import Centro_Salud



class Donante(Pacientes):
    """
    Representa a un paciente donante de órganos.

    Almacena información relacionada con el fallecimiento y los órganos disponibles para ablación.
    """


    def __init__(self, nombre: str, dni: int, fecha_nacimiento: datetime, sexo: str,
                 telefono: str, tipo_sangre: str, centro_salud_asociado: 'Centro_Salud',
                 fecha_fallecimiento: datetime, hora_fallecimiento: str,
                 fecha_inicio_ablacion: datetime, hora_inicio_ablacion: str,
                 organos_a_donar_str: Optional[List[str]] = None):
        """
        Inicializa un nuevo donante con información adicional sobre su fallecimiento y órganos a donar.

        Params:
            organos_a_donar_str: Lista opcional de órganos en formato de texto.
        """
        super().__init__(nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado)
        self.fecha_fallecimiento = fecha_fallecimiento
        self.hora_fallecimiento = hora_fallecimiento
        self.fecha_inicio_ablacion = fecha_inicio_ablacion
        self.hora_inicio_ablacion = hora_inicio_ablacion
        self.organos_a_donar = [] # Inicializamos como lista vacía
        self.organos_ablacionados = []
        if organos_a_donar_str is not None:
            self._crear_objetos_organo(organos_a_donar_str)
        else:
            self._generar_organos_aleatorios()

    def _crear_objetos_organo(self, lista_organos_str: list[str]) -> None:
        """
        Crea instancias de órganos válidos a partir de una lista de nombres de órganos.

        Params:
            lista_organos_str (list[str]): Lista de cadenas representando tipos de órganos.

        Precondiciones:
            Cada órgano debe estar en Organo.TIPOS_VALIDOS.

        Effects:
            Agrega objetos Organo a la lista interna del donante.
        """

        for organo_str in lista_organos_str:
            try:
                organo = Organo(organo_str)
                self.organos_a_donar.append(organo)
            except ValueError as e:
                print(f"Error: El tipo de órgano '{organo_str}' no es válido para el donante {self.nombre}. Tipos válidos: {Organo.TIPOS_VALIDOS}")

    def _generar_organos_aleatorios(self) -> None:
        """
        Genera una cantidad aleatoria de órganos válidos para donar.

        Effects:
            Llama internamente a _crear_objetos_organo para agregar los órganos generados.
        """
        organos_posibles = Organo.TIPOS_VALIDOS
        cantidad_organos = random.randint(1, len(organos_posibles))
        organos_aleatorios_str = random.sample(organos_posibles, cantidad_organos)
        self._crear_objetos_organo(organos_aleatorios_str)

    def mostrar_organos_a_donar(self) -> None:
        """
        Imprime los órganos que están disponibles para donar.

        Effects:
            Muestra información por consola.
        """
        print(f"Órganos a donar por {self.nombre}: {', '.join(self.organos_a_donar)}")

    def remover_organo_donado(self, organo: Organo) -> None:
        """
        Elimina un órgano de la lista de órganos disponibles si existe.

        Params:
            organo (Organo): Objeto órgano a remover.

        Effects:
            Actualiza la lista de órganos del donante. Muestra mensaje si no existe.
        """

        if organo in self.organos_a_donar:
            self.organos_a_donar.remove(organo)
            print(f"Órgano {organo} removido de la lista de donación de {self.nombre}.")
        else:
            print(f"El órgano {organo} no está en la lista de donación de {self.nombre}.")

   