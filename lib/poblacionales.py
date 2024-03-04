import numpy as np
import lib.solutions
import lib.vecindades
import lib.objfunc
import lib.check
import signal as sg
import sys

def genetic_algorithm(instance, cross_function, mutation_function, max_time, max_generations, mut_chance, N, verbose = False):
    if verbose:
        print("cross function: {}\n"
              "mutation function: {}\n"
              "max_time: {}\n"
              "max_generations: {}\n"
              "mut_chance: {}\n"
              "Poblation size: {}\n"
              .format(cross_function.__name__,mutation_function.__name__,max_time,max_generations,mut_chance,N))
    
    fitness_lib = lib.objfunc.initialize_fitness()
    total_time = 0
    
    # Crear población inicial
    pobl = [lib.solutions.random_solution_constructive(instance) for i in range(N)]
    pobl = np.array(pobl)
    pobl_fitness = np.empty(N)
    
    for i in range(N):
        _,new_fitness,new_time = lib.objfunc.fitness_heat(fitness_lib,"",instance,pobl[i])
        pobl_fitness[i] = new_fitness
        total_time += new_time
    
    iter = 1 
    
    # Poner el tiempo máximo permitido
    # sg.signal(sg.SIGALRM, lib.handlers.timeout_handler)
    # sg.alarm(max_time)

    try:
    
        while iter < max_generations and total_time < max_time:
            if verbose:
                print("\033[1;34mGeneration {}\033[0m, total time {}s, pobl:\n{}\npobl_fitnesses:\n{}".format(iter,round(total_time,2),pobl,pobl_fitness))
                
            # Crea la siguiente generación
            next_pobl = lib.vecindades.cross_over(instance,pobl,N, verbose=verbose)
            
            # Aplicar mutación a la nueva generación
            dice = np.random.random_sample()
            if dice <= mut_chance:
                if verbose:
                    print("Mutation occurred!")
                next_pobl = mutation_function(instance,next_pobl,M=N) # Con M=N tenemos un ~85% de candidatos válidos, esto se podría estudiar más adelante
            
            # Calcular fitness para cada individuo de la siguiente generación (si es válido)
            next_pobl_fitness = np.empty(N)
            not_valid_count = 0
            for i in range(N):
                if lib.check.valid_solution(instance,next_pobl[i]):
                    _,new_fitness,new_time = lib.objfunc.fitness_heat(fitness_lib,"",instance,next_pobl[i])
                    next_pobl_fitness[i] = new_fitness
                    total_time += new_time
                else:
                    not_valid_count += 1
                    next_pobl_fitness[i] = sys.float_info.max
            
            if verbose and dice <= mut_chance:
                print("Not valid mutated elements count:",not_valid_count,", {} percent".format(not_valid_count/N))
                
            # Juntar generación actual y siguiente
            pobl         = np.concatenate([pobl,next_pobl])
            pobl_fitness = np.concatenate([pobl_fitness,next_pobl_fitness])
            
            # Evitamos repeticiones, sino converge muy rápido, es posible comentar estas dos líneas si es lo que se busca
            pobl, unique_index = np.unique(pobl,return_index=True,axis=0)
            pobl_fitness = pobl_fitness[unique_index]
            
            # Quedarnos con los mejores N
            ordered_instances = np.argsort(pobl_fitness)
            pobl         = pobl        [ordered_instances[0:N]]
            pobl_fitness = pobl_fitness[ordered_instances[0:N]]
            
            iter += 1

        ordered_pobl = np.argsort(pobl_fitness)
    except TimeoutError as e:
        print("Timeout!")
    finally:
        sg.alarm(0)
        return total_time,pobl[ordered_pobl],pobl_fitness[ordered_pobl],iter
