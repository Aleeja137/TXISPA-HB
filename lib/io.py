import numpy as np

# Lee los parámetros desde fichero
# Devuelve (instance,initial_solution) donde
## instance = scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info
## initial_solution puede ser vacío
def read_params(filepath):    
    # Lee los parámetros de la cabecera
    file = open(filepath,'r')
    params = file.readline().split()
    scale    = int(params[0])
    nchip    = int(params[1])
    max_iter = int(params[5])
    n_pos    = int(params[6])
    nconf    = 1
    t_ext     = float(params[2])
    tmax_chip = float(params[3])
    t_delta   = float(params[4])
    tam = (100*scale)//n_pos
    file.readline()
    
    initial_solution = np.zeros(nchip*2,dtype=np.int32)
    chip_info = np.zeros(nchip*3,dtype=np.int32)
    
    # Lee la información de los chips
    for i in range(nchip):
        chip_info_line = file.readline().split()
        h = int(chip_info_line[0])
        w = int(chip_info_line[1])
        tchip = float(chip_info_line[2])
        chip_info[i*3]   = h
        chip_info[i*3+1] = w
        chip_info[i*3+2] = tchip
        
    # print(chip_info)
    line = file.readline()
    
    # Si hay una solución inicial, la lee
    if not line:
        print("Sin solución inicial")
    else:
        for i in range(nchip):
            chip_position = file.readline().split()
            x = int(chip_position[0])
            y = int(chip_position[1])
            initial_solution[i*2]   = x
            initial_solution[i*2+1] = y
    
    # print(initial_solution)
    instance = scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info
    return instance,initial_solution

# Escribe el fichero de input para el código C 
# (No se debería usar esta función)
def write_card_file(filepath, instance, solution):
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam, chip_info = instance
    
    file = open(filepath,'w')
    
    # Escribir los ficheros cabecera
    file.write("{} {} {} {} {} {} {}\n\n".format(scale,nconf,nchip,t_ext,tmax_chip,t_delta,max_iter))
    
    # Escribe la información de los chips
    for (h,w,tchip) in chip_info:
        file.write("{} {} {}\n".format(h*tam,w*tam,tchip))
    
    file.write("\n")
    
    # Escribe la configuración o solución dada
    for (x,y) in solution:
        file.write("{} {}\n".format(x*tam,y*tam))
    file.write("\n")