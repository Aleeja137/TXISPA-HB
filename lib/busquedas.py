import solutions
import objfunc
import vecindades
import neighbor_selector

def local_search(instance, initial_solution_function, max_eval, neighbor_selector_function, vecindad_function, max_time, verbose = False):
        
    if verbose:
        print("Función para solución inicial elegida: {}\n"
              "Función para generar vecindad elegida: {}\n"
              "Función para elegir vecino siguiente elegida: {}\n"
              .format(initial_solution_function.__name__,vecindad_function.__name__,neighbor_selector_function.__name__))
        
    # Obtener solución inicial
    initial_sol = initial_solution_function(instance)
    mejora = True
    
    # Calcular punto de partida
    fitness_lib = objfunc.initialize_fitness()
    _, fitness_value, fitness_time = objfunc.fitness_heat(fitness_lib,"",instance,initial_sol)
    n_eval = 1
    
    current_sol = initial_sol
    current_fitness = fitness_value
    total_time = fitness_time
    
    # Mientras no sobrepasen las iteraciones, se encuentre mejora o no se sobrepase el tiempo de ejecución
    while n_eval < max_eval and mejora and total_time < max_time:
        
        if verbose:
            print("Evaluations used: {}, time used: {}, best_fitness: {}".format(n_eval,round(total_time,2),current_fitness))
            
        # Se obtiene la vecindad según función elegida
        vecindad = vecindad_function(instance,current_sol)

        # Se recorren los vecinos según función elegida
        encontrado,used_eval,best_fitness,best_candidato,used_time = neighbor_selector_function(instance,vecindad,n_eval,max_eval,current_sol,current_fitness,fitness_lib)
        
        total_time += used_time
        n_eval     += used_eval
        
        # Si no se ha encontrado un vecino que mejore, no merece seguir buscando
        if not encontrado:
            mejora = False
        # Si se ha encontrado un mejor vecino, se sigue por ese
        else:
            current_sol = best_candidato
            current_fitness = best_fitness

    if verbose:
        print("Ejecución terminada!\nEvaluations used: {}, time used: {}, best_fitness: {}".format(n_eval,round(total_time,2),current_fitness))
            
    return current_fitness,current_sol,n_eval,total_time