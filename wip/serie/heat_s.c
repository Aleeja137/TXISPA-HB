/* heat_s.c 

     Difusion del calor en 2 dimensiones      Version en serie

     Se analizan las posiciones de los chips en una tarjeta, para conseguir la temperatura minima
     de la tarjeta. Se utiliza el metodo de tipo Poisson, y la tarjeta se discretiza en una rejilla 
     de puntos 2D.
     
     Entrada: card > la definicion de la tarjeta y las configuraciones a simular
     Salida: la mejor configuracion y la temperatura media
	      card_s.chips: situacion termica inicial
        card_s.res: la situacion termica final
 
     defines.h: definiciones de ciertas variables y estructuras de datos

     Compilar con estos dos ficheros: 
       diffusion.c: insertar calor, difundir y calcular la temperatura media hasta que se estabilice
       faux.c: ciertas funciones auxiliares

************************************************************************************************/

#include <stdio.h>
#include <values.h>
#include <time.h>

#include "defines.h"
#include "faux_s.h"
#include "diffusion_s.h"

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
int main (int argc, char *argv[])
{
  struct info_param param;
  struct info_chips *chips;
  int	 **chip_coord;

  float *grid, *grid_chips, *grid_aux;  
  struct info_results BT;
  
  int    conf, i;
  struct timespec t0, t1;
  double tej, Tmean;

 // reading initial data file
  if (argc != 2) {
    printf ("\n\nERROR: needs a card description file \n\n");
    exit (-1);
  } 

  read_data (argv[1], &param, &chips, &chip_coord);

  printf ("\n  ===================================================================");
  printf ("\n    Thermal diffusion - SERIAL version ");
  printf ("\n    %d x %d points, %d chips", RSIZE*param.scale, CSIZE*param.scale, param.nchip);
  printf ("\n    T_ext = %1.1f, Tmax_chip = %1.1f, T_delta: %1.3f, Max_iter: %d", param.t_ext, param.tmax_chip, param.t_delta, param.max_iter);
  printf ("\n  ===================================================================\n\n");
  
  clock_gettime (CLOCK_REALTIME, &t0);

  grid = malloc(NROW*NCOL * sizeof(float));
  grid_chips = malloc(NROW*NCOL * sizeof(float));
  grid_aux = malloc(NROW*NCOL * sizeof(float));

  BT.bgrid = malloc(NROW*NCOL * sizeof(float));
  BT.cgrid = malloc(NROW*NCOL * sizeof(float));
  BT.Tmean = MAXDOUBLE;
  
  // loop to process chip configurations
  for (conf=0; conf<param.nconf; conf++)
  {
    // inintial values for grids
    init_grid_chips (conf, param, chips, chip_coord, grid_chips);
    init_grids (param, grid, grid_aux);

    // main loop: thermal injection/disipation until convergence (t_delta or max_iter)
    Tmean = calculate_Tmean (param, grid, grid_chips, grid_aux);
    printf ("  Config: %2d    Tmean: %1.2f\n", conf + 1, Tmean);

    // processing configuration results 
    results_conf (conf, Tmean, param, grid, grid_chips, &BT);
  }

  clock_gettime (CLOCK_REALTIME, &t1);
  tej = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec)/(double)1e9;
  printf ("\n\n >>> Best configuration: %2d    Tmean: %1.2f\n", BT.conf + 1, BT.Tmean); 
  printf ("   > Time (serial): %1.3f s \n\n", tej);
  // writing best configuration results
  results (param, &BT, argv[1]);
  

  free (grid);free (grid_chips);free (grid_aux);
  free (BT.bgrid);free (BT.cgrid);
  free (chips);
  for (i=0; i<param.nconf; i++) free (chip_coord[i]);
  free (chip_coord);

  return (0);
}

