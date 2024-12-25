import random
import time
from concurrent.futures import ThreadPoolExecutor
import matplotlib.pyplot as plt

# Configuración inicial
NUM_CAJONES = 5
CAPACIDAD_CAJON = 250
TIEMPO_INSCRIPCION = 0.3  # en segundos
USUARIOS_TOTAL = 1000
CAJONES = {i: 0 for i in range(1, NUM_CAJONES + 1)}

# Función para procesar un grupo
def procesar_inscripcion(grupo_id, grupo_tamano, ranking):
    global CAJONES
    if CAJONES[ranking] + grupo_tamano <= CAPACIDAD_CAJON:
        time.sleep(TIEMPO_INSCRIPCION / grupo_tamano)  # Simular inscripción
        CAJONES[ranking] += grupo_tamano
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

# Simulacion
def simular_inscripcion(numeroHilos):
    usuarios = generar_usuarios()
    with ThreadPoolExecutor(numeroHilos) as executor:  # Ajustar número de hilos
        resultados = list(executor.map(lambda u: procesar_inscripcion(*u), usuarios))
    return resultados

def graficarTiempos(cantidadHilos, listaTiempos):
    """
    Grafica el tiempo total de ejecución en función de la cantidad de hilos utilizados.
    
    Args:
        cantidadHilos (list): Lista con el número de hilos utilizados en cada simulación.
        listaTiempos (list): Lista con los tiempos totales de ejecución correspondientes a cada cantidad de hilos.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(cantidadHilos, listaTiempos, marker='o', linestyle='-', color='b', label='Tiempo total')
    
    plt.title("Tiempo total de inscripción vs Cantidad de hilos", fontsize=14)
    plt.xlabel("Cantidad de hilos", fontsize=12)
    plt.ylabel("Tiempo total (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    cantidadHilos = [2,6,12]
    listaTiempos = []
    for i in cantidadHilos:
        CAJONES = {i: 0 for i in range(1, NUM_CAJONES + 1)}
        tiempoInicio = time.time()
        print ("iniciando")
        resultados = simular_inscripcion(i)
        print("\n".join(resultados))
        print("\nEstado final de los cajones:", CAJONES)
        tiempoFin = time.time()
        tiempoTotal = tiempoFin - tiempoInicio
        listaTiempos.append(tiempoTotal)
        print(f"Tiempo total {tiempoTotal}")
    graficarTiempos(cantidadHilos, listaTiempos)
