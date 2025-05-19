from abc import ABC #, abstractmethod

# @abstractmethod 

class Pacientes(ABC):
  
    def __init__(self, nombre, dni, fecha_nacimiento, sexo, telefono, tipo_sangre, centro_salud_asociado = None):
        self.nombre = nombre
        self.__dni = dni 
        self.fecha_nacimiento = fecha_nacimiento
        self.sexo = sexo 
        self.telefono = telefono 
        self.tipo_sangre = tipo_sangre
        self.centro_salud_asociado = centro_salud_asociado 

    def __str__(self):
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
        
        return self.__dni


    

