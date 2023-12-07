import sys
import time as tm
sys.path.append("lib")
import lib.io
import lib.check
import lib.objfunc
import lib.solutions
import lib.vecindades
import lib.visualize
import lib.busquedas
import lib.neighbor_selector

# Probar io
input_filepath = "data/input2"
instance, initial_solution = lib.io.read_params(input_filepath)
    
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
def probar_rand_sol():
    rand_sol = lib.solutions.random_solution(instance)
    print(rand_sol)
    lib.visualize.visualizar_solucion(instance,rand_sol)    
        

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
    
# ejec_sol_inicial()
# probar_rand_sol()
# probar_vecindades()
# probar_random_search(verbose=True)
# lib.solutions.constructive_solution(instance)
# probar_neighbor_selectors()

# lib.busquedas.local_search(instance,lib.solutions.constructive_solution,10000000,lib.neighbor_selector.best_first,lib.vecindades.move_1,18000,True)
lib.busquedas.local_beam_search(instance,lib.solutions.random_solution,1000000,5,lib.vecindades.move_1,3600,True)