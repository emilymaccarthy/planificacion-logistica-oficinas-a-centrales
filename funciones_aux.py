import random
import subprocess
import re
import csv
import sys
import os
import math

# Función para generar el archivo centrales.txt
def generate_centrales(num_centrales,path_to_save):
    with open(path_to_save, "w") as f:
        for i in range(1, num_centrales + 1):
            lat = random.uniform(-34.70, -34.60) 
            lon = random.uniform(-58.45, -58.35)
            f.write(f"{i} {lat} {lon}\n")

# Función para generar el archivo oficinas.txt
def generate_oficinas(num_oficinas, path_to_save):
    with open(path_to_save, "w") as f:
        for i in range(1, num_oficinas + 1):
            demanda = random.randint(1000, 23)  
            lat = random.uniform(-34.70, -34.60) 
            lon = random.uniform(-58.45, -58.35)
            f.write(f"{i} {demanda} {lat} {lon}\n")


#genera los files de las centrales y las oficinas, luego usa una funcion para calcular la distancia en km entre 2 puntos para genrerar distancias.txt
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
            lat, lon = float(parts[2]), float(parts[3])
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
            f.write(f"{' '.join(distancias)} \n")



# Función para calcular la distancia entre dos puntos en la Tierra usando la fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    R = 6371
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
    
def run_solver(main_zpl_file):
    #runs the solver nomasy genera los archivos de solucion y estadisticas
    commands = f"""
read {main_zpl_file}
optimize

write solution solution.txt
write statistics statistics.txt

quit
        """
    with open("commands.txt", "w") as cmd_file:
        cmd_file.write(commands)
        
    subprocess.run(["scip", "-b", "commands.txt"])
    
def solver_eficciency_maxop(main_zpl_path, solution_save_name, statistics_save_name,maximun_op_per_hour):
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
            updated_lines.append(f"param MaxOP := {maximun_op_per_hour};" + "\n")  # Replace the entire line with the new value
        else:
            updated_lines.append(line)

    # Write the updated content back to the file
    with open(main_zpl_path, 'w') as file:
        file.writelines(updated_lines)
    
        
   # Ejecutar SCIP con el archivo de comandos
    
    commands = f"""
read {main_zpl_path}
optimize

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
    
    # Buscar el objective value
        objective_match = re.search(r"objective value\s*[:\s]*([0-9\.]+)", solution)
        if objective_match:
            objective_value = float(objective_match.group(1))  # Convierte el valor extraído a float
        else:
            objective_value = "N/A"  # Si no se encuentra el objective value, lo asigna como "N/A"

    # Append results to the CSV file
    with open("soluciones/ej3/result_3.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([maximun_op_per_hour, solving_time, sol_status, objective_value])

    
    print("Resultados guardados en result_3.csv")
     
def solver_con_instancias_generadas(cant_oficinas, cant_centrales, paths_data,main_zpl_path, solution_save_name, statistics_save_name,time_limit):
    
    #primer generar los arhcivos de oficinas, centrales, distancias
    generate_files(cant_oficinas,cant_centrales,paths_data)
    
    
    #modifcar los paths del main para que lea esto 
    with open(main_zpl_path, "r") as file:
        lines = file.readlines()
        
    updated_lines = []

    
    for line in lines:
        
        if line.startswith("set O := {"):
            updated_lines.append(f"set O := {{ read \"{paths_data[1]}\" as \"<1n>\" }};\n")
        
        elif line.startswith("set C := {"):
            updated_lines.append(f"set C := {{ read \"{paths_data[0]}\" as \"<1n>\" }};\n")
        
        elif line.startswith("param demand[O]"):
            updated_lines.append(f"param demand[O] := read \"{paths_data[1]}\" as \"2n\";\n")
        
        elif line.startswith("param distance[O * C]"):
            updated_lines.append(f"param distance[O * C] := read \"{paths_data[2]}\" as \"n+\";\n")
        else:
            
            updated_lines.append(line)
    
    with open(main_zpl_path, "w") as file:
        file.writelines(updated_lines)
       
    
    # Ejecutar SCIP con el archivo de comandos
    commands = f"""
read {main_zpl_path}
set limit gap 0.06
optimize

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
            
            # Buscar el objective value
        objective_match = re.search(r"objective value\s*[:\s]*([0-9\.]+)", solution)
        if objective_match:
            objective_value = float(objective_match.group(1))  # Convierte el valor extraído a float
        else:
            objective_value = "N/A"  # Si no se encuentra el objective value, lo asigna como "N/A"

    
    with open("soluciones/ej4/results_4.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([cant_oficinas,cant_centrales, solving_time, sol_status, objective_value])
    
    print("Resultados guardados en result_4.csv")
