"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base: todas las demás heredan de esta."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente incorrectos (correo, teléfono, etc.)."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un dato obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Parámetros del servicio incorrectos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Datos de la reserva incorrectos (duración, etc.)."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Operación que no corresponde al estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Error en cálculo de costos, impuestos o descuentos."""
