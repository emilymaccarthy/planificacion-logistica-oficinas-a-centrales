import random

# Función para generar el archivo centrales.txt
def generate_centrales(num_centrales):
    with open("centrales.txt", "w") as f:
        for i in range(1, num_centrales + 1):
            lat = random.uniform(-90, 90)  # Latitud aleatoria
            lon = random.uniform(-180, 180)  # Longitud aleatoria
            f.write(f"{i},{lat},{lon}\n")

# Genera el archivo con 10 centrales operativas como ejemplo
generate_centrales(10)


# Función para generar el archivo oficinas.txt
def generate_oficinas(num_oficinas):
    with open("oficinas.txt", "w") as f:
        for i in range(1, num_oficinas + 1):
            demanda = random.randint(1, 100)  # Demanda aleatoria entre 1 y 100
            lat = random.uniform(-90, 90)  # Latitud aleatoria
            lon = random.uniform(-180, 180)  # Longitud aleatoria
            f.write(f"{i},{demanda},{lat},{lon}\n")

# Genera el archivo con 10 oficinas como ejemplo
generate_oficinas(10)

## no evalua la distnacia real
# Función para generar el archivo distancias.txt
def generate_distancias(num_oficinas, num_centrales):
    with open("distancias.txt", "w") as f:
        for i in range(1, num_oficinas + 1):
            distancias = [random.randint(1, 100) for _ in range(num_centrales)]  # Distancias aleatorias entre 1 y 100
            f.write(f"{i} " + " ".join(map(str, distancias)) + "\n")

# Genera el archivo con distancias para 10 oficinas y 10 centrales operativas como ejemplo
generate_distancias(10, 10)


import time
import subprocess

# Función para medir el tiempo de resolución
def measure_solver_time(centrales_file, oficinas_file, distancias_file):
    # Comando para ejecutar el solver con los archivos generados
    command = [
        "scip",  # O el solver que estés usando
        "-c", 
        f"read {centrales_file} {oficinas_file} {distancias_file}",
        "optimize"
    ]
    
    start_time = time.time()  # Inicia el conteo del tiempo
    
    # Ejecuta el solver (suponiendo que el solver se ejecuta con un comando como este)
    result = subprocess.run(command, capture_output=True, text=True)
    
    end_time = time.time()  # Fin del conteo del tiempo
    
    solving_time = end_time - start_time  # Tiempo total de resolución
    return solving_time

# Ejemplo de uso:
solver_time = measure_solver_time("centrales.txt", "oficinas.txt", "distancias.txt")
print(f"Tiempo de resolución: {solver_time} segundos")
