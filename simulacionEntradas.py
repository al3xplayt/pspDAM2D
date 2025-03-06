import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Configuración inicial
NUM_CAJONES = 5
CAPACIDAD_CAJON = 250
TIEMPO_INSCRIPCION = 0.3  # en segundos
USUARIOS_TOTAL = 1000

# Estado compartido
cajones = {i: 0 for i in range(1, NUM_CAJONES + 1)}
lock = threading.Lock()  # Lock global para sincronizar el acceso a los cajones

# Función para procesar un grupo con sincronización
def procesar_inscripcion(grupo_id, grupo_tamano, ranking):
    global cajones

    with lock:  # Bloqueamos para evitar condiciones de carrera
        if cajones[ranking] + grupo_tamano <= CAPACIDAD_CAJON:
            time.sleep(TIEMPO_INSCRIPCION / grupo_tamano)  # Simular inscripción
            cajones[ranking] += grupo_tamano
            return f"Grupo {grupo_id} asignado al cajón {ranking}."
        return f"Grupo {grupo_id} rechazado. No hay espacio suficiente en el cajón {ranking}."

# Generar usuarios
def generar_usuarios():
    usuarios = []
    for i in range(USUARIOS_TOTAL):
        grupo_tamano = random.randint(1, 6)  # Grupos de 1 a 6 personas
        ranking = random.randint(1, NUM_CAJONES)  # Ranking 1-5
        usuarios.append((i, grupo_tamano, ranking))
    return usuarios

# Simulación con hilos y sincronización
def simular_inscripcion(numeroHilos):
    global cajones
    cajones = {i: 0 for i in range(1, NUM_CAJONES + 1)}  # Reiniciar estado

    usuarios = generar_usuarios()
    with ThreadPoolExecutor(numeroHilos) as executor:
        resultados = list(executor.map(lambda u: procesar_inscripcion(*u), usuarios))

    return resultados, dict(cajones)  # Convertimos a diccionario normal para imprimir

# Graficar tiempos de ejecución
def graficarTiempos(cantidadHilos, listaTiempos):
    plt.figure(figsize=(10, 6))
    plt.plot(cantidadHilos, listaTiempos, marker='o', linestyle='-', color='b', label='Tiempo total')

    plt.title("Tiempo total de inscripción vs Cantidad de hilos", fontsize=14)
    plt.xlabel("Cantidad de hilos", fontsize=12)
    plt.ylabel("Tiempo total (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    cantidadHilos = [2, 6, 12]
    listaTiempos = []

    for i in cantidadHilos:
        tiempoInicio = time.time()
        print(f"\nIniciando simulación con {i} hilos...")
        resultados, estado_final_cajones = simular_inscripcion(i)
        print("\n".join(resultados))
        print("\nEstado final de los cajones:", estado_final_cajones)
        tiempoFin = time.time()
        tiempoTotal = tiempoFin - tiempoInicio
        listaTiempos.append(tiempoTotal)
        print(f"Tiempo total: {tiempoTotal:.4f} segundos")

    graficarTiempos(cantidadHilos, listaTiempos)
