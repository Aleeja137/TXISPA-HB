/* File: diffusion_s.c */ 

#include "defines.h"



/************************************************************************************/
void thermal_update (struct info_param param, float *grid, float *grid_chips)
{
  int i, j, a, b;

  // heat injection at chip positions
  for (i=1; i<NROW-1; i++)
  for (j=1; j<NCOL-1; j++) 
    if (grid_chips[i*NCOL+j] > grid[i*NCOL+j])
      grid[i*NCOL+j] += 0.05 * (grid_chips[i*NCOL+j] - grid[i*NCOL+j]);

  // air cooling at the middle of the card
  a = 0.44*(NCOL-2) + 1;
  b = 0.56*(NCOL-2) + 1;

  for (i=1; i<NROW-1; i++)
  for (j=a; j<b; j++)
      grid[i*NCOL+j] -= 0.01 * (grid[i*NCOL+j] - param.t_ext);
}

/************************************************************************************/
double thermal_diffusion (struct info_param param, float *grid, float *grid_aux)
{
  int    i, j;
  float  T;
  double Tfull = 0.0;

  for (i=1; i<NROW-1; i++)
    for (j=1; j<NCOL-1; j++)
    {
      T = grid[i*NCOL+j] + 
          0.10 * (grid[(i+1)*NCOL+j]   + grid[(i-1)*NCOL+j]   + grid[i*NCOL+(j+1)]     + grid[i*NCOL+(j-1)] + 
                  grid[(i+1)*NCOL+j+1] + grid[(i-1)*NCOL+j+1] + grid[(i+1)*NCOL+(j-1)] + grid[(i-1)*NCOL+(j-1)] 
                  - 8*grid[i*NCOL+j]);

      grid_aux[i*NCOL+j] = T;
      Tfull += T;
    }

    //new values for the grid
    for (i=1; i<NROW-1; i++)
    for (j=1; j<NCOL-1; j++)
      grid[i*NCOL+j] = grid_aux[i*NCOL+j]; 

    return (Tfull);
}

/************************************************************************************/
double calculate_Tmean (struct info_param param, float *grid, float *grid_chips, float *grid_aux)
{
  int    i, j, end, niter;
  float  Tfull;
  double Tmean, Tmean0 = param.t_ext;

  end = 0; niter = 0;

  while (end == 0)
  {
    niter++;
    Tmean = 0.0;

    // heat injection and air cooling 
    thermal_update (param, grid, grid_chips);
 
    // thermal diffusion
    Tfull = thermal_diffusion(param, grid, grid_aux);
    

    // convergence every 10 iterations
    if (niter % 10 == 0)
    {
      Tmean = Tfull / ((NCOL-2)*(NROW-2));
      if ((fabs(Tmean - Tmean0) < param.t_delta) || (niter > param.max_iter))
           end = 1;
      else Tmean0 = Tmean;
    }
  } // end while 
  printf ("Iter (ser): %d\t", niter);
  return (Tmean);
}

