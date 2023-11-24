import numpy as np

def valid_solution(instance, solution):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    if np.all(solution == 0):
        return False
    
    n_filas = n_pos*2
    n_columnas = n_pos

    # Verificar que ningún chip se salga de la placa
    for i in range(nchip):
        x = solution[i*2]
        y = solution[i*2+1]
        ancho = chip_info[i*3]
        alto  = chip_info[i*3+1]

        if x < 0 or x + ancho > n_filas or y < 0 or y + alto > n_columnas:
            return False

    # Verificar que ningún chip solape con otro chip
    for i in range(nchip - 1):
        x1 = solution[i*2]
        y1 = solution[i*2+1]
        ancho1 = chip_info[i*3]
        alto1  = chip_info[i*3+1]

        for j in range(i + 1, nchip):
            x2 = solution[j*2]
            y2 = solution[j*2+1]
            ancho2 = chip_info[j*3]
            alto2  = chip_info[j*3+1]

            if (x1 < x2 + ancho2 and x1 + ancho1 > x2 and
                y1 < y2 + alto2 and y1 + alto1 > y2):
                return False 

    return True  
