from abc import ABC



class Pacientes(ABC):
    """
    Clase abstracta base para representar a los pacientes del sistema,
    ya sean donantes o receptores. Contiene atributos y métodos comunes
    para la identificación y asociación a un centro de salud.
  
    """

    
    def __init__(self, nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado = None):
        """
        Inicializa un nuevo Pacientes.

        Params:
            nombre (str): Nombre completo del paciente.
            dni (int): Número de DNI único del paciente.
            fecha_nacimiento (datetime): Fecha de nacimiento del paciente.
            sexo (str): Sexo del paciente.
            telefono (str): Número de teléfono.
            tipo_sangre (str): Tipo de sangre del paciente.
            centro_salud_asociado (Centro_Salud, optional): Centro de salud al que pertenece (puede ser None).
        """
        self.nombre = nombre
        self.__dni = dni 
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo 
        self.telefono = telefono 
        self.tipo_sangre = tipo_sangre
        self.centro_salud_asociado = centro_salud_asociado 

    def __str__(self):
        """
        Retorna una representación en texto del paciente

        Returns:
            str: Cadena de texto con la información principal del paciente.
        """

        if self.centro_salud_asociado:
            centro_salud_nombre = self.centro_salud_asociado.nombre 
        else:
            centro_salud_nombre = "No asignado"
        return (
            f"\nNombre: {self.nombre},"
            f"\nDNI: {self.__dni},"
            f"\nFecha de Nacimiento: {self.fecha_nacimiento},"
            f"\nSexo: {self.sexo},"
            f"\nTeléfono: {self.telefono},"
            f"\nTipo de Sangre: {self.tipo_sangre},"
            f"\nCentro de Salud: {centro_salud_nombre}"
        )
    
    def get_dni(self):
        """
        Retorna el número de DNI del paciente.

        Returns:
            int: DNI del paciente.
        """
        
        return self.__dni

    def get_partido(self):
        """
         Retorna el partido del centro de salud asociado, si existe.

        Returns:
             Optional[str]: Nombre del partido o None.
        """
        return self.centro_salud_asociado.partido if self.centro_salud_asociado else None

    

