# Parque de Diversiones 🎡

Proyecto académico de Estructuras de Datos desarrollado en Python con Tkinter.

## Requisitos
- Python 3 instalado.
- Tkinter (normalmente viene incluido con Python).

## Cómo ejecutar
1. Descargue o clone este repositorio.
2. Abra una terminal dentro de la carpeta del proyecto.
3. Ejecute:

```bash
python parque_diversiones.py
```

En algunos equipos Windows también puede funcionar:

```bash
py parque_diversiones.py
```

## ¿Qué incluye?
### 1. Cola FIFO — Montaña rusa
La clase `ColaVisitantes` utiliza nodos enlazados. `encolar()` agrega al final y `desencolar()` atiende desde el frente. Por eso, el primero que llega es el primero que sube.

### 2. Pila LIFO — Libro de reclamos
La clase `PilaReclamos` utiliza nodos enlazados. `apilar()` agrega en el tope y `desapilar()` retira el último reclamo registrado.

### 3. Recursividad — Fuegos artificiales
La función `dibujar_explosion()` se llama a sí misma dos veces para crear ramas hijas. Cada hija tiene el 55 % del tamaño y un nivel menos. El caso base es `nivel <= 0 or longitud < 4`. Las partículas tienen tiempos de nacimiento distintos: primero sube el cohete, después explota y finalmente aparecen las ramificaciones. `animar_fuegos()` muestra ese árbol con gravedad, estelas, halos y desvanecimiento mediante `after()`, sin bloquear la interfaz.

## Estructuras utilizadas
- Clase `Nodo`, con un dato y una referencia al siguiente nodo.
- Cola enlazada con referencias `frente` y `final`.
- Pila enlazada con referencia `tope`.
- Función recursiva con caso base.

**Nota:** no se utilizan `append()` ni `pop()` para implementar la cola o la pila. Los recorridos para mostrar los datos utilizan una lista auxiliar únicamente para alimentar la interfaz gráfica.


## Animaciones y cómo probarlas
- Fuegos artificiales: presione **LANZAR FUEGOS ARTIFICIALES**. El show dura unos 9 segundos. Puede repetirlo incluso mientras está activo: el anterior se cancela.
- Agregue un visitante y atiéndalo: disfrutará 20 segundos de montaña rusa y 20 de martillo. El tren sigue una pista cerrada y los vagones se inclinan con la pendiente; el martillo arranca suavemente y la cabina gira con el brazo.
- Cambie el tamaño de la ventana para comprobar cómo se adaptan las atracciones. Los fuegos toman las dimensiones al iniciar cada show; vuelva a lanzarlos para usar un tamaño nuevo.
- Cambie de pestaña durante las animaciones y cierre la ventana durante un show para comprobar que los temporizadores se cancelan.

No se requieren paquetes adicionales. Las listas de partículas pertenecen a la animación; la cola y la pila académicas siguen implementadas con nodos enlazados.

## Verificación automática
Ejecute `python verificar_animaciones.py` en un equipo con Tkinter y entorno gráfico disponible. Comprueba FIFO/LIFO, caso base y generaciones recursivas, el show completo, reinicio, dibujo de ambas atracciones en tres tamaños, transiciones y cierre. Usa una ventana oculta y tiempo simulado; no reemplaza la revisión visual del programa.
