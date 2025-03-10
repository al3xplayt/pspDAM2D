import random
import time
import threading
import matplotlib.pyplot as plt

# Configuración inicial
NUM_CAJONES = 5
CAPACIDAD_CAJON = 2500
TIEMPO_INSCRIPCION = 30  # en segundos
USUARIOS_POR_SEGUNDO = 1

tiempo_por_usuario = 30
lock = threading.Lock()
cajones = {i: 0 for i in range(1, NUM_CAJONES + 1)}

# Función para procesar un grupo
def procesar_inscripcion(grupo_id, grupo_tamano, ranking):
    global cajones
    with lock:  # Proteger el acceso al diccionario compartido
        if cajones[ranking] + grupo_tamano <= CAPACIDAD_CAJON:
            time.sleep(tiempo_por_usuario / grupo_tamano)  # Simular inscripción
            cajones[ranking] += grupo_tamano
            print(f"Grupo {grupo_id} asignado al cajón {ranking}.")
        else:
            print(f"Grupo {grupo_id} rechazado. No hay espacio suficiente en el cajón {ranking}.")

# Generar usuarios
def generar_usuarios():
    usuario_id = 1
    threads = []
    while sum(cajones.values()) < NUM_CAJONES * CAPACIDAD_CAJON:
        grupo_tamano = random.randint(1, 6)  # Grupos de 1 a 6 personas
        ranking = random.randint(1, NUM_CAJONES)  # Ranking 1-5
        t = threading.Thread(target=procesar_inscripcion, args=(usuario_id, grupo_tamano, ranking))
        threads.append(t)
        t.start()
        usuario_id += 1
        time.sleep(1 / USUARIOS_POR_SEGUNDO)  # Simular llegada de usuarios
    
    for t in threads:
        t.join()

# Simulación con hilos
def simular_inscripcion(numeroHilos):
    global cajones
    cajones = {i: 0 for i in range(1, NUM_CAJONES + 1)}
    generar_usuarios()
    return cajones

def graficarTiempos(cantidadHilos, listaTiempos):
    plt.figure(figsize=(10, 6))
    plt.plot(cantidadHilos, listaTiempos, marker='o', linestyle='-', color='b', label='Tiempo total')
    plt.title("Tiempo total de inscripción vs Cantidad de hilos", fontsize=14)
    plt.xlabel("Cantidad de hilos", fontsize=12)
    plt.ylabel("Tiempo total (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("resultados_hilos.png")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    cantidadHilos = [2, 6, 12]
    listaTiempos = []

    for hilos in cantidadHilos:
        tiempoInicio = time.time()
        print("Iniciando con", hilos, "hilos")
        cajones_final = simular_inscripcion(hilos)
        print("\nEstado final de los cajones:", cajones_final)
        tiempoFin = time.time()
        tiempoTotal = tiempoFin - tiempoInicio
        listaTiempos.append(tiempoTotal)
        print(f"Tiempo total {tiempoTotal:.2f} segundos")
    
    graficarTiempos(cantidadHilos, listaTiempos)
