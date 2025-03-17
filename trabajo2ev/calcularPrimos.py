import csv
import time

def es_primo(n):
    #Comprobar si un nunmero es primo
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def leer_csv(nombre_archivo):
    #Leer los datos del csv
    with open(nombre_archivo, 'r') as archivo:
        lector = csv.reader(archivo)
        for fila in lector:
            return list(map(int, fila))  # Convertimos a enteros

if __name__ == "__main__":
    archivo_csv = "/home/isard/psp/numeros_aleatorios.csv"  # Nombre del archivo CSV
    numeros = leer_csv(archivo_csv)
    
    inicio = time.time()
    primos = [n for n in numeros if es_primo(n)]
    fin = time.time()
    
    print("Total de primos: ", len(primos))
    print(f"Tiempo de ejecución: {fin - inicio:.4f} segundos")
