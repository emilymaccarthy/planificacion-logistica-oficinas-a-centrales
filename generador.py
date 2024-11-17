from funciones_aux import run_solver, solver_eficciency_maxop, solver_con_instancias_generadas

def main():
    
    
    ##1: correr el solver
    main_1 = "main_og.zpl"
    # run_solver(main_1)
    
    ##2: correr el solver +1 restriccion
    main_2 = "main2.zpl"
    # run_solver(main_2) # creo que la nueva restriccion nu funca
    
    ##3: testear las diferentes instancias de maxop
    main_3 = "main3.zpl"

    # #maxOPS = [5000,6000,7000,8000,9000,10000,11000,13000,15000,17000,19000]
    # #maxOPS = [8100,8200,8300,8400,8500,8600,8700,8800,8900,9200,9400,9600]
    # maxOPS = [11000,12000,14000,16000,18000]
    # for maxOP in maxOPS:
    #     solver_eficciency_maxop(
    #         main_zpl_path=main_3,
    #         solution_save_name=f"soluciones/ej3/solution/solution_{maxOP}.txt",
    #         statistics_save_name=f"soluciones/ej3/statistics/statistics_{maxOP}.txt",
    #         maximun_op_per_hour=maxOP
    #     )

    ##4: generar instancias nuevas 
    main_4 = "main4.zpl"
    
    cant_oficinas = [56,60,70,80,90,100,150,200,300]
    cant_centrales = [5,10,20,30,40,45,50,55,60]
    
    #cantidad de tiempo que quiero que el solver corra encontrando una solucion
    cant_minutos = 5
    tiempo_solver = 60*cant_minutos
    
    for oficina in cant_oficinas:
        for central in cant_centrales:
            paths = [f"data/centrales_{central}.txt",f"data/oficinas_{oficina}.txt", f"data/distancias_{oficina}_{central}"]
            print(f"\n\nSOLVER: {oficina}_{central}\n\n")
            solver_con_instancias_generadas(
                cant_oficinas=oficina,
                cant_centrales=central,
                paths_data=paths,
                main_zpl_path=main_4,
                solution_save_name=f"soluciones/ej4/solution/solution_{oficina}_{central}.txt",
                statistics_save_name=f"soluciones/ej4/statistics/statistics_{oficina}_{central}.txt",
                time_limit=tiempo_solver
            )
    
    

    
# Con Gap = 0.05 llega hasta 60_20

