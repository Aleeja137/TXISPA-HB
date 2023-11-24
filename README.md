# TXISPA-HB
 Heurísticos de Búsqueda sobre el problema de distribución de chips en una placa. Los chips generan calor, y la placa se enfría en el centro. Se busca la temperatura media más baja.

# Implementación actual

# Compilar código C como librería
gcc -shared -o fitness.so -fPIC fitness.c diffusion.c faux.c -lrt

# TODO
Cambiar función C para que obtenga una lista de posiciones en lugar de un fichero (read_data e init_grid_chips)
Pasar todo a np.arrays
Pasar las tuplas a listas
Ordenar github

# Mejoras
Usar función objetivo 2 para frontera pareto
Usar función objetivo 2 para evaluar función objetivo C sobre un subconjunto de la vecindad, ya que toma mucho tiempo