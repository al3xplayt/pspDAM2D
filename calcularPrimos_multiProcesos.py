import math
import time
import multiprocessing

def es_primo(n: int) -> bool:
    """Determina si un número es primo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def contar_primos_parcial(numeros: list[int]) -> int:
    """Cuenta los primos en una sublista."""
    return sum(1 for n in numeros if es_primo(n))

def leer_numeros_desde_csv(archivo: str) -> list[int]:
    """Lee números desde un archivo CSV y devuelve una lista de enteros."""
    with open(archivo, 'r') as f:
        return [int(num) for num in f.readline().split(",")]

def contar_primos_multiproceso(numeros: list[int], num_procesos: int) -> int:
    """Cuenta los primos usando múltiples procesos."""
    pool = multiprocessing.Pool(num_procesos)  
    size = len(numeros) // num_procesos  
    chunks = [numeros[i * size:(i + 1) * size] for i in range(num_procesos)]  

    if len(numeros) % num_procesos != 0:  
        chunks[-1].extend(numeros[num_procesos * size:])

    resultados = pool.map(contar_primos_parcial, chunks)  
    pool.close()
    pool.join()

    return sum(resultados)  

if __name__ == "__main__":
    archivo_csv = "/home/isard/psp/numeros_aleatorios.csv"  # Asegúrate de tener este archivo con números
    numeros = leer_numeros_desde_csv(archivo_csv)

    num_procesos = multiprocessing.cpu_count()  # Usa tantos procesos como núcleos disponibles

    inicio = time.time()
    total_primos = contar_primos_multiproceso(numeros, num_procesos)
    fin = time.time()

    print(f"Total de primos encontrados: {total_primos}")
    print(f"Tiempo de ejecución con {num_procesos} procesos: {fin - inicio:.4f} segundos")
