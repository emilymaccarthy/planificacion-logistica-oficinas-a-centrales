# Set de las oficinas (O) y centros operacionales (C)
# set O := {1 to 56};  # Oficinas
set O := { read "data/oficinas.txt" as "<1n>" };
# set C := {1 to 10};  # Centros Operacionales
set C := { read "data/centrales.txt" as "<1n>" };


# Parameteros

param demand[O] := read "data/oficinas.txt" as "2n";
param distance[O * C] := read "data/distancias.txt" as "n+";

# do forall <o> in O do print demand[o];

#Para guardar valores 
param MaxOP := 15000;


## Variables
var y[C] binary;                  # Si el centro c esta abierto (1) o cerrado (0)
var x[O * C] binary;              # Si la oficina o esta abierta en el centro de operacion c

# Funcion objetivo: Minimizar el costo total (costo de abrir + costo del cable)
minimize total_cost:
    sum <c> in C : 5700 * y[c] +
    sum <o,c> in O * C : x[o,c] * distance[o,c] * (17/1000);

## Restricciones

# Si la oficina o esta abierta (1) en el centro operativo c, entonces el centro opretivo debe estar abierto (1)
subto centralDebeEstarAbierta: 
    forall <o, c> in O * C do
        x[o,c] <= y[c];

# Cada oficina o debe estar conecta a exactmaente 1 centro operativo c
subto cadaOficinaConectada:
    forall <o> in O do
        sum <c> in C : x[o,c] == 1;

# El total de operacion por hora en el centro operacional c no puede exceder 150000
subto MaximasOpPorHora:
    forall <c> in C do
        sum <o> in O : x[o,c] * demand[o] <= MaxOP;

# #2) el total de oficinas no puede exceder 10 oficinas por central operativa: punto 2
# subto MaximoOficinaACentral:
#     forall <c> in C do
#         sum <o> in O : x[o,c] <= 10;


# scip -b commands.txt corre el archivo compila y guarda soluciones
# luego correr archivo de python (generador.py) para guardar las varibale sprinciaples y el tiempo del solver

