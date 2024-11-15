import re

# Open and read the ZIMPL file
with open("main.zpl", 'r') as file:
    content = file.read()

# Define regular expressions to find the specific parameters
maxop_pattern = r"param\s+MaxOP\s*:=\s*(\d+);"
maxop_match = re.search(maxop_pattern, content)
# Extract and print the values of the parameters
if maxop_match:
    maxop_value = maxop_match.group(1)  # This retrieves the value of MaxOP
    
    
# Extract solving time from statistics.txt
with open("statistics.txt", "r") as f:
    stats = f.read()
    time_match = re.search(r"solving\s*:\s*([\d.]+)", stats)
    solving_time = time_match.group(1) if time_match else "N/A"
    
with open("solution.txt", "r") as f:
    stats = f.read()
    sol_match = re.search(r"solution\s+status\s*[:\s]*([a-zA-Z\s]+)", stats)
    if sol_match:
        sol_status = sol_match.group(1)
        if "optimal solution found" in sol_status:
            sol_status = 1
        else:
            sol_status = 0
    


# Open the file and read its contents
with open("data/distancias.txt", 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

# Calculate the number of rows (lines in the file)
o_size = len(lines) -1 
c_size = len(lines[0].split())



# Write results to result.csv
with open("result.csv", "a") as f:
    f.write(f"{maxop_value},{o_size},{c_size},{solving_time},{sol_status}\n")
    




