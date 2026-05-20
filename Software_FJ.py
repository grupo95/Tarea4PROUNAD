from abc import ABC, abstractmethod
from datetime import datetime

# ==========================
# ARCHIVO DE LOGS
# ==========================

def registrar_log(mensaje):
    with open("logs.txt", "a", encoding="utf-8") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")

# ==========================
# EXCEPCIONES PERSONALIZADAS
# ==========================

class ClienteError(Exception):
    pass

class ServicioError(Exception):
    pass

class ReservaError(Exception):
    pass

# ==========================
# CLASE ABSTRACTA PERSONA
# ==========================

class Persona(ABC):

    @abstractmethod
    def mostrar_informacion(self):
        pass

# ==========================
# CLASE CLIENTE
# ==========================

class Cliente(Persona):

    def __init__(self, nombre, correo):

        if not nombre.strip():
            raise ClienteError("El nombre no puede estar vacío")

        if "@" not in correo:
            raise ClienteError("Correo electrónico inválido")

        self.__nombre = nombre
        self.__correo = correo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def mostrar_informacion(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"

# ==========================
# CLASE ABSTRACTA SERVICIO
# ==========================

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        if tarifa <= 0:
            raise ServicioError("La tarifa debe ser positiva")

        self.nombre = nombre
        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass

# ==========================
# SERVICIO RESERVA DE SALAS
# ==========================

class ReservaSala(Servicio):

    def calcular_costo(self, horas, descuento=0):
        total = self.tarifa * horas
        return total - descuento

    def descripcion(self):
        return f"Servicio de reserva de salas - Tarifa: {self.tarifa}"

# ==========================
# SERVICIO ALQUILER EQUIPOS
# ==========================

class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas, impuesto=0.19):
        subtotal = self.tarifa * horas
        return subtotal + (subtotal * impuesto)

    def descripcion(self):
        return f"Servicio de alquiler de equipos - Tarifa: {self.tarifa}"

# ==========================
# SERVICIO ASESORÍA
# ==========================

class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas, adicional=50000):
        return (self.tarifa * horas) + adicional

    def descripcion(self):
        return f"Servicio de asesoría especializada - Tarifa: {self.tarifa}"

# ==========================
# CLASE RESERVA
# ==========================

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaError("La duración debe ser mayor que cero")

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def procesar(self):

        try:
            costo = self.servicio.calcular_costo(self.horas)
            self.confirmar()

            print("Reserva procesada correctamente")
            print(f"Cliente: {self.cliente.nombre}")
            print(f"Servicio: {self.servicio.nombre}")
            print(f"Costo total: {costo}")
            print(f"Estado: {self.estado}\n")

        except Exception as error:
            registrar_log(str(error))
            raise ReservaError("Error al procesar la reserva") from error

# ==========================
# SIMULACIÓN DE OPERACIONES
# ==========================

operaciones = []

try:
    cliente1 = Cliente("Carlos Pérez", "carlos@gmail.com")
    operaciones.append(cliente1)
except Exception as e:
    registrar_log(e)

try:
    cliente2 = Cliente("", "correo_invalido")
    operaciones.append(cliente2)
except Exception as e:
    registrar_log(e)

try:
    sala = ReservaSala("Sala VIP", 50000)
    equipo = AlquilerEquipo("Computador Gamer", 30000)
    asesoria = AsesoriaEspecializada("Asesoría Python", 80000)

except Exception as e:
    registrar_log(e)

try:
    reserva1 = Reserva(cliente1, sala, 3)
    reserva1.procesar()
except Exception as e:
    registrar_log(e)

try:
    reserva2 = Reserva(cliente1, equipo, -5)
    reserva2.procesar()
except Exception as e:
    registrar_log(e)

try:
    reserva3 = Reserva(cliente1, asesoria, 2)
    reserva3.procesar()
except Exception as e:
    registrar_log(e)

# Operaciones adicionales

for i in range(1, 6):

    try:
        reserva_extra = Reserva(cliente1, sala, i)
        reserva_extra.procesar()

    except Exception as e:
        registrar_log(e)

print("Sistema ejecutado correctamente")
