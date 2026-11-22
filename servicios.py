"""Jerarquía de servicios: abstracción, herencia y polimorfismo."""
from abc import abstractmethod
from entidades import Entidad
from excepciones import DatoInvalidoError

class Servicio(Entidad):
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        self.nombre = nombre
        self.tarifa_hora = float(tarifa_hora)
        self.disponible = bool(disponible)
        self.validar()

    def validar(self):
        if not isinstance(self.nombre, str) or not self.nombre.strip():
            raise DatoInvalidoError("El nombre del servicio es obligatorio.")
        if self.tarifa_hora <= 0:
            raise DatoInvalidoError("La tarifa por hora debe ser mayor que cero.")
        return True

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        pass

    def _calcular_total(self, duracion, impuesto=0.19, descuento=0.0):
        # La misma función permite calcular el costo básico o con
        # parámetros opcionales (impuesto y descuento), simulando sobrecarga.
        if not 0 <= impuesto <= 1:
            raise DatoInvalidoError("El impuesto debe estar entre 0 y 1.")
        if not 0 <= descuento <= 1:
            raise DatoInvalidoError("El descuento debe estar entre 0 y 1.")
        subtotal = self.tarifa_hora * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        self.capacidad = int(capacidad)
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar(self):
        super().validar()
        if self.capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser positiva.")
        return True

    def describir(self):
        return f"Sala '{self.nombre}', capacidad para {self.capacidad} personas."

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatoInvalidoError("La duración de la reserva debe ser positiva.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion)
        return self._calcular_total(duracion, impuesto, descuento)


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, unidades, disponible=True):
        self.unidades = int(unidades)
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar(self):
        super().validar()
        if self.unidades <= 0:
            raise DatoInvalidoError("Las unidades disponibles deben ser positivas.")
        return True

    def describir(self):
        return f"Alquiler de equipo: {self.nombre}. Unidades disponibles: {self.unidades}."

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatoInvalidoError("Las horas de alquiler deben ser positivas.")
        if self.unidades < 1:
            raise DatoInvalidoError("No hay unidades disponibles.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion)
        return self._calcular_total(duracion, impuesto, descuento)


class Asesoria(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        self.especialidad = especialidad
        super().__init__(identificador, nombre, tarifa_hora, disponible)

    def validar(self):
        super().validar()
        if not isinstance(self.especialidad, str) or not self.especialidad.strip():
            raise DatoInvalidoError("La especialidad de la asesoría es obligatoria.")
        return True

    def describir(self):
        return f"Asesoría especializada en {self.especialidad}: {self.nombre}."

    def validar_parametros(self, duracion):
        if duracion <= 0:
            raise DatoInvalidoError("La duración de la asesoría debe ser positiva.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion)
        return self._calcular_total(duracion, impuesto, descuento)
