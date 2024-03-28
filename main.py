import threading
import datetime

class CuentaBancaria:
    def __init__(self, saldo_inicial=0):
        self.saldo = saldo_inicial
        self.movimientos = []
        self.lock = threading.Lock()

    def consignar(self, monto):
        with self.lock:
            self.saldo += monto
            self.movimientos.append(('Consignación', monto))

    def retirar(self, monto):
        with self.lock:
            if self.saldo >= monto:
                self.saldo -= monto
                self.movimientos.append(('Retiro', monto))
            else:
                print("Fondos insuficientes")

    def consultar_saldo(self):
        with self.lock:
            return self.saldo

    def consultar_movimientos(self):
        with self.lock:
            return self.movimientos

    def generar_extracto_mensual(self, mes, ano):
        with self.lock:
            movimientos_mes = []
            for movimiento in self.movimientos:
                fecha_movimiento = movimiento[0]
                if fecha_movimiento.month == mes and fecha_movimiento.year == ano:
                    movimientos_mes.append(movimiento)
            return movimientos_mes

class Cliente:
    def __init__(self, nombre, cuenta):
        self.nombre = nombre
        self.cuenta = cuenta

    def realizar_transaccion(self, tipo, monto):
        if tipo == 'Consignación':
            self.cuenta.consignar(monto)
        elif tipo == 'Retiro':
            self.cuenta.retirar(monto)

# Crear cuentas bancarias
cuenta_ahorros = CuentaBancaria()
cuenta_corriente = CuentaBancaria()

# Crear clientes
cliente1 = Cliente("Cliente A", cuenta_ahorros)
cliente2 = Cliente("Cliente B", cuenta_corriente)

# Realizar transacciones
cliente1.realizar_transaccion('Consignación', 1000)
cliente1.realizar_transaccion('Retiro', 500)
cliente2.realizar_transaccion('Consignación', 2000)

# Consultar saldo y movimientos
print(cliente1.cuenta.consultar_saldo())
print(cliente1.cuenta.consultar_movimientos())
