import sys
import time as tm
import numpy as np
import lib.io
import lib.check
import lib.objfunc
import lib.solutions
import lib.vecindades
import lib.visualize
import lib.busquedas
import lib.neighbor_selector
import lib.poblacionales
import lib.handlers
import signal as sg

sys.path.append("lib")
    
dificultad_humana = [1,2,3,4,5]
dificultad_cpu    = [1,2,3,4,5]

max_time = 10

print("Local Search algorithm, random_sol_constructive, best first, move_1")
            
def process_file(input_filepath, max_time):
    sg.signal(sg.SIGALRM, lib.handlers.timeout_handler)
    sg.alarm(1.1*max_time)
    try:
        start_time = tm.time()
        instance, initial_solution = lib.io.read_params(input_filepath)
        result = lib.busquedas.local_search(instance=instance, 
                                            initial_solution_function=lib.solutions.random_solution_constructive, 
                                            max_eval=1000000, 
                                            neighbor_selector_function=lib.neighbor_selector.best_first, 
                                            vecindad_function=lib.vecindades.move_1, 
                                            max_time=max_time, 
                                            verbose=False)
        
        end_time = tm.time()
        current_fitness, current_sol, n_eval, total_time = result
        print("Best fitness:", current_fitness)
        print("n_eval:", n_eval)
        print("Time calculating:", total_time, ", total time:", end_time - start_time)
        print("Best sol:\n", current_sol, "\n")
    except lib.handlers.TimeoutError as e:
        print("Timeout!")
        pass
        

# Código principal
for i in dificultad_cpu:
    for j in dificultad_humana:
        input_filepath = "data/benchmark_{}_{}.dat".format(i, j)
        print("Procesando data/benchmark_{}_{}.dat".format(i, j))
        process_file(input_filepath, 3600)
        sg.alarm(0)
        
    
