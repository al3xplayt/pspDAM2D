import math
import time
import threading

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

def contar_primos_parcial(numeros: list[int], resultado: list, index: int):
    """Cuenta los primos en una sublista y almacena el resultado en la posición index."""
    resultado[index] = sum(1 for n in numeros if es_primo(n))

def leer_numeros_desde_csv(archivo: str) -> list[int]:
    """Lee números desde un archivo CSV y devuelve una lista de enteros."""
    with open(archivo, 'r') as f:
        return [int(num) for num in f.readline().split(",")]

def contar_primos_multihilo(numeros: list[int], num_hilos: int) -> int:
    """Cuenta los primos usando múltiples hilos."""
    size = len(numeros) // num_hilos  
    chunks = [numeros[i * size:(i + 1) * size] for i in range(num_hilos)]  

    if len(numeros) % num_hilos != 0:  
        chunks[-1].extend(numeros[num_hilos * size:])

    resultados = [0] * num_hilos  
    hilos = []

    for i in range(num_hilos):
        hilo = threading.Thread(target=contar_primos_parcial, args=(chunks[i], resultados, i))
        hilos.append(hilo)
        hilo.start()

    for hilo in hilos:
        hilo.join()

    return sum(resultados)  

if __name__ == "__main__":
    archivo_csv = "/home/isard/psp/trabajoSockets/numeros_aleatorios.csv"  
    numeros = leer_numeros_desde_csv(archivo_csv)

    num_hilos = 1  # Puedes probar con diferentes valores

    inicio = time.time()
    total_primos = contar_primos_multihilo(numeros, num_hilos)
    fin = time.time()

    print(f"Total de primos encontrados: {total_primos}")
    print(f"Tiempo de ejecución con {num_hilos} hilos: {fin - inicio:.4f} segundos")
