import ctypes

def initialize_fitness():
    # Cargar la librería 
    objective_function_HEAT = ctypes.CDLL("lib/fitness.so")

    # Definir el tipo de los argumentos que se le pasan (relevante) y el del resultado (irrelevante)
    #objective_function_HEAT.fitness.argtypes=  save_results   card_file,      scale         nchip         t_ext          tmax_chip       t_delta          max_iter
    #                                           chip_info                     chip_positions                Tmean_out                       Tej_out)
    objective_function_HEAT.fitness.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_int,
                                                ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
    
    objective_function_HEAT.fitness.restype = ctypes.c_int
    return objective_function_HEAT
    
def fitness_heat(objective_function_HEAT, filepath, instance, solucion, salida = False):    
    # Preparar las variables de argumento
    if not salida:
        input_int = 0
    else:
        input_int = 1
        
    input_string = filepath.encode('utf-8')  # Necesario convertirlo a char* para C
    
    scale,nconf,nchip,max_iter,n_pos,t_ext,tmax_chip,t_delta,tam,chip_info = instance
    
    guardar_result = ctypes.c_int(input_int)
    fichero_result = ctypes.c_char_p(input_string)
    scale = ctypes.c_int(scale)
    nchip = ctypes.c_int(nchip)
    t_ext = ctypes.c_float(t_ext)
    tmax_chip = ctypes.c_float(tmax_chip)
    t_delta = ctypes.c_float(t_delta)
    max_iter_value = ctypes.c_int(max_iter)
    
    # Crear arrays de ctypes para chip_info y solucion
    chip_info_array = (ctypes.c_int * len(chip_info))(*chip_info)
    solucion_array = (ctypes.c_int * len(solucion))(*solucion)
    
    # Crear variables ctypes para Tmean y Tej
    Tmean = ctypes.c_double()
    Tej = ctypes.c_double()

    # print("-----PYTHON-----")
    # print("Save_results:",guardar_result)
    # print("scale:",scale)
    # print("nchip:",nchip)
    # print("t_ext:",t_ext)
    # print("tmax_chip:",tmax_chip)
    # print("t_delta:",t_delta)
    # print("max_iter_value:",max_iter_value)
    # print("----------------")
    
    # Ejecución
    resultado = objective_function_HEAT.fitness(
        guardar_result, fichero_result, scale, nchip, t_ext, tmax_chip, t_delta, max_iter_value,
        chip_info_array, solucion_array, ctypes.byref(Tmean), ctypes.byref(Tej)
    )
    
    return resultado,Tmean.value,Tej.value