"""
for i in dificultad_cpu:
    for j in dificultad_humana:
        input_filepath = "data/benchmark_{}_{}.dat".format(i,j)
        print("Procesando data/benchmark_{}_{}.dat".format(i,j))
        sg.signal(sg.SIGALRM, lib.handlers.timeout_handler)
        sg.alarm(max_time)
        try:
            
            start_time = tm.time()
            instance, initial_solution = lib.io.read_params(input_filepath)
            result = lib.busquedas.local_search(instance = instance, 
                                                initial_solution_function = lib.solutions.random_solution_constructive, 
                                                max_eval = 1000000, 
                                                neighbor_selector_function = lib.neighbor_selector.best_first, 
                                                vecindad_function = lib.vecindades.move_1, 
                                                max_time =  max_time, 
                                                verbose = False)
            
            end_time = tm.time()
            current_fitness,current_sol,n_eval,total_time = result
            print("Best fitness:",current_fitness)
            print("n_eval:",n_eval)
            print("Time calculating:",total_time," , total time:",end_time-start_time)
            print("Best sol:\n",current_sol,"\n")
        except TimeoutError as e:
            print("Timeout!")
# Ejecución con solución inicial
def ejec_sol_inicial():
    input_filepath = "data/input1"
    output_filepath = 'generated_files/card1'
    instance, initial_solution = lib.io.read_params(input_filepath)

    if lib.check.valid_solution(instance,initial_solution):
        fitness_lib = lib.objfunc.initialize_fitness()
        result_valid, fitness_value, fitness_time = lib.objfunc.fitness_heat(fitness_lib,output_filepath,instance,initial_solution)

        if not result_valid:
            print("Valor fitness: ",fitness_value)
            print("Ha tardado {} segundos".format(fitness_time))
            lib.visualize.visualizar_solucion(instance,initial_solution)
        else:
            print("Program ended with error")
    else:
        print("Not a valid solution")

# Probar random solution
def probar_rand_sol(instance):
    rand_sol = lib.solutions.random_solution(instance)
    print(rand_sol)
    lib.visualize.visualizar_solucion(instance,rand_sol)    
    return rand_sol

# Probar random solution constructiva
def probar_rand_sol_cons(instance):
    rand_sol = lib.solutions.random_solution_constructive(instance)
    print(rand_sol)
    lib.visualize.visualizar_solucion(instance,rand_sol)    
    return rand_sol
        
# Probar vecindades
def probar_vecindades():
    rand_sol = lib.solutions.random_solution(instance)
    print("Solución inicial aleatoria:",rand_sol)
    # visualizar_solucion(rand_sol[0]) 
    
    vecindad_1 = lib.vecindades.move_1(instance,rand_sol)
    # print("Vecindad move_1:",vecindad_1)
    print("Tam vecindad move_1:",len(vecindad_1))
    # for elem in vecindad_1[0]:
    #     visualizar_solucion(elem)  

    vecindad_2 = lib.vecindades.swap_2(instance,rand_sol)
    # print("Vecindad swap_2:",vecindad_2)
    print("Tam vecindad swap_2:",len(vecindad_2))  
    # for elem in vecindad_2[0]:
    #     visualizar_solucion(elem)  

def probar_random_search(verbose = False):
    time1 = tm.time()
    best_sol_value, best_sol_codif, _ = lib.busquedas.random_search(instance,10, verbose)
    time2 = tm.time()
    print("Best fitness:",best_sol_value)
    print("Best fitness codif:",best_sol_codif)
    print("Total time:",time2-time1)
    lib.visualize.visualizar_solucion(instance,best_sol_codif)
    
def probar_neighbor_selectors():
    
    rand_sol = lib.solutions.random_solution(instance)
    print("Solución inicial aleatoria:",rand_sol)

    vecindad_1 = lib.vecindades.move_1(instance,rand_sol)
    print("Size of vecindad:",len(vecindad_1))
    fitness_lib = lib.objfunc.initialize_fitness()
    result_valid, fitness_value, fitness_time = lib.objfunc.fitness_heat(fitness_lib,"",instance,rand_sol)
    print("Rand sol fitness:",fitness_value)
    print("Best first  :",lib.neighbor_selector.best_first  (instance,vecindad_1,1,1000,rand_sol,fitness_value,fitness_lib))
    print("Best greedy :",lib.neighbor_selector.best_greedy (instance,vecindad_1,1,1000,rand_sol,fitness_value,fitness_lib))
    print("Random neigh:",lib.neighbor_selector.random_neigh(instance,vecindad_1,1,1000,rand_sol,fitness_value,fitness_lib))
    
def probar_cross_over():
    # creamos una población de 10 elementos
    N = 10
    pobl = [lib.solutions.random_solution(instance) for i in range(N)]
    print("pobl:\n",pobl)
    M = 10
    proportion = -1
    print("Generamos {} cruces con la porporción {}".format(M,proportion))
    generados = lib.vecindades.cross_over(instance,pobl,M,proportion)
    print("Generados:\n",generados)
    
def probar_mutacion_general():
    N = 5
    pobl = [lib.solutions.random_solution(instance) for i in range(N)]
    pobl = np.array(pobl)
    print("pobl:\n",pobl)
    M = 5
    print("Generamos {} mutaciones".format(M))
    generados = lib.vecindades.mutacion_general(instance,pobl,M)
    print("Generados:\n",generados)
    print("pobl:\n",pobl)
    
def probar_eliminados_mutacion():
    N = 50
    pobl = [lib.solutions.random_solution(instance) for i in range(N)]
    pobl = np.array(pobl)
    
    M = 50
    repetitions = 1000
    count_valid = 0
    
    for _ in range(repetitions):
        generados = lib.vecindades.mutacion_general(instance,pobl,M)
        for i in range(N):
            if lib.check.valid_solution(instance,generados[i]):
                count_valid += 1
    
    print("De {} individuos originales, con {} mutaciones, {} repeticiones, tasa de válidos: {}".format(N,M,repetitions,count_valid/(N*repetitions)))
    
def procesar_archivo(filepath):
    print("Procesando", filepath)

    try:
        instance, initial_solution = lib.io.read_params(filepath)
        rand_sol = probar_rand_sol(instance) 
        
        # Extraer las coordenadas de cada chip en rand_sol
        coordenadas_chips = [(rand_sol[i], rand_sol[i+1]) for i in range(0, len(rand_sol), 2)]

        # Escribir las coordenadas al final del archivo
        with open(filepath, 'a') as file:
            file.write('\n')  # Línea en blanco
            for i, j in coordenadas_chips:
                file.write(f"{i} {j}\n")

    except FileNotFoundError:
        print(f"¡Error! El archivo {filepath} no fue encontrado.")
    except Exception as e:
        print(f"¡Error! Ocurrió un problema al procesar el archivo {filepath}: {str(e)}")


for i in range(1,6):
    for j in range(1,6):
        input_filepath = "data/benchmark_{}_{}.dat".format(i,j)
        print("Procesando data/benchmark_{}_{}.dat".format(i,j))
        instance, initial_solution = lib.io.read_params(input_filepath)
        # initial_solution = probar_rand_sol_cons(instance)
        # lib.visualize.visualizar_solucion(instance,initial_solution)
        print(lib.check.valid_solution(instance,initial_solution))
        
ejec_sol_inicial()
probar_vecindades()
probar_random_search(verbose=True)
lib.solutions.constructive_solution(instance, debug = True)
probar_neighbor_selectors()

lib.busquedas.local_search(instance,lib.solutions.constructive_solution,10000000,lib.neighbor_selector.best_first,lib.vecindades.move_1,18000,True)
lib.busquedas.local_beam_search(instance,lib.solutions.random_solution,1000000,5,lib.vecindades.move_1,3600,True)

probar_cross_over()
probar_mutacion_general()
probar_eliminados_mutacion()

total_time,pobl,pobl_fit,gen = lib.poblacionales.genetic_algorithm(instance,lib.vecindades.cross_over,lib.vecindades.mutacion_general,max_time=300,max_generations=10,mut_chance=0.1,N=5,verbose=True)
print("Spent {} seconds\nPobl:\n{}\nPobl_fitnesses:\n{}\nTook {} generations".format(total_time,pobl,pobl_fit,gen))

best_fitness,best_sol,n_eval,total_time = lib.busquedas.vnd(instance,lib.solutions.random_solution,10000,lib.neighbor_selector.best_greedy,lib.vecindades.swap_2,lib.vecindades.move_1,6000,True)
print("VND - Spent {} seconds\nbest_sol:\n{}\nbest_sol_fitness:\n{}\nTook {} evaluations".format(total_time,best_sol,best_fitness,n_eval))

best_fitness,best_sol,n_eval,total_time = lib.busquedas.vns(instance,lib.solutions.random_solution,10000,lib.neighbor_selector.best_greedy,lib.vecindades.swap_2,lib.vecindades.move_1,6000,True)
print("VNS - Spent {} seconds\nbest_sol:\n{}\nbest_sol_fitness:\n{}\nTook {} evaluations".format(total_time,best_sol,best_fitness,n_eval))

best_fitness,best_sol,n_eval,total_time = lib.busquedas.simulated_annealing(instance,lib.solutions.random_solution,10000,lib.neighbor_selector.best_greedy,lib.vecindades.swap_2,600,True)
print("Simulated annealing - Spent {} seconds\nbest_sol:\n{}\nbest_sol_fitness:\n{}\nTook {} evaluations".format(total_time,best_sol,best_fitness,n_eval))
"""