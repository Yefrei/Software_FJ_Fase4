"""Entidad Reserva y operaciones de confirmación/cancelación."""
from entidades import Entidad
from excepciones import ReservaInvalidaError, OperacionNoPermitidaError

class Reserva(Entidad):
    def __init__(self, identificador, cliente, servicio, duracion):
        super().__init__(identificador)
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.estado = "PENDIENTE"
        self.total = 0.0
        self.validar()

    def validar(self):
        if self.cliente is None or self.servicio is None:
            raise ReservaInvalidaError("La reserva requiere cliente y servicio.")
        if self.duracion <= 0:
            raise ReservaInvalidaError("La duración debe ser mayor que cero.")
        return True

    def confirmar(self, impuesto=0.19, descuento=0.0):
        if self.estado != "PENDIENTE":
            raise OperacionNoPermitidaError("Solo se pueden confirmar reservas pendientes.")
        if not self.servicio.disponible:
            raise ReservaInvalidaError("El servicio seleccionado no está disponible.")
        self.total = self.servicio.calcular_costo(self.duracion, impuesto, descuento)
        self.estado = "CONFIRMADA"
        return self.total

    def cancelar(self):
        if self.estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya está cancelada.")
        self.estado = "CANCELADA"
        return True

    def __str__(self):
        return (f"Reserva {self.identificador} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Estado: {self.estado} | "
                f"Total: ${self.total:,.2f}")
