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
  // printf("C debug 9.1\n");

  for (i=0; i<NROW; i++)
  for (j=0; j<NCOL; j++)  
    grid_chips[i*NCOL+j] = param.t_ext;

  // printf("C debug 9.2\n");
  // printf("param.chip: %i\n",param.nchip);
  // printf("C debug - param.nchip: %i\n",param.nchip);
  for (n=0; n<param.nchip; n++)
  {
    // printf("chip n : %i\n chip_coord[conf][2*n]: %i, limit: %i\n chip_coord[conf][2*n+1]: %d, limit: %i\n",n, chip_coord[conf][2*n]*param.scale, (chip_coord[conf][2*n] + chips[n].h)*param.scale, chip_coord[conf][2*n+1]*param.scale, (chip_coord[conf][2*n+1]+chips[n].w) * param.scale);
    // for (i = chip_coord[conf][2*n]   * param.scale; i < (chip_coord[conf][2*n] + chips[n].h) * param.scale; i++)
    // {
    //   for (j = chip_coord[conf][2*n+1] * param.scale; j < (chip_coord[conf][2*n+1]+chips[n].w) * param.scale; j++) 
    //   {
    //     // printf("chips %i tchip: %f\n",n,chips[n].tchip);
    //     grid_chips[(i+1)*NCOL+(j+1)] = chips[n].tchip;
    //   }
    // }
    // printf("C debug - chip n : %i\n chip_coord[conf][2*n]: %i, limit: %i\n chip_coord[conf][2*n+1]: %d, limit: %i\n",n, chip_coord[conf][2*n], (chip_coord[conf][2*n] + chips[n].h), chip_coord[conf][2*n+1], (chip_coord[conf][2*n+1]+chips[n].w));
    for (i = chip_coord[conf][2*n]; i < (chip_coord[conf][2*n] + chips[n].h); i++)
    {
      for (j = chip_coord[conf][2*n+1]; j < (chip_coord[conf][2*n+1]+chips[n].w); j++) 
      {
        // printf("chips %i tchip: %f\n",n,chips[n].tchip);
        grid_chips[(i+1)*NCOL+(j+1)] = chips[n].tchip;
      }
    }
  }  
  // printf("C debug 9.3\n");
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
int fitness (int save_results, char * card_file, int scale, int nchip, float t_ext, float tmax_chip, float t_delta, int max_iter, int * chip_info, int * chip_positions, double* Tmean_out, double* Tej_out)
{
  struct info_param param;
  struct info_chips *chips;
  int	 **chip_coord;

  float *grid, *grid_chips, *grid_aux;  
  struct info_results BT;
  
  int    conf, i;
  struct timespec t0, t1;
  double tej, Tmean;
  // printf("-------C--------\n");
  // printf("Save results: %i\nscale: %i\nnchip: %i\nt_ext: %f\ntmax_chip: %f\nt_delta: %f\n",save_results,scale,nchip,t_ext,tmax_chip,t_delta);
  clock_gettime (CLOCK_REALTIME, &t0);
  
  // printf("max_iter: %i\n",max_iter);
  // printf("----------------\n");
  read_data (scale, nchip,t_ext,tmax_chip,t_delta,max_iter,chip_info,chip_positions,&param,&chips,&chip_coord);
  // printf("C debug 8\n");
  
  grid = malloc(NROW*NCOL * sizeof(float));
  // printf("C debug - Size of grid is (%i,%i)\n",NROW,NCOL);
  grid_chips = malloc(NROW*NCOL * sizeof(float));
  grid_aux = malloc(NROW*NCOL * sizeof(float));

  BT.bgrid = malloc(NROW*NCOL * sizeof(float));
  BT.cgrid = malloc(NROW*NCOL * sizeof(float));
  BT.Tmean = MAXDOUBLE;
  // printf("C debug 9\n");
  
  // Inintial values for grid
  init_grid_chips (0, param, chips, chip_coord, grid_chips);
  // printf("C debug 10\n");
  init_grids (param, grid, grid_aux);
  // printf("C debug 11\n");

  // Thermal injection/disipation until convergence (t_delta or max_iter)
  Tmean = calculate_Tmean (param, grid, grid_chips, grid_aux, max_iter);
  // printf("C debug 12\n");

  clock_gettime (CLOCK_REALTIME, &t1);

  if (save_results == 1)
  {
    // Processing configuration results 
    results_conf (Tmean, param, grid, grid_chips, &BT);

    // writing best configuration results
    results (param, &BT, card_file);
  }

  // printf("C debug 13\n");
  
  tej = (t1.tv_sec - t0.tv_sec) + (t1.tv_nsec - t0.tv_nsec)/(double)1e9;  
  *Tmean_out = Tmean;
  *Tej_out = tej;
  // printf ("Tmean: %1.2f\n", Tmean);
  // printf ("Time: %1.3f s\n", tej);
  for (i = 0; i < nchip;i++){
    // printf("C debug - Chip %i size: (%i,%i), position (%i,%i) \n",i,(chips)[i].h,(chips)[i].w,chip_positions[2*i],chip_positions[2*i+1]);
  }

  // printf("C debug 13.2\n");
  if (grid != NULL){
    free (grid);}
  // printf("C debug 14\n");
  if (grid_chips != NULL){
    free (grid_chips);}
  // printf("C debug 15\n");
  if (grid_aux != NULL){
    free (grid_aux);}
  // printf("C debug 16\n");
  if (BT.bgrid != NULL){
    free (BT.bgrid);}
  // printf("C debug 17\n");
  if (BT.cgrid != NULL){
    free (BT.cgrid);}
  // printf("C debug 18\n");
  if (chips != NULL){
    free (chips);}
  // printf("C debug 19\n");
  if (chip_coord != NULL){
    free (chip_coord);}
  // printf("C debug 20\n");

  return (0);
}



int main() {
    int save_results = 0;  // Puedes ajustar este valor según tus necesidades
    char card_file[] = "";  // Nombre del archivo de salida, puedes cambiarlo
    int scale = 10;  // Puedes ajustar este valor según tus necesidades
    int nchip = 6;  // Puedes ajustar este valor según tus necesidades
    float t_ext = 20.0;  // Puedes ajustar este valor según tus necesidades
    float tmax_chip = 160.0;  // Puedes ajustar este valor según tus necesidades
    float t_delta = 0.01;  // Puedes ajustar este valor según tus necesidades
    int max_iter = 10;  // Puedes ajustar este valor según tus necesidades

    // Valores ficticios para chip_info y chip_positions, debes ajustarlos según tus necesidades
    int chip_info[] = {20,30,40,40,50,10,15,60,25,35,43,50};
    int chip_positions[] = {356,78,32,155,46,131,272,39,299,152,167,61};

    double Tmean_out, Tej_out;

    int num_iterations = 1;  // Número de veces que deseas repetir la llamada a la función

    for (int iteration = 0; iteration < num_iterations; ++iteration) {
        // Llamada a la función fitness
        int result = fitness(save_results, card_file, scale, nchip, t_ext, tmax_chip, t_delta, max_iter, chip_info, chip_positions, &Tmean_out, &Tej_out);

        // Imprimir resultados si es necesario
        printf("Iteración %d:\n", iteration + 1);
        printf("Resultado de la función fitness: %d\n", result);
        printf("Tmean: %1.2f\n", Tmean_out);
        printf("Tej: %1.3f s\n", Tej_out);
        printf("\n");

        // Puedes agregar un pequeño retardo entre las iteraciones si es necesario
        // usleep(1000000);  // Espera de 1 segundo (1,000,000 microsegundos)
    }

    return 0;
}