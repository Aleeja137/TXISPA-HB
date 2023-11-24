# TXISPA-HB  
Heurísticos de Búsqueda sobre el problema de distribución de chips en una placa. Los chips generan calor, y la placa se enfría en el centro. Se busca la temperatura media más baja.  
  
# Implementación actual  
Vecindades  
Random Search  
Best first (búsqueda local viene casi hecho con esto)  
Visualizar placa  
Fución objetivo  
Todo hecho intentando seguir una estructura modular, viendo de cara al futuro  

# Compilar código C como librería  
gcc -shared -o fitness.so -fPIC fitness.c diffusion.c faux.c -lrt  
  
# TODO    
Arreglar memory corruption (C free)   (Trabajando en ello con valgrind y gdb)
  
# Mejoras planeadas    
## Mejoras principales  
Local Beam search  
Random restart local search (OpenMP/Python multiprocessing)  
Poblacionales (differential evolution and/or genetic algorithm)  
Solución inicial parecido a GRASP (poniendo los más grandes/más calientes en el cooling zone)  
Función objetivo secundaria (wirelength) para pareto (parecido al lab)  
VNS ya que la temperatura media cambia poco con vecindad move_1  
Simulated annealing para Insertar individuos aleatorios (parecido al lab)  

## mejoras secundarias  
Visualizar recorrido en las búsquedas (vídeo/GIF)  
Visualizar zonas de enfriamiento  
Visualizar calor placa cada iteración con el mejor candidato  