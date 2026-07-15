import threading
import queue
import time
import sys

def realizar_tarea(cola):
    for progreso in range(1, 101):
        time.sleep(0.05)
        cola.put(progreso)
    cola.put(None)

def mostrar_barra(progreso, longitud=40):
    completado = int(longitud * progreso / 100)
    restante = longitud - completado
    barra = "█" * completado
    espacios = "-" * restante
    sys.stdout.write(f"\rProgreso: [{barra}{espacios}] {progreso}%")
    sys.stdout.flush()

def main():
    print("Iniciando actividad...\n")
    cola = queue.Queue()
    hilo = threading.Thread(
        target=realizar_tarea,
        args=(cola,)
    )
    hilo.start()

    while True:
        progreso = cola.get()
        if progreso is None:
            break
        mostrar_barra(progreso)

    hilo.join()
    print("\n\nActividad terminada correctamente.")

if __name__ == "__main__":
    main()