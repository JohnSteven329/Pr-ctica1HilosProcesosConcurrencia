# Práctica: Procesos e hilos en Python

## Descripción

Esta práctica demuestra las diferencias entre procesos e hilos, el uso de memoria
compartida, las condiciones de carrera, los mecanismos de sincronización y el
rendimiento en tareas de entrada/salida y de uso intensivo del procesador.

También incluye una barra de progreso concurrente que muestra el avance de una
tarea en tiempo real.

## Objetivos de aprendizaje

- Comprender la diferencia entre procesos e hilos en cuanto al aislamiento de
  memoria y el acceso a recursos compartidos.
- Identificar y resolver condiciones de carrera mediante `threading.Lock`.
- Medir el rendimiento de hilos y procesos en tareas I/O-bound y CPU-bound.
- Implementar una barra de progreso concurrente.

## Requisitos

- Python 3.7 o superior.
- No se necesitan librerías externas.

Para comprobar la versión instalada:

```bash
python --version
```

En algunos sistemas se debe utilizar `python3` en lugar de `python`.

## Archivos del proyecto

| Archivo | Descripción |
|---|---|
| `cajeros.py` | Simula retiros concurrentes con y sin un cerrojo. |
| `escenario1_memoria.py` | Compara la memoria compartida de los hilos con el aislamiento de los procesos. |
| `escenario2_io.py` | Mide el rendimiento de los hilos en tareas I/O-bound. |
| `escenario3_cpu.py` | Compara hilos y procesos en una tarea CPU-bound. |
| `barra_progreso.py` | Muestra una barra de progreso desde el hilo principal. |

## Ejecución

Desde la carpeta del proyecto, ejecutar cada programa por separado:

```bash
python cajeros.py
python escenario1_memoria.py
python escenario2_io.py
python escenario3_cpu.py
python barra_progreso.py
```

## 1. Simulador de cajeros automáticos

El programa crea varios clientes representados por hilos. Todos intentan retirar
dinero de la misma cuenta.

### Prueba sin sincronización

Cada hilo lee el saldo, espera un momento y después escribe el nuevo valor.
Durante esa espera, otros hilos pueden leer el mismo saldo anterior. Esto causa
una condición de carrera y produce un saldo incorrecto.

### Prueba con sincronización

La instrucción `with self.lock:` permite que solamente un hilo consulte y
modifique el saldo a la vez. El resultado final coincide con el saldo esperado.

### Preguntas de reflexión

**¿Qué es una condición de carrera?**

Es una situación en la que varios hilos acceden y modifican simultáneamente un
recurso compartido. El resultado depende del orden de ejecución de los hilos.

**¿Cómo soluciona el problema un lock?**

El lock crea una sección crítica. Mientras un hilo tiene el cerrojo, los demás
deben esperar antes de modificar el mismo recurso.

**¿Qué ocurriría si el saldo se comprobara fuera del lock?**

Otro hilo podría cambiar el saldo después de la comprobación y antes del retiro.
Por esa razón, la comprobación y la modificación deben estar dentro del mismo
bloque protegido.

## 2. Escenario 1: aislamiento y memoria compartida

Los hilos de un mismo proceso comparten la variable global `contador`. Sin un
lock, las operaciones de lectura y escritura pueden intercalarse y perder
incrementos.

Cuando se utiliza un lock, el resultado debe ser exactamente `20000`.

Los procesos no comparten directamente la variable global. Cada proceso recibe
una copia inicial con valor cero, la incrementa hasta `10000` y conserva ese
resultado en su propio espacio de memoria. La variable del proceso principal
permanece en cero.

### Preguntas de reflexión

**¿Por qué los hilos pueden modificar la misma variable?**

Porque pertenecen al mismo proceso y comparten su espacio de memoria.

**¿Por qué la variable global no cambia al usar procesos?**

Porque cada proceso posee un espacio de memoria independiente. Los argumentos
recibidos son copias, no referencias directas a la memoria del proceso principal.

