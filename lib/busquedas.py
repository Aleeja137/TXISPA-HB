import solutions
import objfunc
import vecindades

def random_search(instance, num_solutions) -> list:
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    # print("Debug 1: Pre initialize")
    fitness_lib = objfunc.initialize_fitness()
    
    best_sol_codif = solutions.random_solution(instance)
    _, best_sol_value, total_time = objfunc.fitness_heat(fitness_lib,"",instance,best_sol_codif,salida=False)

    sol_actual_codif = best_sol_codif.copy()
    sol_actual_value = best_sol_value

    for i in range(num_solutions):
        print("Solution",i)
        sol_actual_codif = solutions.random_solution(instance)
        _, sol_actual_value, sol_actual_time = objfunc.fitness_heat(fitness_lib,"",instance,sol_actual_codif,salida=False)
        total_time += sol_actual_time
        # print(sol_actual_value)
        if sol_actual_value <= best_sol_value:
            best_sol_value = sol_actual_value
            best_sol_codif = sol_actual_codif
            # print(best_sol_codif)
            # print(best_sol_value)

    return best_sol_value,best_sol_codif, total_time

def best_first_move(instance, candidato, fitness_candidato, max_eval, n_eval):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    current_sol = candidato.copy()
    current_fitness = fitness_candidato

    objective_function_HEAT = objfunc.initialize_fitness()
    iter_count = n_eval
    mejora = True
    total_time = 0

    # Mientras no sobrepasen las iteraciones o se encuentre mejora
    while (iter_count < max_eval and mejora):
        # Se obtiene la vecindad
        vecindad = vecindades.move_1(instance,current_sol)

        # Se recorren los vecinos hasta encontrar uno con mejor solucion
        sol_ind = 0
        encontrado = False

        # Se recorren los vecinos hasta encontrar el primero que mejore la función fitness
        while sol_ind < len(vecindad) and not encontrado:
            if (iter_count > max_eval):
                break
            # Se calcula el fitness de uno de los vecinos
            # print("Vecino",sol_ind," es",vecindad[sol_ind])
            _,new_fitness,new_time = objfunc.fitness_heat(objective_function_HEAT,"",instance,vecindad[sol_ind])
            total_time += new_time
            iter_count = iter_count + 1
            # Si mejora el fitness se sigue ese camino
            if (new_fitness < current_fitness):
                print("Fitness mejorado de {} a {}".format(current_fitness,new_fitness))
                current_fitness = new_fitness
                current_sol = vecindad[sol_ind].copy()
                encontrado = True
            sol_ind = sol_ind + 1

        # Si no se ha encontrado un vecino que mejore, no merece seguir buscando
        if not encontrado:
            mejora = False

    best_fitness = current_fitness
    best_solution = current_sol
    return best_fitness,best_solution,iter_count, total_time

def local_search(instance,max_eval):
    return 1