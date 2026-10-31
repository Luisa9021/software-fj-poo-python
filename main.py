"""Simulación de operaciones del sistema Software FJ (sin base de datos)."""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import Reserva, EstadoReserva
from excepciones import SoftwareFJError, ReservaInvalidaError
from logger import registrar_evento, registrar_error

# "Base de datos" en memoria: solo listas de objetos
clientes = []
servicios = []
reservas = []


def buscar(lista, identificador):
    """Busca un objeto por id dentro de una lista."""
    for elemento in lista:
        if elemento.id == identificador:
            return elemento
    raise ReservaInvalidaError(f"No existe el elemento {identificador!r}")


def agregar_cliente(cliente):
    """Guarda un cliente en la lista y devuelve su descripción."""
    clientes.append(cliente)
    return cliente.describir()


def agregar_servicio(servicio):
    """Guarda un servicio en la lista y devuelve su descripción."""
    servicios.append(servicio)
    return servicio.describir()


def crear_reserva(id_reserva, cliente, servicio, horas):
    """Crea una reserva, la guarda en la lista y la devuelve."""
    reserva = Reserva(id_reserva, cliente, servicio, horas)
    reservas.append(reserva)
    return reserva


def reservar_y_confirmar():
    """Operación 8: crea la reserva R01 y la confirma."""
    reserva = crear_reserva("R01", buscar(clientes, "C01"), buscar(servicios, "S01"), 3)
    reserva.confirmar()
    return reserva.describir()


def cancelar_dos_veces():
    """Operación 10: la segunda cancelación debe fallar."""
    reserva = crear_reserva("R02", buscar(clientes, "C01"), buscar(servicios, "S03"), 2)
    reserva.cancelar()   # Primera cancelación: válida
    reserva.cancelar()   # Segunda cancelación: lanza OperacionNoPermitidaError
    return reserva.describir()


def ejecutar(numero, descripcion, accion):
    """Ejecuta una operación sin que un error detenga el programa."""
    print(f"\n--- Operación {numero}: {descripcion} ---")
    try:
        resultado = accion()
    except SoftwareFJError as error:
        # Error controlado del sistema
        print(f"[ERROR CONTROLADO] {error}")
        registrar_error(f"Operación {numero} ({descripcion}): {error}")
        if error.__cause__ is not None:  # Muestra la causa si hubo encadenamiento
            registrar_error(f"   Causa original: {error.__cause__!r}")
    except Exception as error:
        # Red de seguridad: cualquier error inesperado
        print(f"[ERROR INESPERADO] {error}")
        registrar_error(f"Operación {numero} - error inesperado: {error!r}")
    else:
        # Solo se ejecuta si no hubo ningún error
        print(f"[OK] {resultado}")
        registrar_evento(f"Operación {numero} exitosa: {descripcion}")
    finally:
        # Se ejecuta siempre
        print("    (operación finalizada, el sistema continúa)")


def main():
    registrar_evento("=== Inicio de la simulación de Software FJ ===")

    # ----- CLIENTES -----
    ejecutar(1, "Registrar cliente válido",
             lambda: agregar_cliente(Cliente("C01", "Ana Torres", "ana@correo.com", "3001234567")))
    ejecutar(2, "Registrar cliente con correo inválido",
             lambda: agregar_cliente(Cliente("C02", "Luis Pérez", "luis.correo.com", "3109876543")))
    ejecutar(3, "Registrar cliente sin nombre",
             lambda: agregar_cliente(Cliente("C03", None, "sin@correo.com", "3201112233")))

    # ----- SERVICIOS -----
    ejecutar(4, "Crear sala de reuniones válida",
             lambda: agregar_servicio(ReservaSala("S01", "Sala Ejecutiva", 50000, 10)))
    ejecutar(5, "Crear equipo con tarifa negativa",
             lambda: agregar_servicio(AlquilerEquipo("S09", "Portátil", -5000, 100000)))
    ejecutar(6, "Crear alquiler de equipo válido",
             lambda: agregar_servicio(AlquilerEquipo("S02", "Proyector", 15000, 50000)))
    ejecutar(7, "Crear asesoría especializada válida",
             lambda: agregar_servicio(AsesoriaEspecializada("S03", "Asesoría en Redes", 80000, "senior")))

    # ----- RESERVAS -----
    ejecutar(8, "Crear y confirmar reserva exitosa", reservar_y_confirmar)
    ejecutar(9, "Reservar un servicio no disponible",
             lambda: crear_reserva("R03", buscar(clientes, "C01"),
                                   AlquilerEquipo("S08", "Proyector HD", 15000, 50000, disponible=False),
                                   2).describir())
    ejecutar(10, "Cancelar dos veces la misma reserva", cancelar_dos_veces)

    # ----- COSTOS -----
    ejecutar(11, "Procesar reserva con descuento de 150 %",
             lambda: buscar(reservas, "R01").procesar(descuento=1.5))
    ejecutar(12, "Procesar reserva con IVA 19 % y descuento 10 %",
             lambda: buscar(reservas, "R01").procesar(impuesto=0.19, descuento=0.10))

    # ----- RESERVAS INVÁLIDAS -----
    ejecutar(13, "Reserva con duración de 0 horas",
             lambda: crear_reserva("R04", buscar(clientes, "C01"), buscar(servicios, "S01"), 0).describir())
    ejecutar(14, "Reserva con duración no numérica (excepción encadenada)",
             lambda: crear_reserva("R05", buscar(clientes, "C01"), buscar(servicios, "S01"), "abc").describir())

    # ----- RESUMEN FINAL -----
    print("\n========== RESUMEN ==========")
    print(f"Clientes registrados : {len(clientes)}")
    print(f"Servicios creados    : {len(servicios)}")
    print(f"Reservas creadas     : {len(reservas)}")
    for estado in EstadoReserva:
        total = sum(1 for r in reservas if r.estado == estado)
        print(f"   - {estado.value}: {total}")
    print("Revise el archivo logs/software_fj.log para ver todos los eventos y errores.")
    registrar_evento("=== Fin de la simulación de Software FJ ===")


if __name__ == "__main__":
    main()
