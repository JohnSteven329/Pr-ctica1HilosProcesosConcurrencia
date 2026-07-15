import math
import multiprocessing
import os
import threading
import time

ITERACIONES = 10_000_000


def tarea_cpu(cantidad):
    resultado = 0.0

    for numero in range(1, cantidad):
        resultado += math.sqrt(numero)

    return resultado


def medir_hilos():
    inicio = time.perf_counter()

    hilos = [
        threading.Thread(target=tarea_cpu, args=(ITERACIONES,))
        for _ in range(2)
    ]

    for hilo in hilos:
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return time.perf_counter() - inicio


def medir_procesos():
    inicio = time.perf_counter()

    procesos = [
        multiprocessing.Process(target=tarea_cpu, args=(ITERACIONES,))
        for _ in range(2)
    ]

    for proceso in procesos:
        proceso.start()

    for proceso in procesos:
        proceso.join()

    return time.perf_counter() - inicio


if __name__ == "__main__":
    tiempo_hilos = medir_hilos()
    tiempo_procesos = medir_procesos()

    print(f"Núcleos disponibles: {os.cpu_count()}")
    print(f"Tiempo con hilos: {tiempo_hilos:.2f} segundos")
    print(f"Tiempo con procesos: {tiempo_procesos:.2f} segundos")

    if tiempo_procesos < tiempo_hilos:
        print("Los procesos fueron más rápidos en esta ejecución.")
    else:
        print("Los resultados pueden variar según el equipo y su carga.")
