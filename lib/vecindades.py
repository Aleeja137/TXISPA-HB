import numpy as np
import itertools
import check

def move_1 (instance, solucion):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    result = np.empty(0)
    
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