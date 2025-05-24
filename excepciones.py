class PacienteNoEncontradoError(Exception):
    """Excepcion cuando un paciente no se encuentra en el sistema INCUCAI."""
    pass

class CentroSaludNoEncontradoError(Exception):
    """Excepción cuando un centro de salud no se encuentra en el sistema INCUCAI."""
    pass

class RecursosInsuficientesError(Exception):
    """Excepción cuando no se pueden asignar los recursos necesarios (vehículo/cirujano)."""
    pass

class RecursoNoDisponibleError(Exception):
    """Excepción cuando no hay un recurso disponible en un centro de salud específico."""
    pass