**¿Cómo se podrían compartir datos entre procesos?**

Se pueden utilizar herramientas de `multiprocessing`, como `Queue`, `Pipe`,
`Value`, `Array` o `Manager`.

## 3. Escenario 2: tareas I/O-bound

Cada hilo simula una operación de red o disco mediante `time.sleep(2)`. Las
cuatro tareas comienzan casi al mismo tiempo, por lo que el tiempo total debe ser
cercano a dos segundos.

Si se ejecutaran secuencialmente, tardarían aproximadamente ocho segundos.

### Preguntas de reflexión

**¿Por qué los hilos mejoran el tiempo de ejecución?**

Mientras un hilo espera una operación de entrada/salida, el sistema operativo
puede ejecutar otro hilo.

**¿En qué tareas conviene utilizar hilos?**

En solicitudes de red, lectura y escritura de archivos, consultas a bases de
datos y otras operaciones que pasan tiempo esperando recursos externos.

**¿Las tareas se ejecutan necesariamente en el mismo orden?**

No. El planificador del sistema operativo decide cuándo se ejecuta cada hilo.

## 4. Escenario 3: tareas CPU-bound y GIL

Los dos hilos realizan cálculos matemáticos intensivos. En una instalación
tradicional de CPython, el Global Interpreter Lock limita la ejecución
simultánea de código Python en varios hilos.

Los procesos poseen intérpretes independientes y pueden utilizar diferentes
núcleos del procesador. Por esta razón, normalmente son más rápidos para tareas
CPU-bound.

Los tiempos exactos dependen del procesador, la cantidad de núcleos, el sistema
operativo y los programas que estén ejecutándose.

### Preguntas de reflexión

**¿Qué es el GIL?**

Es un mecanismo de CPython que permite que un solo hilo ejecute bytecode de
Python a la vez dentro de un proceso.

**¿Por qué los procesos pueden ser más rápidos?**

Cada proceso tiene su propio intérprete y su propio GIL. Así pueden trabajar
simultáneamente en varios núcleos.

**¿Por qué los procesos también tienen un costo?**

Crear procesos y transferir información entre ellos consume más memoria y
tiempo que crear hilos.

## 5. Barra de progreso concurrente

El hilo secundario simula la tarea y envía porcentajes mediante una `Queue`.
El hilo principal recibe los valores y actualiza la consola.

La cola evita que ambos hilos escriban o lean datos compartidos sin control.
El valor `("finalizado", None)` indica que la tarea terminó.

### Preguntas de reflexión

**¿Por qué se utiliza una cola?**

La cola es una forma segura de comunicar datos entre hilos. Evita revisar
constantemente una variable compartida sin sincronización.

**¿Por qué la barra se dibuja con `\r`?**

El carácter `\r` mueve el cursor al inicio de la misma línea, permitiendo
actualizar la barra sin imprimir una línea nueva en cada porcentaje.

**¿Qué función cumple `join()`?**

Hace que el hilo principal espere a que el hilo secundario termine antes de
cerrar el programa.

## Conclusiones

Los hilos comparten memoria y son adecuados para tareas que esperan operaciones
de entrada/salida. Sin embargo, el acceso concurrente a variables compartidas
puede generar condiciones de carrera, por lo que deben utilizarse mecanismos de
sincronización.

Los procesos tienen memoria aislada y un mayor costo de creación, pero permiten
aprovechar varios núcleos en tareas intensivas de CPU. La elección entre procesos
e hilos depende del tipo de trabajo que se necesita realizar.

## Presentación en vivo

Durante la presentación se recomienda ejecutar primero:

```bash
python barra_progreso.py
```

Después se puede mostrar `cajeros.py` para explicar visualmente la diferencia
entre ejecutar retiros sin lock y con lock.

## Publicación en GitHub

Crear un repositorio vacío en GitHub y ejecutar:

```bash
git init
git add .
git commit -m "Completar práctica de procesos e hilos"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Reemplazar `URL_DEL_REPOSITORIO` por la dirección del repositorio creado.
