import socket
import threading
import time

def es_primo(n):
    """Función que determina si un número es primo"""
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def manejar_cliente(cliente_socket, fragmento):
    """Maneja la conexión de un cliente y procesa su fragmento"""
    try:
        # Contar los primos en el fragmento
        primos_en_fragmento = [num for num in fragmento if es_primo(num)]
        total_primos = len(primos_en_fragmento)

        # Enviar el total de primos al servidor
        cliente_socket.sendall(str(total_primos).encode())
    finally:
        cliente_socket.close()

def servidor():
    """Función que ejecuta el servidor"""
    # Crear el socket del servidor
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 5021))  # Escuchar en todas las interfaces
    server_socket.listen(5)
    print("Servidor escuchando en el puerto 5020...")

    # Leer el archivo CSV
    with open('/home/isard/psp/numeros_aleatorios.csv', 'r') as f:
        numeros = list(map(int, f.read().split(',')))  # Convertir a lista de enteros

    # Determinar el número de clientes y dividir el archivo en fragmentos
    num_clients = 3  # Asumimos 3 clientes como ejemplo
    fragmentos = [numeros[i::num_clients] for i in range(num_clients)]

    # Esperar a que todos los clientes se conecten antes de comenzar el tiempo
    hilos_cliente = []
    start_time = None

    for i in range(num_clients):
        cliente_socket, _ = server_socket.accept()
        print(f"Cliente {i+1} conectado")

        # Iniciar la medición del tiempo cuando el último cliente se conecte
        if len(hilos_cliente) == num_clients - 1:
            start_time = time.time()

        # Enviar el fragmento de números al cliente
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente_socket, fragmentos[i]))
        hilo_cliente.start()
        hilos_cliente.append(hilo_cliente)

    # Esperar a que todos los hilos terminen
    for hilo in hilos_cliente:
        hilo.join()

    # Mostrar el tiempo total de ejecución si todos los clientes han terminado
    if start_time is not None:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Tiempo total de ejecución: {execution_time:.4f} segundos")

if __name__ == "__main__":
    servidor()
