import random as rm
import numpy as np
import check

def random_solution(instance):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    solution = np.empty(nchip*2,dtype=np.int32)
    
    valid = False
    while not valid:
        
        for i in range(nchip):
            x = rm.randint(0,n_pos*2)
            y = rm.randint(0,n_pos)
            
            solution[i*2]   = x
            solution[i*2+1] = y
            
        valid = check.valid_solution(instance,solution)
            
    return solution