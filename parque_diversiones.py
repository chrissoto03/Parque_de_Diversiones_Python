import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import time


# =====================================================
# CLASE NODO
# =====================================================

class Nodo:
    # Un nodo guarda un dato y el enlace al siguiente. Cola y pila comparten
    # esta pieza, pero conectan y retiran sus nodos en posiciones diferentes.
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


# =====================================================
# COLA FIFO - VISITANTES
# =====================================================

class ColaVisitantes:

    def __init__(self):
        self.frente = None
        self.final = None
        self.cantidad = 0

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, visitante):
        # FIFO: insertar al final conserva el orden de llegada. Si estaba
        # vacía, el nuevo nodo es simultáneamente el frente y el final.
        nuevo = Nodo(visitante)

        if self.esta_vacia():
            self.frente = nuevo
            self.final = nuevo
        else:
            self.final.siguiente = nuevo
            self.final = nuevo

        self.cantidad += 1

    def desencolar(self):
        # Retiramos el frente y avanzamos su referencia al siguiente nodo.
        # Cuando sale el último visitante también debemos limpiar el final.
        if self.esta_vacia():
            return None

        visitante = self.frente.dato
        self.frente = self.frente.siguiente

        if self.frente is None:
            self.final = None

        self.cantidad -= 1
        return visitante

    def obtener_visitantes(self):
        # Recorremos enlaces sin retirar visitantes; la lista resultante solo
        # sirve para mostrar la fila en pantalla, no implementa la cola.
        resultado = []
        actual = self.frente

        while actual is not None:
            resultado += [actual.dato]
            actual = actual.siguiente

        return resultado


# =====================================================
# PILA LIFO - RECLAMOS
# =====================================================

class PilaReclamos:

    def __init__(self):
        self.tope = None
        self.cantidad = 0

    def esta_vacia(self):
        return self.tope is None

    def apilar(self, reclamo):
        # LIFO: el nuevo nodo apunta al antiguo tope y se convierte en el tope.
        nuevo = Nodo(reclamo)
        nuevo.siguiente = self.tope
        self.tope = nuevo
        self.cantidad += 1

    def desapilar(self):
        # Deshacer consiste en retirar el tope: siempre es el último agregado.
        if self.esta_vacia():
            return None

        reclamo = self.tope.dato
        self.tope = self.tope.siguiente
        self.cantidad -= 1

        return reclamo

    def obtener_reclamos(self):
        # Consultamos desde el más reciente hasta el más antiguo sin modificar
        # la pila; así mostrar el historial no equivale a deshacer reclamos.
        resultado = []
        actual = self.tope

        while actual is not None:
            resultado += [actual.dato]
            actual = actual.siguiente

        return resultado


# =====================================================
# APLICACIÓN PRINCIPAL
# =====================================================

