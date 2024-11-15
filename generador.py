import random
import time
import subprocess
import re
import csv
import sys
import os

## no evalua la distnacia real
# Función para generar el archivo distancias.txt
def generate_distancias(num_oficinas, num_centrales,path_to_save):
    
    with open(path_to_save, "w") as f:
        for i in range(1, num_oficinas + 1):
            distancias = [random.randint(1, 100) for _ in range(num_centrales)]  # Distancias aleatorias entre 1 y 100
            f.write(f"{i} " + " ".join(map(str, distancias)) + "\n")


# Función para generar el archivo centrales.txt
def generate_centrales(num_centrales,path_to_save):
    with open(path_to_save, "w") as f:
        for i in range(1, num_centrales + 1):
            lat = random.uniform(-90, 90)  # Latitud aleatoria
            lon = random.uniform(-180, 180)  # Longitud aleatoria
            f.write(f"{i},{lat},{lon}\n")

# Función para generar el archivo oficinas.txt
def generate_oficinas(num_oficinas, path_to_save):
    with open(path_to_save, "w") as f:
        for i in range(1, num_oficinas + 1):
            demanda = random.randint(1, 100)  # Demanda aleatoria entre 1 y 100
            lat = random.uniform(-90, 90)  # Latitud aleatoria
            lon = random.uniform(-180, 180)  # Longitud aleatoria
            f.write(f"{i},{demanda},{lat},{lon}\n")


#posible funcion para generar todos los files todabia no la testie 
def generate_files(num_oficinas, num_centrales,path_to_save):
  
    if not os.path.exists(path_to_save[0]):
        generate_centrales(num_centrales,path_to_save[0])
        
    if not os.path.exists(path_to_save[1]):
        generate_oficinas(num_oficinas, path_to_save[1]) 
        
    oficinas = {}
    with open(path_to_save[1], "r") as f:
        for line in f.readlines():
            parts = line.split()
            oficina_id = int(parts[0])
            lat, lon = float(parts[1]), float(parts[2])
            oficinas[oficina_id] = (lat, lon)

    centrales = {}
    with open(path_to_save[0], "r") as f:
        for line in f.readlines():
            parts = line.split()
            central_id = int(parts[0])
            lat, lon = float(parts[1]), float(parts[2])
            centrales[central_id] = (lat, lon)

    # Generar el archivo de distancias
    with open(path_to_save[2], "w") as f:
        for oficina_id, oficina_coords in oficinas.items():
            distancias = []
            for central_id, central_coords in centrales.items():
                # Calcular la distancia entre la oficina y la central usando la fórmula de Haversine
                distancia = haversine(oficina_coords[0], oficina_coords[1], central_coords[0], central_coords[1])
                distancias.append(f"{distancia:.2f}")  # Redondear a dos decimales
            f.write(f"{oficina_id} " + " ".join(distancias) + "\n")

# Radio de la Tierra en kilómetros
R = 6371

# Función para calcular la distancia entre dos puntos en la Tierra usando la fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    # Convertir grados a radianes
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Diferencias de latitudes y longitudes
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Fórmula de Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia en kilómetros
    return R * c
    

def run_solver():
    #runs the solver nomasy genera los archivos de solucion y estadisticas
    commands = f"""
read main.zpl
optimize

set display/verblevel 4

write solution solution.txt
write statistics statistics.txt
        """
    with open("commands.txt", "w") as cmd_file:
        cmd_file.write(commands)
        
    subprocess.run(["scip", "-b", "commands.txt"])
    
