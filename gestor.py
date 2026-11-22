"""Administración en memoria de clientes, servicios y reservas."""
import logging
from pathlib import Path
from excepciones import ErrorSistema, DatoInvalidoError, ServicioNoDisponibleError
from clientes import Cliente
from reservas import Reserva

RUTA_LOG = Path(__file__).parent / "logs" / "sistema.log"
RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=RUTA_LOG,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    encoding="utf-8",
    force=True
)

class GestorSistema:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("El objeto no corresponde a un cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise DatoInvalidoError("Ya existe un cliente con ese identificador.")
        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        if not servicio.disponible:
            raise ServicioNoDisponibleError("No se puede registrar un servicio no disponible.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise DatoInvalidoError("Ya existe un servicio con ese identificador.")
        self.servicios.append(servicio)
        logging.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, identificador, id_cliente, id_servicio, duracion):
        cliente = next((c for c in self.clientes if c.identificador == str(id_cliente)), None)
        servicio = next((s for s in self.servicios if s.identificador == str(id_servicio)), None)
        if cliente is None:
            raise DatoInvalidoError("No se encontró el cliente solicitado.")
        if servicio is None:
            raise DatoInvalidoError("No se encontró el servicio solicitado.")
        reserva = Reserva(identificador, cliente, servicio, duracion)
        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", identificador)
        return reserva

    def buscar_reserva(self, identificador):
        reserva = next((r for r in self.reservas if r.identificador == str(identificador)), None)
        if reserva is None:
            raise DatoInvalidoError("No existe la reserva indicada.")
        return reserva

    def mostrar_resumen(self):
        print("\n--- RESUMEN DEL SISTEMA ---")
        print(f"Clientes registrados: {len(self.clientes)}")
        print(f"Servicios registrados: {len(self.servicios)}")
        print(f"Reservas creadas: {len(self.reservas)}")
        for reserva in self.reservas:
            print(reserva)