class ParqueDiversiones:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("Parque de Diversiones")
        self.ventana.geometry("1100x760")
        self.ventana.minsize(850, 650)
        self.ventana.configure(bg="#101827")

        # Estructuras de datos
        self.cola = ColaVisitantes()
        self.pila = PilaReclamos()

        # Estadísticas
        self.total_atendidos = 0
        self.total_reclamos = 0

        # Control de clientes y atracciones
        self.visitante_actual = None
        self.tipo_atraccion = None
        self.fase = 0

        # Control de animaciones y tiempos
        self.animacion_id = None
        # Un solo temporizador controla el show; se cancela al repetir o cerrar.
        self.fuegos_id = None
        self.particulas = []
        self.transicion_id = None
        self.tiempo_restante = 20

        # Colores
        self.fondo = "#101827"
        self.panel = "#1D293B"
        self.azul = "#2563EB"
        self.verde = "#16A34A"
        self.rojo = "#DC2626"
        self.blanco = "#FFFFFF"
        self.gris = "#CBD5E1"

        self.crear_interfaz()

        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_programa
        )

    # =================================================
    # INTERFAZ PRINCIPAL
    # =================================================

    def crear_interfaz(self):
        # Los Frame agrupan controles, los Label muestran texto y los Button
        # ejecutan el método indicado en command al hacer clic. El Notebook
        # separa visitantes, reclamos, fuegos y atracciones en pestañas.

        encabezado = tk.Frame(
            self.ventana,
            bg="#172554",
            height=110
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="🎡 PARQUE DE DIVERSIONES",
            font=("Arial", 25, "bold"),
            bg="#172554",
            fg="white"
        ).pack(pady=(15, 5))

        tk.Label(
            encabezado,
            text="Sistema de administración y entretenimiento",
            font=("Arial", 11),
            bg="#172554",
            fg="#BFDBFE"
        ).pack()

        # Estadísticas
        estadisticas = tk.Frame(
            self.ventana,
            bg=self.fondo
        )
        estadisticas.pack(fill="x", padx=15, pady=12)

        self.lbl_visitantes = tk.Label(
            estadisticas,
            text="Visitantes en espera: 0",
            bg=self.panel,
            fg=self.blanco,
            font=("Arial", 11, "bold"),
            padx=12,
            pady=12
        )
        self.lbl_visitantes.pack(side="left", padx=4)

        self.lbl_atendidos = tk.Label(
            estadisticas,
            text="Visitantes atendidos: 0",
            bg=self.panel,
            fg=self.blanco,
            font=("Arial", 11, "bold"),
            padx=12,
            pady=12
        )
        self.lbl_atendidos.pack(side="left", padx=4)

        self.lbl_reclamos = tk.Label(
            estadisticas,
            text="Reclamos: 0",
            bg=self.panel,
            fg=self.blanco,
            font=("Arial", 11, "bold"),
            padx=12,
            pady=12
        )
        self.lbl_reclamos.pack(side="left", padx=4)

        # Estilo de pestañas
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TNotebook",
            background=self.fondo,
            borderwidth=0
        )

        estilo.configure(
            "TNotebook.Tab",
            padding=[15, 10],
            font=("Arial", 10, "bold")
        )

        self.pestanas = ttk.Notebook(self.ventana)
        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )

        # Pestañas
        self.tab_montana = tk.Frame(
            self.pestanas,
            bg=self.fondo
        )

        self.tab_reclamos = tk.Frame(
            self.pestanas,
            bg=self.fondo
        )

        self.tab_fuegos = tk.Frame(
            self.pestanas,
            bg=self.fondo
        )

        self.tab_atracciones = tk.Frame(
            self.pestanas,
            bg=self.fondo
        )

        self.pestanas.add(
            self.tab_montana,
            text="🎟 Visitantes"
        )

        self.pestanas.add(
            self.tab_reclamos,
            text="📋 Reclamos"
        )

        self.pestanas.add(
            self.tab_fuegos,
            text="🎆 Fuegos artificiales"
        )

        self.pestanas.add(
            self.tab_atracciones,
            text="🎠 Atracciones"
        )

        self.crear_tab_montana()
        self.crear_tab_reclamos()
        self.crear_tab_fuegos()
        self.crear_tab_atracciones()

        tk.Label(
            self.ventana,
            text="Proyecto académico de estructuras de datos - Python",
            bg=self.fondo,
            fg="#94A3B8",
            font=("Arial", 9)
        ).pack(pady=6)

    # =================================================
    # MÓDULO 1: VISITANTES - COLA FIFO
    # =================================================

    def crear_tab_montana(self):

        tk.Label(
            self.tab_montana,
            text="🎢 ADMINISTRACIÓN DE VISITANTES",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 19, "bold")
        ).pack(pady=20)

        tk.Label(
            self.tab_montana,
            text="Los visitantes ingresan según su orden de llegada (FIFO).",
            bg=self.fondo,
            fg=self.gris,
            font=("Arial", 11)
        ).pack()

        formulario = tk.Frame(
            self.tab_montana,
            bg=self.panel,
            padx=20,
            pady=20
        )
        formulario.pack(
            padx=30,
            pady=20,
            fill="x"
        )

        tk.Label(
            formulario,
            text="Nombre del visitante:",
            bg=self.panel,
            fg=self.blanco,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        self.entrada_visitante = tk.Entry(
            formulario,
            font=("Arial", 13)
        )
        self.entrada_visitante.pack(
            fill="x",
            pady=10,
            ipady=7
        )

        botones = tk.Frame(
            formulario,
            bg=self.panel
        )
        botones.pack(fill="x")

        tk.Button(
            botones,
            text="➕ Agregar visitante",
            bg=self.verde,
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.agregar_visitante
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="🎢 Atender visitante",
            bg=self.azul,
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.atender_visitante
        ).pack(side="left", padx=5)

        tk.Label(
            self.tab_montana,
            text="Fila de visitantes",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.lista_visitantes = tk.Listbox(
            self.tab_montana,
            font=("Arial", 12),
            bg="#F1F5F9",
            fg="#1E293B",
            height=10
        )
        self.lista_visitantes.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.actualizar_visitantes()

    def agregar_visitante(self):

        nombre = self.entrada_visitante.get().strip()

        if not nombre:
            messagebox.showwarning(
                "Atención",
                "Ingrese el nombre del visitante."
            )
            return

        self.cola.encolar(nombre)
        self.entrada_visitante.delete(0, tk.END)

        self.actualizar_visitantes()

        messagebox.showinfo(
            "Visitante agregado",
            nombre + " fue agregado a la fila."
        )

    def atender_visitante(self):

        # No permitir atender a otro mientras alguien juega
        if self.visitante_actual is not None:
            messagebox.showwarning(
                "Atracción ocupada",
                self.visitante_actual +
                " todavía está disfrutando las atracciones."
            )
            return

        visitante = self.cola.desencolar()

        if visitante is None:
            messagebox.showwarning(
                "Fila vacía",
                "No hay visitantes esperando."
            )
            return

        self.total_atendidos += 1
        self.visitante_actual = visitante

        self.actualizar_visitantes()

        # Comienza automáticamente el recorrido
        self.iniciar_atraccion("Montaña rusa")

    def actualizar_visitantes(self):
        # Refresca la representación visual después de modificar la cola.
        # Los datos reales permanecen en los nodos, no en el Listbox.

        self.lista_visitantes.delete(0, tk.END)

        visitantes = self.cola.obtener_visitantes()

        for posicion, visitante in enumerate(
            visitantes,
            start=1
        ):
            self.lista_visitantes.insert(
                tk.END,
                str(posicion) + ". " + visitante
            )

        self.lbl_visitantes.config(
            text="Visitantes en espera: " + str(self.cola.cantidad)
        )

        self.lbl_atendidos.config(
            text="Visitantes atendidos: " + str(self.total_atendidos)
        )

    # =================================================
    # MÓDULO 2: RECLAMOS - PILA LIFO
    # =================================================

    def crear_tab_reclamos(self):

        tk.Label(
            self.tab_reclamos,
            text="📋 SISTEMA DE RECLAMOS",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 19, "bold")
        ).pack(pady=20)

        tk.Label(
            self.tab_reclamos,
            text="El último reclamo registrado será el primero en salir (LIFO).",
            bg=self.fondo,
            fg=self.gris,
            font=("Arial", 11)
        ).pack()

        formulario = tk.Frame(
            self.tab_reclamos,
            bg=self.panel,
            padx=20,
            pady=20
        )
        formulario.pack(
            padx=30,
            pady=20,
            fill="x"
        )

        tk.Label(
            formulario,
            text="Descripción del reclamo:",
            bg=self.panel,
            fg=self.blanco,
            font=("Arial", 11, "bold")
        ).pack(anchor="w")

        self.entrada_reclamo = tk.Entry(
            formulario,
            font=("Arial", 12)
        )
        self.entrada_reclamo.pack(
            fill="x",
            pady=10,
            ipady=7
        )

        botones = tk.Frame(
            formulario,
            bg=self.panel
        )
        botones.pack(fill="x")

        tk.Button(
            botones,
            text="➕ Registrar reclamo",
            bg=self.verde,
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.registrar_reclamo
        ).pack(side="left", padx=5)

        tk.Button(
            botones,
            text="↩ Deshacer último reclamo",
            bg=self.rojo,
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.deshacer_reclamo
        ).pack(side="left", padx=5)

        tk.Label(
            self.tab_reclamos,
            text="Historial de reclamos (último primero)",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.lista_reclamos = tk.Listbox(
            self.tab_reclamos,
            font=("Arial", 12),
            bg="#F1F5F9",
            fg="#1E293B",
            height=10
        )
        self.lista_reclamos.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        self.actualizar_reclamos()

    def registrar_reclamo(self):

        reclamo = self.entrada_reclamo.get().strip()

        if not reclamo:
            messagebox.showwarning(
                "Atención",
                "Escriba una descripción del reclamo."
            )
            return

        self.pila.apilar(reclamo)
        self.total_reclamos += 1

        self.entrada_reclamo.delete(0, tk.END)

        self.actualizar_reclamos()

        messagebox.showinfo(
            "Reclamo registrado",
            "El reclamo fue registrado correctamente."
        )

    def deshacer_reclamo(self):

        reclamo = self.pila.desapilar()

        if reclamo is None:
            messagebox.showwarning(
                "Pila vacía",
                "No existen reclamos para deshacer."
            )
            return

        self.actualizar_reclamos()

        messagebox.showinfo(
            "Reclamo deshecho",
            "Se eliminó el último reclamo:\n" + reclamo
        )

    def actualizar_reclamos(self):
        # Reconstruye el historial visible y muestra cuántos reclamos siguen
        # vigentes, descontando los que el usuario haya deshecho.

        self.lista_reclamos.delete(0, tk.END)

        reclamos = self.pila.obtener_reclamos()

        for posicion, reclamo in enumerate(
            reclamos,
            start=1
        ):
            self.lista_reclamos.insert(
                tk.END,
                str(posicion) + ". " + reclamo
            )

        self.lbl_reclamos.config(
            text="Reclamos: " + str(self.pila.cantidad)
        )

    # =================================================
    # MÓDULO 3: FUEGOS ARTIFICIALES
    # =================================================

    def crear_tab_fuegos(self):

        tk.Label(
            self.tab_fuegos,
            text="🎆 ESPECTÁCULO DE FUEGOS ARTIFICIALES",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        tk.Label(
            self.tab_fuegos,
            text="Generación de explosiones mediante recursividad.",
            bg=self.fondo,
            fg=self.gris,
            font=("Arial", 11)
        ).pack()

        self.lienzo = tk.Canvas(
            self.tab_fuegos,
            bg="#080D1B",
            height=350,
            highlightthickness=0
        )
        self.lienzo.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=15
        )

        self.lienzo.create_text(
            400,
            150,
            text="¡Bienvenidos al espectáculo!",
            fill="white",
            font=("Arial", 19, "bold")
        )

        tk.Button(
            self.tab_fuegos,
            text="🎆 LANZAR FUEGOS ARTIFICIALES",
            bg="#9333EA",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=20,
            pady=12,
            command=self.lanzar_fuegos
        ).pack(pady=10)

    def lanzar_fuegos(self):
        """Construye el árbol recursivo y luego reproduce sus nacimientos."""
        # Reiniciar elimina tanto el temporizador anterior como sus dibujos
        # y partículas, para que dos espectáculos no se superpongan.
        if self.fuegos_id is not None:
            self.ventana.after_cancel(self.fuegos_id)
            self.fuegos_id = None
        self.lienzo.delete("all")
        self.particulas = []
        ancho = max(200, self.lienzo.winfo_width())
        alto = max(180, self.lienzo.winfo_height())
        # Cielo fijo: las estrellas no cambian aleatoriamente en cada cuadro.
        for _ in range(65):
            x, y = random.uniform(0, ancho), random.uniform(0, alto * .85)
            self.lienzo.create_oval(x, y, x+2, y+2, fill="#536382", outline="")
        for i in range(18):
            x = i * ancho / 18
            techo = alto - random.uniform(15, 42)
            self.lienzo.create_rectangle(x, techo, x+ancho/18, alto,
                                         fill="#111b30", outline="")
        colores = ["#FF6699", "#FFD166", "#66E9FF", "#C69BFF", "#8DFFBC"]
        for i in range(7):
            # Cada cohete despega 0,85 segundos después del anterior.
            # inicio y nacimiento son segundos relativos al comienzo del show.
            x = ancho * (.23 + .54 * random.random())
            y = alto * (.23 + .19 * random.random())
            inicio = i * .85
            # El cohete llega al punto exacto donde nacen las ramas principales.
            self.crear_particula(x, alto-20, (x-ancho/2)*.08,
                                 (y-(alto-20)-18)/1.1, inicio, 1.1,
                                 "#FFE9B0", 2.5, gravedad=36/1.21)
            cohete = self.particulas[-1]
            origen_x = x + cohete["vx"] * 1.1
            escala = min(ancho * .10, alto * .18)
            giro = random.uniform(0, math.tau)
            for rayo in range(12):
                # El círculo tiene 2*pi radianes (math.tau). Lo dividimos en
                # 12 direcciones. Este for inicia 12 árboles independientes;
                # la recursión ocurre DENTRO de dibujar_explosion.
                self.dibujar_explosion(origen_x, y, escala,
                                      giro+rayo*math.tau/12, 3,
                                      colores[i % len(colores)], inicio+1.1)
        self.inicio_fuegos = time.perf_counter()
        self.animar_fuegos()

    def crear_particula(self, x, y, vx, vy, nacimiento, vida, color,
                        radio, gravedad=48):
        # x/y: origen; vx/vy: velocidad en píxeles por segundo; vida: segundos
        # visibles; nacimiento: momento de aparición; radio: tamaño del núcleo.
        # objetos=None significa que todavía no se crearon las figuras.
        # Cada partícula reutiliza tres objetos del Canvas: halo, estela y núcleo.
        # No usamos un after por rama: así el trabajo pendiente queda acotado.
        self.particulas.append(dict(x=x, y=y, vx=vx, vy=vy,
                                    nacimiento=nacimiento, vida=vida,
                                    color=color, radio=radio, gravedad=gravedad,
                                    objetos=None))

    def dibujar_explosion(self, x, y, longitud, angulo, nivel, color,
                         nacimiento=0):
        """Recursión real: una chispa produce dos hijas más pequeñas."""
        # Esta función prepara los datos: no espera ni dibuja toda la explosión
        # de inmediato. animar_fuegos mostrará cada chispa cuando le corresponda.
        # longitud controla la distancia de la rama; angulo su dirección en
        # radianes; nivel limita cuántas generaciones quedan por generar.
        # CASO BASE: sin tamaño o profundidad suficiente no creamos más hijas.
        # return termina ESTA llamada y vuelve a la que la invocó. No detiene
        # las otras ramas ni borra las partículas que ya se habían creado.
        if nivel <= 0 or longitud < 4:
            return
        duracion = .48
        # PASO 1: registrar la chispa madre. Seno y coseno convierten la
        # dirección angular en velocidades horizontal y vertical.
        vx = longitud * math.cos(angulo) / duracion
        vy = longitud * math.sin(angulo) / duracion
        self.crear_particula(x, y, vx, vy, nacimiento, .85, color, nivel*.75)
        # Las hijas nacen después, en la posición que alcanzó su madre,
        # incluida la caída por gravedad: no aparecen separadas de su estela.
        nuevo_x = x + vx * duracion
        nuevo_y = y + vy * duracion + .5 * 48 * duracion**2
        # PASO 2 (RECURSIVO): la misma función se llama con un problema menor.
        # La primera hija se desvía -0,48 radianes y la segunda +0,48.
        # Ambas recorren el 55 % de la longitud y reciben un nivel menos.
        # Reducir nivel garantiza llegar al caso base y evita recursión infinita.
        # nacimiento+duracion programa su aparición 0,48 segundos más tarde;
        # no es una pausa: el árbol completo se calcula antes de animarlo.
        self.dibujar_explosion(nuevo_x, nuevo_y, longitud*.55,
                               angulo-.48, nivel-1, color, nacimiento+duracion)
        self.dibujar_explosion(nuevo_x, nuevo_y, longitud*.55,
                               angulo+.48, nivel-1, color, nacimiento+duracion)
        # Ejemplo con nivel=3 y longitud suficiente: 1 madre -> 2 hijas ->
        # 4 nietas = 7 partículas. Las llamadas con nivel=0 regresan sin crear
        # partículas. Python termina la primera rama antes de visitar la otra;
        # sus tiempos de nacimiento permiten mostrarlas juntas en pantalla.

    @staticmethod
    def color_atenuado(color, intensidad, fondo="#080D1B"):
        # Tkinter no tiene alfa para estas figuras; interpolar hacia el fondo
        # simula el desvanecimiento sin añadir dependencias externas.
        intensidad = max(0, min(1, intensidad))
        canales = [round(int(fondo[i:i+2], 16)*(1-intensidad) +
                         int(color[i:i+2], 16)*intensidad) for i in (1, 3, 5)]
        return "#" + "".join(f"{c:02x}" for c in canales)

    def animar_fuegos(self):
        # Este bucle reproduce el árbol ya construido; no es la recursividad
        # del ejercicio. La recursión está en las dos llamadas del método anterior.
        self.fuegos_id = None
        tiempo = time.perf_counter() - self.inicio_fuegos
        pendientes = []
        for p in self.particulas:
            edad = tiempo - p["nacimiento"]
            # Una edad negativa indica que todavía no nace. Si supera su vida,
            # borramos sus figuras y dejamos de conservarla en pendientes.
            if edad >= p["vida"]:
                if p["objetos"]:
                    for objeto in p["objetos"]:
                        self.lienzo.delete(objeto)
                continue
            pendientes.append(p)
            if edad < 0:
                continue
            if p["objetos"] is None:
                p["objetos"] = (
                    self.lienzo.create_oval(0, 0, 0, 0, outline=""),
                    self.lienzo.create_line(0, 0, 0, 0, width=2, capstyle=tk.ROUND),
                    self.lienzo.create_oval(0, 0, 0, 0, outline=""))
            brillo = (1-edad/p["vida"])**.65
            # Movimiento con gravedad: Canvas aumenta Y hacia abajo, por eso
            # la gravedad positiva hace caer las chispas. El brillo disminuye.
            x = p["x"] + p["vx"]*edad
            y = p["y"] + p["vy"]*edad + .5*p["gravedad"]*edad**2
            anterior = max(0, edad-.12)
            # La estela une la posición de hace 0,12 segundos con la actual.
            tx = p["x"] + p["vx"]*anterior
            ty = p["y"] + p["vy"]*anterior + .5*p["gravedad"]*anterior**2
            halo, estela, nucleo = p["objetos"]
            radio = max(.5, p["radio"]*brillo)
            self.lienzo.coords(halo, x-radio*3, y-radio*3, x+radio*3, y+radio*3)
            self.lienzo.itemconfig(halo, fill=self.color_atenuado(p["color"], brillo*.18))
            self.lienzo.coords(estela, tx, ty, x, y)
            self.lienzo.itemconfig(estela, fill=self.color_atenuado(p["color"], brillo*.65))
            self.lienzo.coords(nucleo, x-radio, y-radio, x+radio, y+radio)
            self.lienzo.itemconfig(nucleo, fill=self.color_atenuado(p["color"], brillo))
        self.particulas = pendientes
        if pendientes:
            # after devuelve el control a Tkinter y solicita otro cuadro.
            # No es una llamada recursiva directa: Tkinter lo ejecutará después,
            # cuando esta ejecución ya haya terminado, sin apilar llamadas.
            self.fuegos_id = self.ventana.after(33, self.animar_fuegos)
        else:
            self.lienzo.create_text(self.lienzo.winfo_width()/2,
                                    self.lienzo.winfo_height()/2,
                                    text="¡Gracias por iluminar el parque!", fill="#FFE9B0",
                                    font=("Arial", 18, "bold"))


    def crear_tab_atracciones(self):

        tk.Label(
            self.tab_atracciones,
            text="🎠 ZONA DE ATRACCIONES",
            bg=self.fondo,
            fg=self.blanco,
            font=("Arial", 21, "bold")
        ).pack(pady=15)

        self.lbl_jugador = tk.Label(
            self.tab_atracciones,
            text="Esperando un visitante...",
            bg=self.fondo,
            fg="#FACC15",
            font=("Arial", 15, "bold")
        )
        self.lbl_jugador.pack(pady=5)

        self.lbl_estado_juego = tk.Label(
            self.tab_atracciones,
            text="El cliente disfrutará dos atracciones.",
            bg=self.fondo,
            fg="white",
            font=("Arial", 11)
        )
        self.lbl_estado_juego.pack(pady=5)

        self.lbl_tiempo = tk.Label(
            self.tab_atracciones,
            text="Tiempo restante: --",
            bg=self.fondo,
            fg="#FACC15",
            font=("Arial", 13, "bold")
        )
        self.lbl_tiempo.pack(pady=5)

        self.canvas_juegos = tk.Canvas(
            self.tab_atracciones,
            bg="#87CEEB",
            height=370,
            highlightthickness=0
        )
        self.canvas_juegos.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=15
        )

        self.canvas_juegos.create_text(
            375,
            150,
            text="¡Bienvenidos al parque!",
            fill="white",
            font=("Arial", 22, "bold")
        )

        tk.Label(
            self.tab_atracciones,
            text="Recorrido automático: Montaña rusa → Martillo mecánico → Finalización",
            bg=self.fondo,
            fg=self.gris,
            font=("Arial", 10)
        ).pack(pady=5)

    # =================================================
    # INICIAR ATRACCIÓN
    # =================================================

    def iniciar_atraccion(self, tipo):

        if self.visitante_actual is None:
            return

        self.tipo_atraccion = tipo
        self.fase = 0
        self.tiempo_restante = 20
        self.inicio_atraccion = time.perf_counter()

        self.pestanas.select(self.tab_atracciones)

        self.lbl_jugador.config(
            text="🎟 Cliente jugando: " + self.visitante_actual
        )

        self.lbl_estado_juego.config(
            text="¡Está disfrutando de " + tipo + "!"
        )

        self.lbl_tiempo.config(
            text="Tiempo restante: 20 segundos"
        )

        # Cancelar animación anterior
        if self.animacion_id is not None:
            self.ventana.after_cancel(self.animacion_id)
            self.animacion_id = None

        # Cancelar temporizador anterior
        if self.transicion_id is not None:
            self.ventana.after_cancel(self.transicion_id)
            self.transicion_id = None

        # Iniciar dibujo animado
        self.animar_atraccion()

        # Iniciar contador de 20 segundos
        self.contar_tiempo()

    # =================================================
    # CONTADOR DE TIEMPO
    # =================================================

    def contar_tiempo(self):
        # El contador se actualiza una vez por segundo, independientemente
        # de los cuadros de animación. Al llegar a cero cambia de atracción.

        self.lbl_tiempo.config(
            text="Tiempo restante: " +
            str(self.tiempo_restante) +
            " segundos"
        )

        if self.tiempo_restante > 0:

            self.tiempo_restante -= 1

            self.transicion_id = self.ventana.after(
                1000,
                self.contar_tiempo
            )

        else:

            self.transicion_id = None

            self.siguiente_atraccion()

    # =================================================
    # SIGUIENTE ATRACCIÓN
    # =================================================

    def siguiente_atraccion(self):

        if self.visitante_actual is None:
            return

        # Detener animación anterior
        if self.animacion_id is not None:

            self.ventana.after_cancel(
                self.animacion_id
            )

            self.animacion_id = None

        # Primera atracción: montaña rusa
        if self.tipo_atraccion == "Montaña rusa":

            self.iniciar_atraccion("Martillo")

        # Segunda atracción: finalizar recorrido
        elif self.tipo_atraccion == "Martillo":

            self.finalizar_recorrido()

    # =================================================
    # FINALIZAR RECORRIDO
    # =================================================

    def finalizar_recorrido(self):

        if self.animacion_id is not None:

            self.ventana.after_cancel(
                self.animacion_id
            )

            self.animacion_id = None

        if self.transicion_id is not None:

            self.ventana.after_cancel(
                self.transicion_id
            )

            self.transicion_id = None

        cliente = self.visitante_actual

        # Liberar al cliente
        self.visitante_actual = None
        self.tipo_atraccion = None

        self.lbl_jugador.config(
            text="🏁 Recorrido finalizado"
        )

        self.lbl_estado_juego.config(
            text=cliente + " terminó de disfrutar las atracciones."
        )

        self.lbl_tiempo.config(
            text="Tiempo restante: 0 segundos"
        )

        # Pantalla final
        self.canvas_juegos.delete("all")
        self.canvas_juegos.configure(
            bg="#14532D"
        )

        ancho = self.canvas_juegos.winfo_width()
        alto = self.canvas_juegos.winfo_height()

        self.canvas_juegos.create_text(
            ancho // 2,
            alto // 2 - 35,
            text="🎉 ¡GRACIAS POR VISITAR EL PARQUE!",
            fill="white",
            font=("Arial", 19, "bold")
        )

        self.canvas_juegos.create_text(
            ancho // 2,
            alto // 2 + 20,
            text=cliente + " terminó de jugar.",
            fill="#FACC15",
            font=("Arial", 15, "bold")
        )

        messagebox.showinfo(
            "Recorrido terminado",
            "¡" + cliente +
            " terminó de disfrutar las atracciones!\n\n"
            "Ya puede atender al siguiente visitante."
        )

    # =================================================
    # ANIMACIÓN PRINCIPAL
    # =================================================

    def animar_atraccion(self):
        # Cada cuadro limpia la escena de atracciones y la dibuja de nuevo.
        # fase representa el avance del movimiento y se calcula con un reloj
        # monotónico, que no depende de ajustes en la hora del sistema.

        if self.visitante_actual is None:
            return

        ancho = self.canvas_juegos.winfo_width()
        alto = self.canvas_juegos.winfo_height()

        if ancho < 100:
            ancho = 750

        if alto < 100:
            alto = 370

        self.canvas_juegos.delete("all")

        if self.tipo_atraccion == "Montaña rusa":

            self.dibujar_montana_rusa(
                ancho,
                alto
            )

        elif self.tipo_atraccion == "Martillo":

            self.dibujar_martillo(
                ancho,
                alto
            )

        # El movimiento depende del tiempo real, no de la rapidez del equipo.
        self.fase = (time.perf_counter() - self.inicio_atraccion) * 1.7

        self.animacion_id = self.ventana.after(
            33,
            self.animar_atraccion
        )

    # =================================================
    # DIBUJAR MONTAÑA RUSA
    # =================================================

    @staticmethod
    def punto_pista(t, ancho, alto):
        # Una curva cerrada compartida por rieles y vagones evita que el tren
        # flote fuera de la pista. Todas las medidas se adaptan al lienzo.
        return (ancho*(.5+.40*math.cos(t)),
                alto*(.51+.22*math.sin(t)+.08*math.sin(2*t)))

    def dibujar_vagon(self, x, y, angulo, escala, color, pasajeros=2):
        """Transforma coordenadas locales para inclinar cabina y pasajeros juntos."""
        c = self.canvas_juegos
        def punto(px, py):
            # Rotación 2D: (x*cos(a)-y*sin(a), x*sin(a)+y*cos(a)). Luego
            # escalamos y trasladamos al centro del vagón dentro del Canvas.
            return (x+escala*(px*math.cos(angulo)-py*math.sin(angulo)),
                    y+escala*(px*math.sin(angulo)+py*math.cos(angulo)))
        vertices = [punto(px, py) for px, py in [(-24,-23),(24,-23),(21,-5),(-21,-5)]]
        c.create_polygon(*[v for par in vertices for v in par], fill=color,
                         outline="#FFF1CB", width=2)
        for px in (-15, 15):
            wx, wy = punto(px, -3)
            r = 4*escala
            c.create_oval(wx-r, wy-r, wx+r, wy+r, fill="#172238", outline="#CBD5E1")
        for i in range(pasajeros):
            px = -14 + 28*i/max(1, pasajeros-1)
            hx, hy = punto(px, -31)
            r = 4.5*escala
            c.create_oval(hx-r, hy-r, hx+r, hy+r, fill="#FFD3AA", outline="")
            c.create_line(*punto(px-6,-24), *punto(px+6,-24), fill="#E2E8F0", width=2)

    def dibujar_montana_rusa(self, ancho, alto):
        c = self.canvas_juegos
        c.configure(bg="#B9E6F5")
        c.create_oval(ancho-100, 20, ancho-45, 75, fill="#FFE391", outline="")
        # Nubes con desplazamiento lento para dar profundidad a la escena.
        for i in range(4):
            x = (i*ancho/3 + self.fase*5) % (ancho+120)-60
            for dx, dy in [(0,0),(25,-10),(50,0)]:
                c.create_oval(x+dx, 55+dy, x+dx+55, 80+dy, fill="#F5FCFF", outline="")
        c.create_rectangle(0, alto*.85, ancho, alto, fill="#378766", outline="")
        for i in range(18):
            x,y = self.punto_pista(i*math.tau/18, ancho, alto)
            c.create_line(x,y,x,alto*.88, fill="#6B8A9D", width=3)
        puntos = [v for i in range(181)
                  for v in self.punto_pista(i*math.tau/180, ancho, alto)]
        c.create_line(*puntos, fill="#233B56", width=10)
        c.create_line(*puntos, fill="#FFE4A1", width=3)
        escala = min(ancho/900, alto/370, 1.15)
        # El ángulo de la tangente orienta cada vagón siguiendo la pendiente.
        for i, color in enumerate(["#F05269", "#8B5CF6", "#269DC2"]):
            t = self.fase*.65-i*.18
            x,y = self.punto_pista(t, ancho, alto)
            x2,y2 = self.punto_pista(t+.001, ancho, alto)
            self.dibujar_vagon(x,y,math.atan2(y2-y,x2-x),escala,color)
        c.create_text(ancho/2, 22, text="MONTAÑA RUSA · EXPRESO AVENTURA",
                      fill="#233B56", font=("Arial", 15, "bold"))
        c.create_text(ancho/2, alto-20, text="Cliente: " + self.visitante_actual,
                      fill="white", font=("Arial", 12, "bold"))

    def dibujar_martillo(self, ancho, alto):
        c = self.canvas_juegos
        c.configure(bg="#101B35")
        for i in range(30):
            x,y = (i*83+30)%ancho, (i*47+20)%max(1,alto*.7)
            brillo = .5+.3*math.sin(self.fase+i)
            c.create_oval(x,y,x+2,y+2, fill=self.color_atenuado("#E2E8FF",brillo), outline="")
        suelo = alto*.88
        c.create_rectangle(0,suelo,ancho,alto, fill="#243455", outline="")
        cx, cy = ancho/2, alto*.26
        largo = min(alto*.46, ancho*.32)
        # La amplitud aumenta suavemente al arrancar. El seno frena en los
        # extremos y acelera al pasar por el centro, como un péndulo.
        amplitud = 1.15*min(1, self.fase/4)
        angulo = math.sin(self.fase)*amplitud
        ex, ey = cx+largo*math.sin(angulo), cy+largo*math.cos(angulo)
        for lado in (-1,1):
            c.create_line(cx,cy,cx+lado*largo*.65,suelo,fill="#657BA8",width=13)
            c.create_line(cx,cy,cx+lado*largo*.65,suelo,fill="#A6BADD",width=3)
        # Arcos tenues muestran el recorrido reciente sin acumular dibujos.
        for i in range(6,0,-1):
            previo = math.sin(self.fase-i*.045)*amplitud
            px,py = cx+largo*math.sin(previo), cy+largo*math.cos(previo)
            c.create_oval(px-5,py-5,px+5,py+5,
                          fill=self.color_atenuado("#47D7FF",.25*(1-i/7),"#101B35"),outline="")
        c.create_line(cx,cy,ex,ey,fill="#F4BE55",width=15)
        c.create_line(cx,cy,ex,ey,fill="#FFF0B8",width=3)
        # La cabina gira con el brazo; la misma transformación mueve sus ocupantes.
        escala = min(ancho/700, alto/280, 1.4)
        self.dibujar_vagon(ex,ey,-angulo,escala,"#E95B83",3)
        c.create_oval(cx-16,cy-16,cx+16,cy+16,fill="#EF9160",outline="#FFE2AA",width=3)
        for i in range(15):
            x = ancho*(.15+.7*i/14)
            color = "#FFE391" if (i+int(self.fase*3))%3 else "#53DDF4"
            c.create_oval(x-3,suelo+5,x+3,suelo+11,fill=color,outline="")
        c.create_text(ancho/2,22,text="MARTILLO · VUELO NOCTURNO",fill="#FFE391",
                      font=("Arial",15,"bold"))
        c.create_text(ancho/2,alto-18,text="Cliente: "+self.visitante_actual,
                      fill="white",font=("Arial",12,"bold"))


    def cerrar_programa(self):
        # Cancelar los tres temporizadores antes de destruir la ventana evita
        # que un callback intente dibujar sobre controles que ya no existen.

        if self.fuegos_id is not None:
            self.ventana.after_cancel(self.fuegos_id)
            self.fuegos_id = None

        if self.animacion_id is not None:
            self.ventana.after_cancel(
                self.animacion_id
            )

        if self.transicion_id is not None:
            self.ventana.after_cancel(
                self.transicion_id
            )

        self.ventana.destroy()


# =====================================================
# INICIAR PROGRAMA
# =====================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = ParqueDiversiones(ventana)

    ventana.mainloop()


