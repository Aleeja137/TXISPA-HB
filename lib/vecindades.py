import numpy as np
import itertools
import check

def move_1 (instance, solucion):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    result = np.empty(0,dtype=np.int32)
    
    for i in range(nchip):
        x = solucion[2*i]
        y = solucion[2*i+1]
        
        vecino_0 = solucion.copy()
        vecino_1 = solucion.copy()
        vecino_2 = solucion.copy()
        vecino_3 = solucion.copy()
        vecino_4 = solucion.copy()
        vecino_5 = solucion.copy()
        vecino_6 = solucion.copy()
        vecino_7 = solucion.copy()
        
        # Fila superior
        vecino_0[2*i] = (x-1)%(n_pos*2); vecino_0[2*i+1] = (y-1)%n_pos
        vecino_1[2*i] = x              ; vecino_1[2*i+1] = (y-1)%n_pos
        vecino_2[2*i] = (x+1)%(n_pos*2); vecino_2[2*i+1] = (y-1)%n_pos
        
        # Fila media
        vecino_3[2*i] = (x-1)%(n_pos*2); vecino_3[2*i+1] = y
        vecino_4[2*i] = (x+1)%(n_pos*2); vecino_4[2*i+1] = y
        
        # Fila inferior
        vecino_5[2*i] = (x-1)%(n_pos*2); vecino_5[2*i+1] = (y+1)%n_pos
        vecino_6[2*i] = x              ; vecino_6[2*i+1] = (y+1)%n_pos
        vecino_7[2*i] = (x+1)%(n_pos*2); vecino_7[2*i+1] = (y+1)%n_pos
        
        result = np.append(result,[vecino_0.copy(),vecino_1.copy(),vecino_2.copy(),vecino_3.copy(),vecino_4.copy(),vecino_5.copy(),vecino_6.copy(),vecino_7.copy()])
  
    result = result.reshape(len(result)//(nchip*2),nchip*2)  
    
    # Filtrar las soluciones no válidas
    result = result[[check.valid_solution(instance,x) for x in result]]
    
    return result

def swap_2(instance, solucion):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    result = np.empty(0)

    for i in range(nchip):
        for j in range(i + 1, nchip):
            vecino_swap = solucion.copy()

            # Intercambiar la x entre los chips i y j
            vecino_swap[2*i], vecino_swap[2*j] = vecino_swap[2*j], vecino_swap[2*i]
            
            # Intercambiar la y entre los chips i y j
            vecino_swap[2*i+1], vecino_swap[2*j+1] = vecino_swap[2*j+1], vecino_swap[2*i+1]

            # Verificar si la solución resultante es válida
            if check.valid_solution(instance,vecino_swap):
                result = np.append(result,vecino_swap.copy())

    result = result.reshape(len(result)//(nchip*2),nchip*2)  
    return result

def cross_over(instance,pobl,M,proportion = -1):
    # Genera cruces aleatorios entre pares de soluciones, genera M cruces válidos
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    aux = np.random.choice(len(pobl),size=2*M)
    result = pobl
    
    i = 0
    intentos = 0
    while i<M:
        # Se obtienen los elementos a cruzar
        elem1 = aux[2*i]
        elem2 = aux[2*i+1]
        
        # Se calcula la proporción del cruce
        if proportion == -1:
            # Aleatorio entre 0 y 1
            percentage = np.random.random_sample()
            percentage = int(round(percentage*nchip))
        else:
            # Aleatorio entre [proportion..(1-proportion))
            percentage = ((1-proportion)-proportion) * np.random.random_sample() + proportion
            percentage = int(round(percentage*nchip))
            
        # print("elem1 {} es {}".format(elem1,pobl[elem1]))
        # print("elem2 {} es {}".format(elem2,pobl[elem2]))
        # print("Percentage es:",percentage)
        # print("Cogido de elem1 es [0:{}]: {}".format(percentage, pobl[elem1][0:percentage]))
        # print("Cogido de elem2 es [{}:] : {}".format(percentage+1,pobl[elem2][percentage:]))
        # print("El cruce es:",np.concatenate([pobl[elem1][0:percentage],pobl[elem2][percentage:]]))
        
        tmp_result = np.concatenate([pobl[elem1][0:percentage],pobl[elem2][percentage:]])
        intentos += 1
        if check.valid_solution(instance,tmp_result):
            # print(check.valid_solution(instance,tmp_result))
            # print("\n")
            result[i] = tmp_result
            i += 1
            
    print("Para generar {} cruces válidos han hecho falta {} intentos".format(M,intentos))
    return result
        
def mutacion_general(instance, pobl, M):
    # Genera sobre la población M mutaciones diferentes, completamente aleatorias, con un cambio entre el 1-10% 
    # Planeo en un futuro poder modificar estos parámetros según input
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    N = pobl.shape[0] # Número de elementos que tiene la población
    result_pobl = pobl.copy()
    # Sobre qué soluciones será la mutación
    filas = np.random.randint(low=0,high=N,size = M)
    # Sobre qué chips será la mutación
    chips = np.random.randint(low=0,high=nchip,size=M)
    # Sobre coordenada x o y será la mutación
    coordenadas = np.random.randint(low=0,high=1+1,size=M)
    # Sobre qué dirección (+/-) será la mutación
    direcciones = np.random.randint(low=0,high=1+1,size=M)
    direcciones[direcciones==0] = -1
    # En qué porcentage cambiará la solución
    cantidad_low  = 0.01
    cantidad_high = 0.10
    cantidad = (cantidad_high-cantidad_low) * np.random.random_sample(size=M) + cantidad_low
    # Si eseje x o y, se multiplica el valor por la longitud del eje
    cantidad[coordenadas==0] *= 2*n_pos
    cantidad[coordenadas==1] *= n_pos
    
    # print("filas:\n",filas)
    # print("chips:\n",chips)
    # print("coordenadas:\n",coordenadas)
    # print("direcciones:\n",direcciones)
    # print("cantidad:\n",cantidad)
    
    for fila,chip,coord,cant,dir in zip(filas,chips,coordenadas,cantidad,direcciones):
        result_pobl[fila,2*chip+coord] += int(round(cant*dir))
    
    return result_pobl
    