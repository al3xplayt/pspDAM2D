import socket
import time
import multiprocessing

def es_primo(n):
    """Función que determina si un número es primo"""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def contar_primos(fragmento):
    """Cuenta los números primos en un fragmento de datos usando multiprocesamiento"""
    return sum(1 for num in fragmento if es_primo(num))

def request_prime_numbers():
    """Conecta al servidor, recibe su fragmento de números y cuenta los primos"""
    # Medir el tiempo de ejecución del cliente
    start_time = time.time()

    # Conectar al servidor
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("10.20.20.100", 5021))  # IP del servidor

    # Recibir el fragmento de números
    data = client.recv(4096)  # Suponemos que no se excederá el tamaño del fragmento
    fragmento = list(map(int, data.decode().split(',')))

    # Dividir el fragmento en bloques más pequeños para procesarlos en paralelo
    num_processes = 1  # Número de procesos a usar para contar primos
    chunk_size = len(fragmento) // num_processes
    fragmentos_divididos = [fragmento[i:i + chunk_size] for i in range(0, len(fragmento), chunk_size)]

    # Crear un pool de procesos
    with multiprocessing.Pool(processes=num_processes) as pool:
        resultados = pool.map(contar_primos, fragmentos_divididos)

    # Sumar los resultados
    total_primos = sum(resultados)

    # Enviar el total de primos encontrados al servidor
    client.sendall(str(total_primos).encode())
    client.close()

    # Mostrar el tiempo de ejecución
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tiempo de ejecución en cliente: {execution_time:.2f} segundos")

if __name__ == "__main__":
    request_prime_numbers()
