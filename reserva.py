"""Reserva de Software FJ: integra cliente, servicio, duración y estado."""

from enum import Enum  # Para definir los estados posibles de una reserva
from entidades import Cliente
from servicios import Servicio
from excepciones import (
    SoftwareFJError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
)
from logger import registrar_evento, registrar_error


class EstadoReserva(Enum):
    """Estados por los que puede pasar una reserva."""
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    PROCESADA = "procesada"


class Reserva:
    """Une un cliente con un servicio durante una cantidad de horas."""

    def __init__(self, id_reserva, cliente, servicio, horas):
        # 1. Parámetros faltantes
        if cliente is None or servicio is None:
            raise ParametroFaltanteError("La reserva requiere cliente y servicio")
        # 2. Tipos correctos
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("Cliente o servicio con tipo incorrecto")
        # 3. Duración válida (excepción encadenada si no es un número)
        try:
            horas = float(horas)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError(f"Duración no numérica: {horas!r}") from error
        if horas <= 0:
            raise ReservaInvalidaError(f"La duración debe ser mayor que cero: {horas}")
        # 4. Disponibilidad del servicio
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible")

        self.id = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = EstadoReserva.PENDIENTE  # Toda reserva nace pendiente
        registrar_evento(f"Reserva {self.id} creada para {cliente.id} ({servicio.nombre})")

    def confirmar(self):
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self.estado != EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self.estado.value}"
            )
        self.estado = EstadoReserva.CONFIRMADA
        registrar_evento(f"Reserva {self.id} confirmada")

    def cancelar(self):
        """Cancela la reserva, salvo que ya esté cancelada o procesada."""
        if self.estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self.estado.value}"
            )
        self.estado = EstadoReserva.CANCELADA
        registrar_evento(f"Reserva {self.id} cancelada")

    # "Sobrecarga": un solo método con parámetros opcionales
    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Sin argumentos: costo base. Con impuesto/descuento: costo ajustado."""
        return self.servicio.calcular_costo_total(self.horas, impuesto, descuento)

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo final y deja la reserva como PROCESADA."""
        try:
            # Solo se procesan reservas confirmadas
            if self.estado != EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesan reservas confirmadas (estado: {self.estado.value})"
                )
            costo = self.calcular_costo(impuesto, descuento)
        except SoftwareFJError as error:
            # Se registra el error y se relanza para que lo maneje quien llamó
            registrar_error(f"Reserva {self.id} no pudo procesarse: {error}")
            raise
        else:
            # Solo se ejecuta si NO hubo errores
            self.estado = EstadoReserva.PROCESADA
            registrar_evento(f"Reserva {self.id} procesada. Total: ${costo}")
            return costo
        finally:
            # Se ejecuta SIEMPRE, haya o no error
            registrar_evento(f"Fin del intento de procesar la reserva {self.id}")

    def describir(self):
        return (f"Reserva {self.id} | {self.cliente.nombre} | "
                f"{self.servicio.nombre} | {self.horas} h | {self.estado.value}")
