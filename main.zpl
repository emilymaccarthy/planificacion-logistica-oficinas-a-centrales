# Define sets for offices and operational centers
set O := {1 to 56};  # Offices
set C := {1 to 10};  # Operational Centers
set H := {1 to 24};  # Hours in a day

# Parameters
#param demand[O] >= 0;          # Demand of operations for each office i at hour h
#param distance[O,C] >= 0;        # Distance between each office i and operational center j

param demand[O] := read "oficinas.txt" as "2n";
param distance[O * C] := read "distancias.txt" as "n+";

# do forall <o> in O do print demand[o];





# Variable
var y[C] binary;                  # Whether operational center j is open (1) or closed (0)
var x[O * C] binary;               # Whether office i is connected to operational center j

# Objective function: Minimize total cost (opening cost + cable distance cost)
minimize total_cost:
    sum <c> in C : 5700 * y[c] +
    sum <o,c> in O * C : x[o,c] * distance[o,c] * (17/1000);

# Constraints

# Constraint 1: If an office is assigned to an operational center, the center must be open
subto centralMustBeOpen: 
    forall <o, c> in O * C do
        x[o,c] <= y[c];

# Constraint 2: Each office must be connected to exactly one operational center
subto everyOfficeConnected:
    forall <o> in O do
        sum <c> in C : x[o,c] == 1;

# Constraint 3: The total operations per hour at any operational center cannot exceed 15,000
subto MaxCentralCap:
    forall <c> in C do
        sum <o> in O : x[o,c] * demand[o] <= 15000;



