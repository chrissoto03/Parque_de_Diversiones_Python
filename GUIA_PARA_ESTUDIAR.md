# Guía para estudiar y exponer el proyecto

## Orden recomendado para aprenderlo
1. **Nodo:** representa cada elemento. Tiene el dato y el enlace al siguiente nodo.
2. **Cola FIFO:** estudia `encolar`, `desencolar` y `obtener_visitantes`. La cola agrega al final y atiende desde el frente.
3. **Pila LIFO:** estudia `apilar`, `desapilar` y `obtener_reclamos`. La pila agrega y retira desde el tope.
4. **Tkinter:** la interfaz llama a los métodos de las estructuras cuando se presionan los botones.
5. **Recursividad:** estudia `dibujar_explosion`. Identifica la condición `nivel <= 0 or longitud < 4` como caso base y la llamada a la misma función como paso recursivo.

## Prueba para la demostración
- Agrega Ana, Luis y María a la fila. Atiende una vez: debe subir Ana.
- Registra tres reclamos. Deshaz uno: debe desaparecer el tercero, porque fue el último registrado.
- Abre Fuegos artificiales y presiona “LANZAR FUEGOS ARTIFICIALES”.

## Guion breve para explicar
“Este programa simula un día en un parque de diversiones. Utiliza una cola FIFO para respetar el orden de llegada de los visitantes, una pila LIFO para poder deshacer el último reclamo y una función recursiva para generar los fuegos artificiales. La cola y la pila están construidas con nodos enlazados, y la función recursiva tiene un caso base para detener las llamadas.”


## Cómo explicar las mejoras visuales
1. **Recursión y animación son tareas distintas.** `dibujar_explosion` construye el árbol llamándose directamente dos veces. Cada rama reduce su longitud y nivel, lo que garantiza que termina. `animar_fuegos` recorre las partículas para mostrar el estado de ese árbol en cada instante; ese recorrido no sustituye la recursión.
2. **Explosiones en cadena.** La madre avanza 0,48 segundos antes de que nazcan sus hijas en su posición. El movimiento usa `x = x0 + vx*t` e `y = y0 + vy*t + gravedad*t²/2`. En Canvas el eje vertical crece hacia abajo.
3. **Luz y desaparición.** Cada partícula tiene núcleo, halo y estela; su color se mezcla gradualmente con el fondo. Al terminar su vida se eliminan sus objetos gráficos.
4. **Interfaz disponible.** `after(33, ...)` solicita un cuadro aproximadamente cada 33 milisegundos. `perf_counter()` mide el tiempo real. No se usan pausas que congelen los botones.
5. **Tren sobre rieles.** `punto_pista` es la misma función para dibujar la pista y ubicar los vagones. Dos puntos cercanos permiten calcular la inclinación con `atan2`.
6. **Cabinas y pasajeros.** `dibujar_vagon` aplica rotación y escala a coordenadas locales. Se reutiliza en ambas atracciones. El seno produce el balanceo del martillo, y su amplitud aumenta al iniciar.
7. **Cierre y reinicio.** Se conserva un identificador por temporizador para cancelarlo. Repetir el show no acumula animaciones anteriores.

