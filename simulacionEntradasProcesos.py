import random
import time
from concurrent.futures import ProcessPoolExecutor
import matplotlib.pyplot as plt
from multiprocessing import Manager, Lock

# Configuración inicial
NUM_CAJONES = 5
CAPACIDAD_CAJON = 250
TIEMPO_INSCRIPCION = 0.3  # en segundos
USUARIOS_TOTAL = 1000

# Función para procesar un grupo con sincronización
def procesar_inscripcion(grupo_id, grupo_tamano, ranking, cajones, lock):
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

# Simulación con procesos y sincronización
def simular_inscripcion(numeroProcesos):
    usuarios = generar_usuarios()
    
    with Manager() as manager:
        cajones = manager.dict({i: 0 for i in range(1, NUM_CAJONES + 1)})  # Diccionario compartido
        lock = Lock()  # Lock para sincronizar el acceso a los cajones

        with ProcessPoolExecutor(numeroProcesos) as executor:
            resultados = list(executor.map(lambda u: procesar_inscripcion(*u, cajones, lock), usuarios))
        
        return resultados, dict(cajones)  # Convertimos a diccionario normal para imprimir

# Graficar los tiempos de ejecución
def graficarTiempos(cantidadProcesos, listaTiempos):
    plt.figure(figsize=(10, 6))
    plt.plot(cantidadProcesos, listaTiempos, marker='o', linestyle='-', color='r', label='Tiempo total')

    plt.title("Tiempo total de inscripción vs Cantidad de procesos", fontsize=14)
    plt.xlabel("Cantidad de procesos", fontsize=12)
    plt.ylabel("Tiempo total (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    cantidadProcesos = [2, 6, 12]
    listaTiempos = []

    for i in cantidadProcesos:
        tiempoInicio = time.time()
        print(f"\nIniciando simulación con {i} procesos...")
        resultados, estado_final_cajones = simular_inscripcion(i)
        print("\n".join(resultados))
        print("\nEstado final de los cajones:", estado_final_cajones)
        tiempoFin = time.time()
        tiempoTotal = tiempoFin - tiempoInicio
        listaTiempos.append(tiempoTotal)
        print(f"Tiempo total: {tiempoTotal:.4f} segundos")

    graficarTiempos(cantidadProcesos, listaTiempos)
