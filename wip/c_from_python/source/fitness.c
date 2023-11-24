/* heat_s.c 

     Difusion del calor en 2 dimensiones      Version aislada

     Se analizan las posiciones de los chips en una tarjeta, para conseguir la temperatura minima
     de la tarjeta. Se utiliza el metodo de tipo Poisson, y la tarjeta se discretiza en una rejilla 
     de puntos 2D.
     
     Entrada: card > la definicion de la tarjeta y la configuración a simular
     Salida: la temperatura media
        Si se indica un 1 por parámetro, genera los siguietes ficheros:
	      card.chips: situacion termica inicial
        card.res: la situacion termica final
 
     defines.h: definiciones de ciertas variables y estructuras de datos

     Compilar con estos dos ficheros: 
       diffusion.c: insertar calor, difundir y calcular la temperatura media hasta que se estabilice
       faux.c: ciertas funciones auxiliares

************************************************************************************************/

#include <stdio.h>
#include <values.h>
#include <time.h>
#include <stdlib.h>
#include <math.h>

#include "defines.h"
#include "faux.h"
#include "diffusion.h"

/************************************************************************************/
void init_grid_chips (int conf, struct info_param param, struct info_chips *chips, int **chip_coord, float *grid_chips)
{
  int i, j, n;

  for (i=0; i<NROW; i++)
  for (j=0; j<NCOL; j++)  
    grid_chips[i*NCOL+j] = param.t_ext;

  for (n=0; n<param.nchip; n++)
  for (i = chip_coord[conf][2*n]   * param.scale; i < (chip_coord[conf][2*n] + chips[n].h) * param.scale; i++)
  for (j = chip_coord[conf][2*n+1] * param.scale; j < (chip_coord[conf][2*n+1]+chips[n].w) * param.scale; j++) 
    grid_chips[(i+1)*NCOL+(j+1)] = chips[n].tchip;
}

/************************************************************************************/
void init_grids (struct info_param param, float *grid, float *grid_aux)
{
  int i, j;

  for (i=0; i<NROW; i++)
  for (j=0; j<NCOL; j++) 
    grid[i*NCOL+j] = grid_aux[i*NCOL+j] = param.t_ext;
}

/************************************************************************************/
/************************************************************************************/
int fitness (int save_results, char * card_file, double* Tmean_out, double* Tej_out)
{
  struct info_param param;
  struct info_chips *chips;
  int	 **chip_coord;

  float *grid, *grid_chips, *grid_aux;  
  struct info_results BT;
  
  int    conf, i;
  struct timespec t0, t1;
  double tej, Tmean;

  clock_gettime (CLOCK_REALTIME, &t0);

  read_data (card_file, &param, &chips, &chip_coord);
  
  grid = malloc(NROW*NCOL * sizeof(float));
  grid_chips = malloc(NROW*NCOL * sizeof(float));
  grid_aux = malloc(NROW*NCOL * sizeof(float));

  BT.bgrid = malloc(NROW*NCOL * sizeof(float));
  BT.cgrid = malloc(NROW*NCOL * sizeof(float));
  BT.Tmean = MAXDOUBLE;
  
  // Inintial values for grid
  init_grid_chips (0, param, chips, chip_coord, grid_chips);
  init_grids (param, grid, grid_aux);

  // Thermal injection/disipation until convergence (t_delta or max_iter)
  Tmean = calculate_Tmean (param, grid, grid_chips, grid_aux);

  clock_gettime (CLOCK_REALTIME, &t1);

  if (save_results)
  {
    // Processing configuration results 
    results_conf (Tmean, param, grid, grid_chips, &BT);

    // writing best configuration results
    results (param, &BT, card_file);
  }
  
  tej = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec)/(double)1e9;  
  *Tmean_out = Tmean;
  *Tej_out = tej;
  // printf ("Tmean: %1.2f\n", Tmean);
  // printf ("Time: %1.3f s\n", tej);

  free (grid);free (grid_chips);free (grid_aux);
  free (BT.bgrid);free (BT.cgrid);
  free (chips);
  free (chip_coord);

  return (0);
}

