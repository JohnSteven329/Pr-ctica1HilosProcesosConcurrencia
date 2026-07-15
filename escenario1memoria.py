import multiprocessing
import threading
import time

ITERACIONES = 10_000
contador = 0
lock = threading.Lock()


def incrementar_sin_lock():
    global contador

    for _ in range(ITERACIONES):
        valor = contador
        time.sleep(0)
        contador = valor + 1


def incrementar_con_lock():
    global contador

    for _ in range(ITERACIONES):
        with lock:
            contador += 1


def ejecutar_hilos(funcion):
    global contador
    contador = 0

    hilos = [
        threading.Thread(target=funcion),
        threading.Thread(target=funcion)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return contador


def incrementar_proceso(contador_local, cola):
    for _ in range(ITERACIONES):
        contador_local += 1

    cola.put(contador_local)


def ejecutar_procesos():
    global contador
    contador = 0
    cola = multiprocessing.Queue()

    procesos = [
        multiprocessing.Process(
            target=incrementar_proceso,
            args=(contador, cola)
        )
        for _ in range(2)
    ]

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()

    resultados_locales = [cola.get() for _ in procesos]
    return contador, resultados_locales


if __name__ == "__main__":
    esperado = ITERACIONES * 2

    sin_lock = ejecutar_hilos(incrementar_sin_lock)
    con_lock = ejecutar_hilos(incrementar_con_lock)
    global_procesos, copias = ejecutar_procesos()

    print("=== HILOS SIN LOCK ===")
    print(f"Esperado: {esperado}")
    print(f"Obtenido: {sin_lock}")

    print("\n=== HILOS CON LOCK ===")
    print(f"Esperado: {esperado}")
    print(f"Obtenido: {con_lock}")

    print("\n=== PROCESOS ===")
    print(f"Resultados de las copias: {copias}")
    print(f"Variable global original: {global_procesos}")
