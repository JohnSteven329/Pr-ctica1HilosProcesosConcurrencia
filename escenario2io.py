import threading
import time


def tarea_io(numero):
    print(f"Tarea {numero}: iniciando I/O...")
    time.sleep(2)
    print(f"Tarea {numero}: I/O completada.")


if __name__ == "__main__":
    inicio = time.perf_counter()
    hilos = []

    for numero in range(1, 5):
        hilo = threading.Thread(target=tarea_io, args=(numero,))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    tiempo_total = time.perf_counter() - inicio
    print(f"\nTiempo total con hilos: {tiempo_total:.2f} segundos")
    print("Tiempo secuencial aproximado: 8.00 segundos")
