"""Ejecución de demostración con más de diez operaciones y manejo de errores."""
import logging
from gestor import GestorSistema, RUTA_LOG
from clientes import Cliente
from servicios import ReservaSala, AlquilerEquipo, Asesoria
from excepciones import ErrorSistema

def ejecutar_operacion(numero, descripcion, funcion):
    print(f"\nOPERACIÓN {numero}: {descripcion}")
    try:
        resultado = funcion()
    except ErrorSistema as error:
        logging.exception("Operación %s fallida: %s", numero, error)
        print(f"Error controlado: {error}")
    except (TypeError, ValueError) as error:
        logging.exception("Error de datos en operación %s: %s", numero, error)
        print(f"Error de datos controlado: {error}")
    else:
        print(f"Resultado: {resultado}")
    finally:
        print(f"Fin de la operación {numero}.")

def main():
    sistema = GestorSistema()

    # 1. Registro válido de cliente.
    ejecutar_operacion(1, "Registrar cliente válido",
        lambda: sistema.registrar_cliente(Cliente("C001", "Ana Pérez", "ana@gmail.com", "3001234567")))

    # 2. Otro cliente válido.
    ejecutar_operacion(2, "Registrar segundo cliente",
        lambda: sistema.registrar_cliente(Cliente("C002", "Carlos Gómez", "carlos@gmail.com", "3101234567")))

    # 3. Cliente inválido: correo sin formato correcto.
    ejecutar_operacion(3, "Intentar registrar cliente con correo inválido",
        lambda: sistema.registrar_cliente(Cliente("C003", "Luis Rojas", "correo-invalido", "3201234567")))

    # 4. Crear servicio de sala.
    sala = ReservaSala("S001", "Sala de reuniones", 50000, 12)
    ejecutar_operacion(4, "Agregar servicio de reserva de sala",
        lambda: sistema.agregar_servicio(sala))

    # 5. Crear servicio de alquiler de equipo.
    equipo = AlquilerEquipo("S002", "Video proyector", 25000, 4)
    ejecutar_operacion(5, "Agregar servicio de alquiler de equipo",
        lambda: sistema.agregar_servicio(equipo))

    # 6. Crear servicio de asesoría.
    asesoria = Asesoria("S003", "Asesoría de software", 80000, "desarrollo Python")
    ejecutar_operacion(6, "Agregar servicio de asesoría",
        lambda: sistema.agregar_servicio(asesoria))

    # 7. Servicio inválido: tarifa negativa.
    ejecutar_operacion(7, "Intentar crear servicio con tarifa negativa",
        lambda: sistema.agregar_servicio(ReservaSala("S004", "Sala inválida", -1000, 10)))

    # 8. Crear reserva correcta.
    def reserva_correcta():
        reserva = sistema.crear_reserva("R001", "C001", "S001", 2)
        total = reserva.confirmar()
        return f"{reserva}; total calculado ${total:,.2f}"
    ejecutar_operacion(8, "Crear y confirmar reserva de sala", reserva_correcta)

    # 9. Reserva con cliente inexistente.
    ejecutar_operacion(9, "Intentar reservar con cliente inexistente",
        lambda: sistema.crear_reserva("R002", "C999", "S001", 1))

    # 10. Reserva con duración inválida.
    ejecutar_operacion(10, "Intentar crear reserva con duración negativa",
        lambda: sistema.crear_reserva("R003", "C002", "S002", -3))

    # 11. Crear y confirmar alquiler con descuento.
    def reserva_equipo():
        reserva = sistema.crear_reserva("R004", "C002", "S002", 3)
        total = reserva.confirmar(descuento=0.10)
        return f"{reserva}; total con descuento ${total:,.2f}"
    ejecutar_operacion(11, "Confirmar alquiler de equipo con descuento", reserva_equipo)

    # 12. Cancelar una reserva existente.
    ejecutar_operacion(12, "Cancelar reserva R004",
        lambda: sistema.buscar_reserva("R004").cancelar())

    # 13. Intentar cancelar una reserva inexistente.
    ejecutar_operacion(13, "Buscar reserva inexistente",
        lambda: sistema.buscar_reserva("R999"))

    # Ejemplo de encadenamiento de excepciones (raise ... from ...).
    print("\nEJEMPLO ADICIONAL: encadenamiento de excepciones")
    try:
        try:
            int("texto-no-numerico")
        except ValueError as error_original:
            raise ErrorSistema("No fue posible convertir el dato a número.") from error_original
    except ErrorSistema as error:
        logging.exception("Excepción encadenada")
        print(f"Excepción controlada y encadenada: {error}")
        print(f"Excepción original: {type(error.__cause__).__name__}")

    sistema.mostrar_resumen()
    print(f"\nLos eventos y errores quedaron registrados en: {RUTA_LOG}")

if __name__ == "__main__":
    main()