def solver_eficcency_maxop(main_zpl_path, solution_save_name, statistics_save_name,maximun_op_per_hour,parameter_op):
    """Corre el solver con el main pasado, guarda la solucion y las estadisticas de la solucion, 
    tambien en un csv guarda el tiempo, maxop, cantidad oficinas, cantidad centrales, si resolvio (1) o no (0)

    Args:
        main_zpl_path (string): path donde se encuentra el main.zpl
        solution_save_name (string): nombre, sine xtension del tipo arhcivo
        statistics_save_name (string): nombre del arhcivo para guardar, sin la extension del tipo de archivo
        distancias (_type_): _description_
    """
    # Open the ZIMPL file and read its content
    with open(main_zpl_path, 'r') as file:
        lines = file.readlines()

    # Look for the line containing 'param MaxOP' and update it
    updated_lines = []
    for line in lines:
        if line.strip().startswith("param MaxOP"):
            updated_lines.append(parameter_op + "\n")  # Replace the entire line with the new value
        else:
            updated_lines.append(line)

    # Write the updated content back to the file
    with open(main_zpl_path, 'w') as file:
        file.writelines(updated_lines)
    
        
   # Ejecutar SCIP con el archivo de comandos
    
    commands = f"""
read main.zpl
optimize

set display/verblevel 4

write solution {solution_save_name}
write statistics {statistics_save_name}
quit
        """

    with open("commands.txt", "w") as cmd_file:
        cmd_file.write(commands)
        
    try:
        subprocess.run(["scip", "-b", "commands.txt"], check=True)  # Will raise an error if SCIP fails
    except subprocess.CalledProcessError as e:
        print(f"Error running SCIP: {e}")
        sys.exit(1)

    
    # Paso 3: Extraer el tiempo de resolución del archivo statistics.txt
    with open(statistics_save_name, "r") as f:
        stats = f.read()
        time_match = re.search(r"solving\s*:\s*([\d.]+)", stats)
        solving_time = float(time_match.group(1)) if time_match else "N/A"
    
    # Paso 4: Extraer el estado de la solución del archivo solution.txt
    with open(solution_save_name, "r") as f:
        solution = f.read()
        sol_match = re.search(r"solution\s+status\s*[:\s]*([a-zA-Z\s]+)", solution)
        if sol_match:
            sol_status = sol_match.group(1)
            sol_status = 1 if "optimal solution found" in sol_status.lower() else 0
        else:
            sol_status = "N/A"
    
   
    # Append results to the CSV file
    with open("results_3/result_3.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([maximun_op_per_hour, solving_time, sol_status])

    
    print("Resultados guardados en result_3.csv")
     

def solver_con_instancias_generadas(cant_oficinas, cant_centrales, paths_data,main_zpl_path, solution_save_name, statistics_save_name):
    
    #primer generar los arhcivos de oficinas, centrales, distancias
    
    if not os.path.exists(paths_data[0]):
        generate_centrales(cant_centrales, paths_data[0])
    if not os.path.exists(paths_data[1]):
        generate_oficinas(cant_oficinas, paths_data[1]) 
    if not os.path.exists(paths_data[2]):
        generate_distancias(cant_oficinas, cant_centrales, paths_data[2])
    
    #if not os.path.exists(paths_data[2]):    
    #si el distancia no existe lo genera dentro de la funcion se ocnsidera si los otros dos files ya fueron creados sino se crean 
        #generate_files()
    
    #modifcar los paths del main para que lea esto 
    # Open and read the ZIMPL file
    with open(main_zpl_path, "r") as file:
        content = file.read()

    # Replace the path for 'oficinas.txt'
    content = re.sub(
        r'set\s+O\s*:=\s*\{.*?read\s+["\'].*?oficinas\.txt["\'].*?\}',
        f'set O := {{ read "{paths_data[1]}" as "<1n>" }}',
        content
    )

    # Replace the path for 'centrales.txt'
    content = re.sub(
        r'set\s+C\s*:=\s*\{.*?read\s+["\'].*?centrales\.txt["\'].*?\}',
        f'set C := {{ read "{paths_data[0]}" as "<1n>" }}',
        content
    )
    
    content = re.sub(
        r'param\s+demand\[O\]\s*:=\s*read\s+["\'].*?oficinas\.txt["\'].*?\;',  
        f'param demand[O] := read "{paths_data[1]}" as "2n";',  
        content
    )
    
    # Replace the path for 'distancias.txt'
    content = re.sub(
        r'param\s+distance\[O\s*\*\s*C\]\s*:=\s*read\s+["\'].*?distancias\.txt["\'].*?\;',
        f'param distance[O * C] := read "{paths_data[2]}" as "n+";',
        content
    )

    # Save the modified content back to the ZIMPL file
    with open(main_zpl_path, "w") as file:
        file.write(content)

    print(f"Updated paths in {main_zpl_path}.")
    
    # Ejecutar SCIP con el archivo de comandos
    commands = f"""
read main.zpl
optimize

set display/verblevel 4

write solution {solution_save_name}
write statistics {statistics_save_name}

quit
    """

    with open("commands.txt", "w") as cmd_file:
        cmd_file.write(commands)
        
    try:
        subprocess.run(["scip", "-b", "commands.txt"], check=True)  # Will raise an error if SCIP fails
    except subprocess.CalledProcessError as e:
        print(f"Error running SCIP: {e}")
        sys.exit(1)

    # Paso 3: Extraer el tiempo de resolución del archivo statistics.txt
    with open(statistics_save_name, "r") as f:
        stats = f.read()
        time_match = re.search(r"solving\s*:\s*([\d.]+)", stats)
        solving_time = float(time_match.group(1)) if time_match else "N/A"
    
    # Paso 4: Extraer el estado de la solución del archivo solution.txt
    with open(solution_save_name, "r") as f:
        solution = f.read()
        sol_match = re.search(r"solution\s+status\s*[:\s]*([a-zA-Z\s]+)", solution)
        if sol_match:
            sol_status = sol_match.group(1)
            sol_status = 1 if "optimal solution found" in sol_status.lower() else 0
        else:
            sol_status = "N/A"
    
    with open("results_4/results_4.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([cant_oficinas,cant_centrales, solving_time, sol_status])
    
    print("Resultados guardados en result_4.csv")

##punto 1: correr el solver
run_solver()

# #punto 3: testear las diferentes instancias de maxop
main = "main.zpl"
maxOP = 15000
replacement = f"param MaxOP := {maxOP};"

# solver_eficcency_maxop(
#     main_zpl_path=main,
#     solution_save_name=f"results_3/solution_{maxOP}.txt",
#     statistics_save_name=f"results_3/statistics_{maxOP}.txt",
#     maximun_op_per_hour=maxOP,
#     parameter_op =replacement
# )



# # #punto 4: generar instancias nuevas 
# num_oficinas = 65
# num_centrales = 10

# paths = [f"data/centrales_{num_centrales}.txt",f"data/oficinas_{num_oficinas}.txt", f"data/distancias_{num_oficinas}_{num_centrales}"]

# solver_con_instancias_generadas(
#     cant_oficinas=num_oficinas,
#     cant_centrales=num_centrales,
#     paths_data=paths,
#     main_zpl_path=main,
#     solution_save_name=f"results_4/solution_{num_oficinas}_{num_centrales}.txt",
#     statistics_save_name=f"results_4/statistics_{num_oficinas}_{num_centrales}.txt"
# )


