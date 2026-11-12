import tkinter as tk
from unittest.mock import patch
import parque_diversiones as p

root = tk.Tk()
root.withdraw()
app = p.ParqueDiversiones(root)
errors = []
root.report_callback_exception = lambda *args: errors.append(args)
for name in ('Ana', 'Luis', 'Maria'):
    app.cola.encolar(name)
assert [app.cola.desencolar() for _ in range(3)] == ['Ana', 'Luis', 'Maria']
for name in ('A', 'B', 'C'):
    app.pila.apilar(name)
assert [app.pila.desapilar() for _ in range(3)] == ['C', 'B', 'A']
app.particulas = []
app.dibujar_explosion(100, 100, 60, 0, 3, '#FFD166')
assert len(app.particulas) == 7
assert sorted(set(round(v['nacimiento'], 2) for v in app.particulas)) == [0, .48, .96]
app.particulas = []
app.dibujar_explosion(0, 0, 3, 0, 3, '#FFD166')
assert not app.particulas
app.lanzar_fuegos()
old = app.fuegos_id
app.lanzar_fuegos()
assert old not in root.tk.call('after', 'info')
# Simula todos los cuadros del show con Canvas real, sin esperar nueve segundos.
start = app.inicio_fuegos
for frame in range(300):
    if app.fuegos_id:
        root.after_cancel(app.fuegos_id)
    with patch.object(p.time, 'perf_counter', return_value=start+frame/30):
        app.animar_fuegos()
    if not app.particulas:
        break
assert not app.particulas and app.fuegos_id is None
app.visitante_actual = 'Prueba'
for w,h in [(750,370), (800,240), (1200,600)]:
    for frame in range(120):
        app.fase = frame/10
        for draw in (app.dibujar_montana_rusa, app.dibujar_martillo):
            app.canvas_juegos.delete('all')
            draw(w,h)
with patch.object(p.messagebox, 'showinfo'):
    app.iniciar_atraccion('Montaña rusa')
    app.siguiente_atraccion()
    assert app.tipo_atraccion == 'Martillo'
    app.siguiente_atraccion()
    assert app.visitante_actual is None
app.lanzar_fuegos()
app.cerrar_programa()
assert not errors, errors
print('OK: FIFO, LIFO, recursion, show completo, reinicio, 720 cuadros de atracciones, transiciones y cierre.')
