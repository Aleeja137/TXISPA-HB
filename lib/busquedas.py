import solutions
import objfunc
import vecindades
import neighbor_selector
import numpy as np

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

def local_beam_search (instance, initial_solution_function, max_eval, N, vecindad_function, max_time, verbose = False):
    
    if verbose:
        print("Función para solución inicial elegida: {}\n"
              "Función para generar vecindad elegida: {}\n"
              "Número de vecinos simulatáneos: {}\n"
              .format(initial_solution_function.__name__,vecindad_function.__name__, N))
        
    # Obtener soluciones iniciales
    initial_solutions = [initial_solution_function(instance) for i in range(N)]
    mejora = True
    # print("initial_solutions:",initial_solutions)

    # Calcular puntos de partida
    current_fitnesses = np.empty(N)
    current_solutions = initial_solutions
    total_time = 0
    
    fitness_lib = objfunc.initialize_fitness()
    for i in range(N):
        _, fitness_value, fitness_time = objfunc.fitness_heat(fitness_lib,"",instance,initial_solutions[i])
        total_time += fitness_time
        current_fitnesses[i] = fitness_value
    
    n_eval = N
        
    # print("current_solutions:",current_solutions)
    # print("current_fitnesses:",current_fitnesses)
    # print("n_eval:",n_eval)
    # print("total_time:",total_time)    
    
    # Mientras no sobrepasen las iteraciones, se encuentre mejora o no se sobrepase el tiempo de ejecución
    while n_eval < max_eval and mejora and total_time < max_time:
        
        if verbose:
            print("Evaluations used: {}, time used: {}, best_fitness: {}".format(n_eval,round(total_time,2),current_fitnesses))
            
        # Se obtiene la vecindad según función elegida
        vecindad = vecindad_function(instance,current_solutions[0])
        for i in range(1,N):
            vecindad_i = vecindad_function(instance,current_solutions[i])
            vecindad = np.concatenate([vecindad,vecindad_i])
        
        # print("vecindad PRE prune {}:\n{}".format(len(vecindad),vecindad))
        vecindad = np.unique(vecindad, axis=0)
        # print("vecindad POST prune {}:\n{}".format(len(vecindad),vecindad))

        # Se aplica la función objetivo sobre cada vecino
        vecindad_fitnesses = np.empty(len(vecindad))
        if verbose:
            print("Total of {} unique neighbors generated".format(len(vecindad)))
        for i in range(len(vecindad)):
            if verbose and i%(len(vecindad)//10) == 0:
                print("Calculating objective function ({}/{}) ...".format(i,len(vecindad)))
            _, fitness_value, fitness_time = objfunc.fitness_heat(fitness_lib,"",instance,vecindad[i])
            total_time += fitness_time
            vecindad_fitnesses[i] = fitness_value
            
        n_eval += len(vecindad)
        # print("vecindad_fitnesses:\n",vecindad_fitnesses)
        # print("n_eval:",n_eval)
        # print("total_time:",total_time)
        
        # Se cogen los N mejores y se añaden a los actuales
        ordered_indexes = np.argsort(vecindad_fitnesses)
        # print("ordered_indexes from new:\n",ordered_indexes)
        new_current_solutions = current_solutions
        new_current_fitnesses = current_fitnesses
        # print("new_current_solutions PRE:\n",new_current_solutions)
        # print("new_current_fitnesses PRE:\n",new_current_fitnesses)
        new_current_solutions = np.concatenate([new_current_solutions,vecindad[ordered_indexes[0:N]]])
        new_current_fitnesses = np.concatenate([new_current_fitnesses,vecindad_fitnesses[ordered_indexes[0:N]]])
        # print("new_current_solutions POST\n:",new_current_solutions)
        # print("new_current_fitnesses POST\n:",new_current_fitnesses)
        
        
        # Se cogen los N mejores de la unión
        ordered_indexes = np.argsort(new_current_fitnesses)
        # print("ordered_indexes from new added:",ordered_indexes)
        new_current_solutions = new_current_solutions[ordered_indexes[0:N]]
        new_current_fitnesses = new_current_fitnesses[ordered_indexes[0:N]]
        # print("new_current_solutions POST POST:",new_current_solutions)
        # print("new_current_fitnesses POST POST:",new_current_fitnesses)
        
        # Si los nuevos N mejores son iguales que los viejos N mejores, no ha habido mejora, terminar
        if np.all(new_current_solutions == current_solutions):
            mejora = False
        else:
            current_solutions = new_current_solutions
            # print("current_solutions updated:",current_solutions)


    ordered_indexes = np.argsort(vecindad_fitnesses)
    if verbose:
        print("Ejecución terminada!\nEvaluations used: {}, time used: {}, best_fitness: {}".format(n_eval,round(total_time,2),current_fitnesses[ordered_indexes]))

    return current_fitnesses[ordered_indexes],current_solutions[ordered_indexes],n_eval,total_time

