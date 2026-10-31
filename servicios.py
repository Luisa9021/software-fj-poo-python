"""Servicios de Software FJ: clase abstracta Servicio y tres servicios especializados."""

from abc import abstractmethod  # Para declarar métodos abstractos
from entidades import Entidad
from excepciones import (
    ServicioInvalidoError,
    CalculoInconsistenteError,
)


class Servicio(Entidad):
    """Clase abstracta: define lo que todo servicio debe saber hacer."""

    IVA = 0.19  # Impuesto general (19 %)

    def __init__(self, id_servicio, nombre, tarifa_hora, disponible=True):
        super().__init__(id_servicio)  # El id se valida en Entidad
        self.nombre = nombre
        self.tarifa_hora = tarifa_hora
        self.disponible = disponible
        self.validar_parametros()  # Cada subclase valida sus propios datos

    @abstractmethod
    def calcular_costo(self, horas):
        """Costo base del servicio (cada subclase lo calcula distinto)."""

    @abstractmethod
    def validar_parametros(self):
        """Lanza ServicioInvalidoError si los datos son incorrectos."""

    def _validar_base(self):
        """Validaciones comunes a todos los servicios."""
        if not self.nombre or not str(self.nombre).strip():
            raise ServicioInvalidoError("El nombre del servicio es obligatorio")
        if not isinstance(self.tarifa_hora, (int, float)) or self.tarifa_hora <= 0:
            raise ServicioInvalidoError(
                f"La tarifa por hora debe ser un número positivo: {self.tarifa_hora!r}"
            )

    # "Sobrecarga" de métodos: tres variantes con parámetros opcionales
    def calcular_costo_total(self, horas, impuesto=0.0, descuento=0.0):
        """Costo final. Sin extras: costo base. Con impuesto y/o descuento: los aplica."""
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise CalculoInconsistenteError(f"Horas inválidas para el cálculo: {horas!r}")
        if not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                f"El descuento debe estar entre 0 y 1 (recibido {descuento})"
            )
        if impuesto < 0:
            raise CalculoInconsistenteError("El impuesto no puede ser negativo")
        base = self.calcular_costo(horas)
        return round(base * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        """Descripción genérica; las subclases la sobrescriben (polimorfismo)."""
        return f"Servicio {self._id}: {self.nombre} - ${self.tarifa_hora}/h"


class ReservaSala(Servicio):
    """Reserva de salas: el costo depende de las horas y la capacidad."""

    def __init__(self, id_servicio, nombre, tarifa_hora, capacidad, disponible=True):
        self.capacidad = capacidad  # Se asigna antes para poder validarla
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        self._validar_base()
        if not isinstance(self.capacidad, int) or self.capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {self.capacidad!r}")

    def calcular_costo(self, horas):
        # Salas de más de 20 personas tienen un recargo del 10 %
        recargo = 1.10 if self.capacidad > 20 else 1.0
        return self.tarifa_hora * horas * recargo

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}) - ${self.tarifa_hora}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: el costo suma un depósito fijo."""

    def __init__(self, id_servicio, nombre, tarifa_hora, deposito, disponible=True):
        self.deposito = deposito
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        self._validar_base()
        if not isinstance(self.deposito, (int, float)) or self.deposito < 0:
            raise ServicioInvalidoError(f"Depósito inválido: {self.deposito!r}")

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas + self.deposito

    def describir(self):
        return f"Equipo '{self.nombre}' - ${self.tarifa_hora}/h + depósito ${self.deposito}"


class AsesoriaEspecializada(Servicio):
    """Asesorías: el nivel del asesor modifica el costo."""

    NIVELES = {"junior": 1.0, "senior": 1.25}  # Multiplicador por nivel

    def __init__(self, id_servicio, nombre, tarifa_hora, nivel, disponible=True):
        self.nivel = str(nivel).lower() if nivel is not None else None
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)

    def validar_parametros(self):
        self._validar_base()
        if self.nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido {self.nivel!r}. Use: {list(self.NIVELES)}"
            )

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas * self.NIVELES[self.nivel]

    def describir(self):
        return f"Asesoría '{self.nombre}' (nivel {self.nivel}) - ${self.tarifa_hora}/h"
