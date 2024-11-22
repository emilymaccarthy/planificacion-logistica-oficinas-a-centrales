# Set de las oficinas (O) y centros operacionales (C)
set O := { read "data/og/oficinas.txt" as "<1n>" };
set C := { read "data/og/centrales.txt" as "<1n>" };


# Parameteros
param demand[O] := read "data/og/oficinas.txt" as "2n";
param distance[O * C] := read "data/og/distancias.txt" as "n+";

## Variables
var y[C] binary;                  # Si el centro c esta abierto (1) o cerrado (0)
var x[O * C] binary;              # Si la oficina o esta abierta en el centro de operacion c
var MaxOP;                           # Variable auxiliar para la funcion objetivo

# Funcion objetivo: Minimizar el numero minimo de centrales requerido para que sea factible el problema
minimize num_minimo_opXhora_necesarios:
    MaxOP;


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


