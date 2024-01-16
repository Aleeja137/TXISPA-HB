# Motivación, estado actual etc  
En los últimos años la era digital ha tomado la tendencia de producir chips de pequeño tamaño y coste, capaces de relativamente mayor cómputo de manera local, como mejor opción que el cómputo centralizado en grandes clusters. Esto se debe a varios motivos, como la recopilación, almacenamiento y tratamiento de datos privados; sistemas con un único punto de ataque o debilidad (sistemas monolíticos); dependencias de la congestión de red; contratación de servicios de terceros, etc.

Por tanto, es necesario diseñar y fabricar chips de diversos tamaños, y de diversas funcionalidades. Por otro lado, los chips y placas convencionales (CPUs, GPUs, tarjetas de red) también han sufrido una revolución en cuento a dimensiones y rendimiento. Sin duda es un mercado muy competitivo, donde se busca el mejor rendimiento al menor coste. 

Por tanto, un aspecto esencial en este sector es el diseño. Algunas empresas están optando por introducir los metaheurísticos y las redes neuronales profundas en la fase de diseño, buscando reducir los gastos y el tiempo de diseño, así como mejorar el rendimiento, buscando soluciones que se diferencian de los estándares establecidos durante décadas. 

Uno de los problemas en el diseño es determinar la mejor distribución de los componentes en una placa. Este problema se conoce como VLSI (Very Large Scale Integration) placement. Este concepto nació en la década de los 70, cuando cabían cada vez más transistores en los chips, y los encargados hasta el momento de diseñar los chips (ingenieros eléctricos, físicos y fábricas del ámbito), no conocían cómo distribuir los componentes de manera eficiente. Fue entonces cuando Carver Mead y Lynn Conway introdujeron el concepto en su libro titulado 'Introduction to VLSI Systems', que actuó como puente entre ingenieros eléctricos e ingenieros informáticos. Fue toda una revolución, estudiantes universitarios pudieron diseñar chips y tener los prototipos fabricados en pocas semanas.

Hoy en día se fusiona la metaheurística con VLSI, para así obtener mejores resultados con menos coste. Concretamente, con el paso 'floorplanning', que consiste en determinar el tamaño, las posiciones, los módulos, etc. En un chip, cumpliendo ciertos parámetros como porcentaje de espacio ocupado, densidad, interconectividad, longitud de cable usado, etc. Es un problema por definición NP-Hard (la representación más cómoda es B*-tree, según [1], por tanto, y según el mismo paper, es NP-Hard). No obstante, hay otras representaciones mencionados en [2]. (No los entiendo del todo, no sé si mencionarlos).

Existen estudios que tratan de evaluar técnicas de metaheurística como algoritmos genéticos, (Hybrid) Simulated Annealing, Particle Swarm Optimization, Ant Colony Optimization [2] y Tabu Search [4], es decir, los métodos más conocidos. Otros incluso usan métodos más directos, como la búsqueda local [1]. Hay otros estudios que usan Symbiosis Adaptativa [3], siguiendo el principio de que algoritmos inspirados en la naturaleza tienen alto rendimiento en problemas multiobjetivo como este, siendo NP-Hard. Independientemente de los resultados, son estudios de 2005-2016, estudios recientes que pueden significar una reducción en tiempo, recursos y un aumento en rendimiento. Beneficio para las empresas y usuarios, y para el medio ambiente. 

