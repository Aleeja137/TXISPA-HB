# TXISPA-HB  
Heurísticos de Búsqueda sobre el problema de distribución de chips en una placa. Los chips generan calor, y la placa se enfría en el centro. Se busca la temperatura media más baja.  
  
# Implementación actual    
Local search y random_search  
Local beam search  
Genetic Algorithm  
Simulated annealing  
VNS/VND  
  
Vecindades move_1 y swap_2  
Poblacional cross_over y mutación  
  
Función objetivo secundaria con manhattan distance  
  
Neighbor selectors de best_firts, best_greedy y random  
  
Visualizar placa   
Fución objetivo  
Todo hecho intentando seguir una estructura modular, viendo de cara al futuro  

# Compilar código C como librería  
gcc -shared -o fitness.so -fPIC fitness.c diffusion.c faux.c -lrt  
  
# Mejoras planeadas    
## Mejoras principales  
Random restart local search (OpenMP/Python multiprocessing)  
Simulated annealing para Insertar individuos aleatorios en Pareto (parecido al lab)  
Una especie de Tabu Search para evitar ejecutar la función objetivo en soluciones ya visitadas (en cualquier búsqueda)  
  
## Mejoras secundarias  
Visualizar recorrido en las búsquedas (vídeo/GIF)  
Visualizar zonas de enfriamiento  
Visualizar calor placa cada iteración con el mejor candidato  

# Debugging  
conda activate /path/to/HB-env
cd source
gcc -o fitness  fitness.c diffusion.c faux.c 
valgrind -v --leak-check=full ./fitness