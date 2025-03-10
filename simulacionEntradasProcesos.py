import random
import time
from multiprocessing import Pool, Manager, Lock
import matplotlib.pyplot as plt

# Configuración inicial
NUM_CAJONES = 5
CAPACIDAD_CAJON = 2500
TIEMPO_INSCRIPCION = 30  # en segundos
USUARIOS_POR_SEGUNDO = 1

tiempo_por_usuario = 30

# Función para procesar un grupo
def procesar_inscripcion(args):
    grupo_id, grupo_tamano, ranking, cajones, lock = args
    with lock:  # Proteger el acceso al diccionario compartido
        if cajones[ranking] + grupo_tamano <= CAPACIDAD_CAJON:
            time.sleep(tiempo_por_usuario / grupo_tamano)  # Simular inscripción
            cajones[ranking] += grupo_tamano
            return f"Grupo {grupo_id} asignado al cajón {ranking}."
        return f"Grupo {grupo_id} rechazado. No hay espacio suficiente en el cajón {ranking}."

# Generar usuarios
def generar_usuarios(cajones):
    usuarios = []
    usuario_id = 1
    while sum(cajones.values()) < NUM_CAJONES * CAPACIDAD_CAJON:
        grupo_tamano = random.randint(1, 6)  # Grupos de 1 a 6 personas
        ranking = random.randint(1, NUM_CAJONES)  # Ranking 1-5
        usuarios.append((usuario_id, grupo_tamano, ranking))
        usuario_id += 1
        time.sleep(1 / USUARIOS_POR_SEGUNDO)  # Simular llegada de usuarios
    return usuarios

# Simulación con procesos
def simular_inscripcion(numeroProcesos):
    with Manager() as manager:
        cajones = manager.dict({i: 0 for i in range(1, NUM_CAJONES + 1)})  # Compartir entre procesos
        lock = manager.Lock()  # Crear un candado compartido

        usuarios = generar_usuarios(cajones)
        args = [(grupo_id, grupo_tamano, ranking, cajones, lock) for grupo_id, grupo_tamano, ranking in usuarios]

        with Pool(numeroProcesos) as pool:
            resultados = pool.map(procesar_inscripcion, args)

        cajones_final = dict(cajones)
        return resultados, cajones_final

def graficarTiempos(cantidadProcesos, listaTiempos):
    """
    Grafica el tiempo total de ejecución en función de la cantidad de procesos utilizados.
    
    Args:
        cantidadProcesos (list): Lista con el número de procesos utilizados en cada simulación.
        listaTiempos (list): Lista con los tiempos totales de ejecución correspondientes a cada cantidad de procesos.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(cantidadProcesos, listaTiempos, marker='o', linestyle='-', color='b', label='Tiempo total')
    
    plt.title("Tiempo total de inscripción vs Cantidad de procesos", fontsize=14)
    plt.xlabel("Cantidad de procesos", fontsize=12)
    plt.ylabel("Tiempo total (segundos)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig("resultados_procesos.png")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    cantidadProcesos = [2, 6, 12]
    listaTiempos = []

    for procesos in cantidadProcesos:
        tiempoInicio = time.time()
        print("Iniciando con", procesos, "procesos")
        resultados, cajones = simular_inscripcion(procesos)
        print("\n".join(resultados[:10]))  # Mostrar solo los primeros 10 resultados
        print("\nEstado final de los cajones:", cajones)
        tiempoFin = time.time()
        tiempoTotal = tiempoFin - tiempoInicio
        listaTiempos.append(tiempoTotal)
        print(f"Tiempo total {tiempoTotal:.2f} segundos")
    
    graficarTiempos(cantidadProcesos, listaTiempos)
