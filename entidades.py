"""Clases base del sistema: Entidad (abstracta) y Cliente."""

import re                      # Expresiones regulares para validar texto
from abc import ABC, abstractmethod  # Herramientas para crear clases abstractas
from excepciones import ClienteInvalidoError, ParametroFaltanteError


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, id_entidad):
        # Valida que el identificador exista y no esté vacío
        if id_entidad is None or not str(id_entidad).strip():
            raise ParametroFaltanteError("El identificador es obligatorio")
        self._id = str(id_entidad).strip()  # Atributo protegido (encapsulado)

    @property
    def id(self):
        """Devuelve el identificador (solo lectura)."""
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad debe implementar su propia descripción."""


class Cliente(Entidad):
    """Cliente de Software FJ con datos personales encapsulados y validados."""

    def __init__(self, id_cliente, nombre, correo, telefono):
        super().__init__(id_cliente)  # Inicializa el id con la clase padre
        # Al asignar, se ejecutan los setters (validaciones)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ---------- Nombre ----------
    @property
    def nombre(self):
        return self.__nombre  # Atributo privado

    @nombre.setter
    def nombre(self, valor):
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El nombre es obligatorio")
        valor = str(valor).strip()
        if len(valor) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres")
        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü ]+$", valor):
            raise ClienteInvalidoError(f"El nombre solo admite letras: {valor!r}")
        self.__nombre = valor

    # ---------- Correo ----------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El correo es obligatorio")
        if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.-]+$", str(valor).strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self.__correo = str(valor).strip()

    # ---------- Teléfono ----------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or not str(valor).strip():
            raise ParametroFaltanteError("El teléfono es obligatorio")
        valor = str(valor).strip()
        if not valor.isdigit() or not 7 <= len(valor) <= 10:
            raise ClienteInvalidoError(f"Teléfono inválido (7 a 10 dígitos): {valor!r}")
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto de Entidad."""
        return f"Cliente {self._id}: {self.__nombre} <{self.__correo}> Tel: {self.__telefono}"
