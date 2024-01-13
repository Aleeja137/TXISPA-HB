import lib.objfunc
import sys
import numpy as np

def best_first(instance, vecindad, n_eval, max_eval, candidato, fitness_candidato,objective_function_HEAT):
    sol_ind = 0
    encontrado = False
    total_time = 0
    
    # inicializamos el mejor como el actual
    best_fitness = fitness_candidato
    best_candidato = candidato
    
    # Se recorren los vecinos hasta encontrar el primero que lo mejore
    while sol_ind < len(vecindad) and not encontrado and n_eval < max_eval:
        _,new_fitness,new_time = lib.objfunc.fitness_heat(objective_function_HEAT,"",instance,vecindad[sol_ind])
        total_time += new_time
        n_eval += 1
        if new_fitness < fitness_candidato:
            encontrado = True
            best_fitness = new_fitness
            best_candidato = vecindad[sol_ind]
        sol_ind +=1
    
    # En caso de no encontrar uno que mejore, devolvemos el actual con encontrado=False
    return encontrado,n_eval,best_fitness,best_candidato,total_time

def best_greedy(instance, vecindad, n_eval, max_eval, candidato, fitness_candidato,objective_function_HEAT):

    encontrado = True
    sol_ind = 0
    total_time = 0
    
    # Inicializa los peores valores posibles
    best_fitness = sys.float_info.max
    best_candidato = np.empty(len(candidato))

    # Evalúa TODOS los vecinos y se queda con el mejor
    while sol_ind < len(vecindad) and n_eval < max_eval:
        _,new_fitness,new_time = lib.objfunc.fitness_heat(objective_function_HEAT,"",instance,vecindad[sol_ind])
        total_time += new_time
        n_eval += 1
        if new_fitness < best_fitness:
            best_fitness = new_fitness
            best_candidato = vecindad[sol_ind]
        sol_ind += 1
    
    # Si el mejor de los vecinos es mejor que el actual, se devuelve, sino se devuelve el actual con encontrado=False
    if fitness_candidato < best_fitness:
        best_fitness = fitness_candidato
        best_candidato = candidato
        encontrado = False
    
    # Si el mejor de los vecinos no es mejor que el actual, se devuelve el actual con encontrado=False
    return encontrado,n_eval,best_fitness,best_candidato,total_time

def random_neigh(instance, vecindad, n_eval, max_eval, candidato, fitness_candidato,objective_function_HEAT):
    n_vecinos = vecindad.shape[0]
    encontrado = False
    rand_neigh_index = np.random.randint(0,n_vecinos)
    
    best_fitness = fitness_candidato
    best_candidato = candidato
    
    _,new_fitness,new_time = lib.objfunc.fitness_heat(objective_function_HEAT,"",instance,vecindad[rand_neigh_index,:])
    
    if new_fitness < best_fitness:
        encontrado = True
        best_fitness = new_fitness
        best_candidato = vecindad[rand_neigh_index,:]
        
    return encontrado,n_eval,best_fitness,best_candidato,new_time
    