"""Modelo de cliente con encapsulación y validación."""
from entidades import Entidad
from excepciones import DatoInvalidoError

class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono
        self.validar()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def validar(self):
        if not isinstance(self.__nombre, str) or len(self.__nombre.strip()) < 3:
            raise DatoInvalidoError("El nombre debe tener al menos 3 caracteres.")
        if not isinstance(self.__correo, str) or "@" not in self.__correo or "." not in self.__correo:
            raise DatoInvalidoError("El correo electrónico no tiene un formato válido.")
        if not str(self.__telefono).isdigit() or len(str(self.__telefono)) < 7:
            raise DatoInvalidoError("El teléfono debe contener al menos 7 dígitos.")
        return True

    def __str__(self):
        return f"Cliente {self.identificador}: {self.nombre} ({self.correo})"