Incluso se ha llegado a introducir la 'Inteligencia Artificial', usando redes neuronales profundas y machine learning. Esta idea ya estaba presente en 1985, por [Robert S. Kirk](https://www.semanticscholar.org/paper/The-impact-of-AI-technology-on-VLSI-design-Kirk/e78da5cd108f6f469067f94ed7c63a11daec1bf4), aunque es hoy en día cuando tenemos la capacidad de cómputo para realmente llevarlo a cabo. Es posible utilizar AI/ML en las distintas fases de diseño, en la simulación del circuito, en el diseño de las arquitecturas, en el SoC, etc [5]. Sobretodo se implementan estos servicios en las aplicaciones CAD usadas para el diseño VLSI. Unos ejemplos son DREAMplace [6], ABCDplace [7], y AutoDMP [8] (la nueva tecnología de NVidia) por ejemplo.

En conclusión, es un campo de investigación ya establecido desde el crecimiento exponencial de la cantidad de transistores que podíamos poner en un chip, y aunque la idea de asistir a la tarea con metaheurísticos y AI/ML es casi igual de antigua, es con los recursos de hoy en día cuando podemos notar una mejora notable. Existen decenas de aplicaciones y papers publicados al respecto, los mencionados aquí son unos pocos de entre los más destacados, es una rama de investigación candente.

# Presentación del problema  
En nuestro caso, el problema es algo más relajado, ya que solo es un problema mono-objetivo, aunque el objetivo es la mejor disipación de calor, algo distinto a VLSI, pero muy relacionado en cuanto a representación y método de resolución. 

Contamos con una placa de tamaño variable, de proporciones 100x200. Este tamaño es variable, ya que cada eje se multiplica por el valor de la variable 'scale', integer de entre 1 y 12. Por tanto, podemos cambiar el tamaño de la placa desde (100,200) hasta (1200,2400). Contamos con varios parámetros del problema:
   
    - scale: determina el factor de escala de la placa
    - nchip: cantidad de chips a incluir en la placa
    - t_ext: temperatura del exterior
    - tmax_chip: temperatura máxima de los chips
    - delta: valor límite de diferencia para considerar la convergencia
    - max_iter: valor límite de iteraciones para considerar la convergencia
    - npos: número de posiciones en el chip
    - [chip_info]: lista con información de dimensiones y temperatura de cada chip
    - [chip_pos]: lista con información de las posiciones de los chips (opcional)

El programa cuenta con un 'core' que se encarga de hacer el cálculo de la función objetivo. Este core está escrito en C, y es parte del proyecto final de la asignatura Sistemas de Cómputo Paralelo. El resto del programa está escrito en Python, que se encarga de aplicar los metaheurísticos. De cara a relajar el problema, manteniendo aún así el tamaño de la placa (y por tanto el tiempo de ejecución del core), se introdujo el parámetro npos.

Si scale tiene valor 4 por ejemplo, el tamaño de la placa es (400,800). npos puede tener el valor 200 por ejemplo. Por tanto, el código python, encargado del apartado de metaheurística, tendrá en cuenta el tamaño de la placa como (200,400), aunque a la hora de ejecutar la función objetivo seguirá respetándose el tamaño real. Si cambiamos scale a 6, la placa tendrá tamaño (600,1200), aunque el ćódigo python seguirá tratando con una placa (200,400), Por tanto, aumentamos el tiempo de cómputo de la función objetivo, aunque el tiempo de ejecución del metaheurístico sigue igual. El parámetro npos nos proporciona un grado extra de libertad a la hora de planear la experimentación.

La placa se enfría en la parte central del eje más corto, e inyecta calor en las posiciones de los chips. Para la difusión de calor se utiliza un algoritmo algo arbitrario, sin muchas raíces en la literatura. Se hace un barrido de todo el chip, haciendo una combinación lineal del calor de las celdas adjacentes en cada celda. Si la temperatura media no ha cambiado por encima de delta o si se han hecho más de max_iter barridas, termina.

Lo que se busca es la distribución de los chips que obtenga la menor temperatura media. Es un problema de minimización.

# Approach de solución
La codificación por la que hemos optado es una lista de ints. Ya que los parámetros de entrada mencionados anteriormente son estáticos para cada ejecución (menos la lista de posiciones), la solución tendrá un tamaño fijo de 2\*nchip*int. cada elemento par y su siguiente representan la **posición** de un chip. Ojo, posición según npos, no según scale. El programa traduce los valores para la ejecución del core.

Con esta codificación, a parte de que es muy cómoda con np.arrays y ocupa poco espacio, permite operaciones de vecindad como move_1, swap, insert, etc.

Están implementados métodos 'tontos' como random_search y local_search, entre otros (local_beam_search, VNS, VND, etc).

# Benchmark set  
De cara a preparar la experimentación para algoritmos futuros, hemos creado un conjunto de 25 casos que forman un benchmark. Los 25 casos pueden colocarse en una matriz 5x5. Cada eje de la matriz corresponde a un nivel de nificultad ascendente en uno de dos aspectos: dificultad de core en el eje vertical, y dificultad de metaheurísticos en el eje horizontal.

Los niveles se han llamado arbitrariamente así:
    
    - 1: very easy
    - 2: easy
    - 3: medium
    - 4: hard
    - 5: very hard

Por supuesto que podrían haberse dividido en más o menos columnas/filas, pero consideramos que 25 casos son suficientes.

De cara a la dificultad del core, lo único necesario es incrementar el scale. El scale tiene estos valores: [1,3,6,9,12].

De cara a la dificultad de los metaheurísticos, hay varios factores que incrementan la dificultad. Primero, algunos parámetros se han dejado fijos, como t_ext, tmax_chip, delta y max_iter. Modificar estos valores no incrementa la dificultad, y tenerlos variando dificultaría la comparativa de resultados entre algoritmos.

Por otro lado, npos, la nchip, los tamaños y formas de los chips, y las temperaturas de los chips, son todo factores que pueden incrementar la dificultad. Como no podemos hacer muchísimos casos de benchmark, he llegado a una relación entre estas variables.

1. npos representa cierto porcentaje de las posiciones. Para cada nivel de dificultad en el eje horizontal, npos tomaba un porcentaje de 100*scale. Los porcentajes son [10,20,40,50,100]. Según la fila, npos tiene su propio valor.
2. Las formas se van complicando. Al principio tenemos chips cuadrados, proporción 1:1. En el segundo nivel, tenemos chips de proporciones 2:2,2:1,1:2 y 1:1 (no se pueden rotar). En el tercero 3:3,3:2,etc. Así tomando valores de 1 hasta 5, depende del nivel de dificultad. 
3. La temperatura ronda a un valor medio, aunque la desviación es mayor a medida que aumenta la dificultad. La temperatura media es el punto medio entre la temperatura del exterior y la temperatura de chip máxima. La desviación es un porcentaje (arriba y abajo) de la siguiente lista: [5,10,20,30,40].
4. Se busca un porcentaje de ocupación cada vez más elevado según el nivel de dificultad. El nivel de ocupación sigue la misma lista que la desviación de la temperatura, con una desviación igual o menor al 1%, ya que no se puede asegurar que sea posible dar con el valor de ocupación exacto generando chips aleatoriamente.  
A medida que aumenta npos, nchip aumenta exponencialmente para cumplir con el porcentaje de ocupación deseado, así que he aumentado el tamaño de los chips para evitar eso. Lo consigo multiplicando las proporciones de los chips por un valor según el nivel. Así se consigue que aumente la cantidad de chips moderadamente respentando el espacio libre deseado. Un chip pasa de ser de tamaño (x,y) a (zx,zy).

Todo esto lo he hecho usando un programa en python, así que los valores son regulables, pero he visto que la mejor combinación es esta (por ahora).

Después, usando el generador de soluciones aleatorias, he creado una solución incial a cada benchmark. En los niveles de dificultad metaheurística altos, he tenido que crear a mano esas soluciones iniciales, ya que no conseguía crear una aleatoriamente. Esto es una mejora necesaria, ya que el estado inicial y su aleatoriedad son aspectos importantes de la metaheurística, y el problema debería poder crear soluciones iniciales aleatorias.

Lo que bsucamos es que los algoritmos poco elaborados o 'tontos' (como el random search), funcionen muy bien en los niveles de dificultad bajos, pero rindan peor que algoritmos elaborados en dificultades elevadas.

Cada caso está caracterizado por su nombre, benchmark_x_y.dat, donde x representa la dificultad de core (eje vertical) e y representa la dificultad metaheurística (eje horizontal). Ambos valores van de 1 a 5. Todos se encuentran dentro de la carpeta data. Se encuentran imágenes de las soluciones iniciales sugeridas a cada benchmark en imag/benchmark_x_y.png

Ejemplo: data/benchmark_2_1.dat

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

# Mejoras planeadas    
## Mejoras principales  
Generar soluciones iniciales aleatorias en cualquier benchmark
Random restart local search (OpenMP/Python multiprocessing)  
Simulated annealing para Insertar individuos aleatorios en Pareto (parecido al lab)  
Una especie de Tabu Search para evitar ejecutar la función objetivo en soluciones ya visitadas (en cualquier búsqueda)

  
## Mejoras secundarias  
Visualizar recorrido en las búsquedas (vídeo/GIF)  
Visualizar zonas de enfriamiento  
Visualizar calor placa cada iteración con el mejor candidato

# Citas y referencias
[Iñigo Lopez] - inigo.lopez@ehu.eus  
[Olatz Perez (SCP)] - olatz.perezdevinaspre@ehu.eus

[1 - Jianli Chen; Wenxing Zhu; M. M. Ali. A Hybrid Simulated Annealing Algorithm for Nonslicing VLSI Floorplanning](https://ieeexplore.ieee.org/document/5571036)  
[2 - Rajendra Bahadur Singh; Anurag Singh Baghel; Ayush Agarwal. A review on VLSI floorplanning optimization using metaheuristic algorithms](https://ieeexplore.ieee.org/abstract/document/7755508?casa_token=KENIAx15rgUAAAAA:CeqW0axieLPSCxRrJjKelDGgxM3os0biB26L9ee2bJbO7EX79aNVC2ZgadrAndC61Nxv2V8)  
[3 - Lalin L Laudis a, N. Ramadass b, Shilpa Shyam a, R. Benschwartz a, V. Suresh a. An Adaptive Symbiosis based Metaheuristics for Combinatorial Optimization in VLSI](https://www.sciencedirect.com/science/article/pii/S1877050920306621)  
[4 - Prasun Ghosal, Tuhina Samanta, Hafizur Rahaman, Parthasarathi Dasgupta. Recent trends in the Application of Meta-heuristics to VLSI layout design](https://www.researchgate.net/profile/Prasun-Ghosal/publication/220888607_Recent_Trends_in_the_Application_of_Meta-Heuristics_to_VLSI_Layout_Design/links/0c960529671ea60cdd000000/Recent-Trends-in-the-Application-of-Meta-Heuristics-to-VLSI-Layout-Design.pdf)  
[5 - Deepthi Amuru a, Andleeb Zahra a, Harsha V. Vudumula a, Pavan K. Cherupally a, Sushanth R. Gurram a, Amir Ahmad b, Zia Abbas a. AI/ML algorithms and applications in VLSI design and technology](https://www.sciencedirect.com/science/article/abs/pii/S0167926023000901)  
[6 - DREAMplace](https://github.com/limbo018/DREAMPlace?tab=readme-ov-file#publications)  
[7 - Yibo Lin; Wuxi Li; Jiaqi Gu; Haoxing Ren; Brucek Khailany; David Z. Pan. ABDCPlace](https://ieeexplore.ieee.org/document/8982049)  
[8 - AutoDMP](https://developer.nvidia.com/blog/autodmp-optimizes-macro-placement-for-chip-design-with-ai-and-gpus/)   
