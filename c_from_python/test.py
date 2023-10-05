import ctypes

# Cargar la librería compartida
fitness_lib = ctypes.CDLL("lib/fitness.so")

# Hay que definir el tipo de los argumentos que se le pasan y el del resultado (irrelevante)
fitness_lib.fitness.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]
fitness_lib.fitness.restype = ctypes.c_int

# Preparar las variables de argumento
input_string = "data/card".encode('utf-8')  # Necesario convertirlo a char* para C
input_int = 0 # 1 Para generar fichero de salida
Tmean = ctypes.c_double()
Tej = ctypes.c_double()

# Ejecución
fitness_lib.fitness(input_int, input_string, ctypes.byref(Tmean), ctypes.byref(Tej))

# Comprobación
print(f"Output Tmean: {Tmean.value}")
print(f"Output Tej: {Tej.value}")
