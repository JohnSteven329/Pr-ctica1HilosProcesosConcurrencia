import threading
import time

SALDO_INICIAL = 1000
NUM_CLIENTES = 10
MONTO_RETIRO = 100


class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo
        self.lock = threading.Lock()

    def retirar_sin_lock(self, cliente, monto):
        saldo_leido = self.saldo
        time.sleep(0.01)

        if saldo_leido >= monto:
            self.saldo = saldo_leido - monto
            print(f"{cliente} retiró ${monto}. Saldo: ${self.saldo}")
        else:
            print(f"{cliente}: fondos insuficientes.")

    def retirar_con_lock(self, cliente, monto):
        with self.lock:
            saldo_leido = self.saldo
            time.sleep(0.01)

            if saldo_leido >= monto:
                self.saldo = saldo_leido - monto
                print(f"{cliente} retiró ${monto}. Saldo: ${self.saldo}")
            else:
                print(f"{cliente}: fondos insuficientes.")


def ejecutar_prueba(usar_lock):
    cuenta = Cuenta(SALDO_INICIAL)
    metodo = cuenta.retirar_con_lock if usar_lock else cuenta.retirar_sin_lock
    hilos = []

    for numero in range(1, NUM_CLIENTES + 1):
        hilo = threading.Thread(
            target=metodo,
            args=(f"Cliente {numero}", MONTO_RETIRO)
        )
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return cuenta.saldo


if __name__ == "__main__":
    esperado = SALDO_INICIAL - NUM_CLIENTES * MONTO_RETIRO

    print("=== RETIROS SIN LOCK ===")
    saldo_sin_lock = ejecutar_prueba(False)
    print(f"Saldo esperado: ${esperado}")
    print(f"Saldo obtenido: ${saldo_sin_lock}")

    print("\n=== RETIROS CON LOCK ===")
    saldo_con_lock = ejecutar_prueba(True)
    print(f"Saldo esperado: ${esperado}")
    print(f"Saldo obtenido: ${saldo_con_lock}")
