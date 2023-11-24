/* File: faux.c */ 

#include <stdio.h>
#include <values.h>
#include <stdlib.h>
#include "defines.h"



/************************************************************************************/
void read_data (int scale, int nchip, float t_ext, float tmax_chip, float t_delta, int max_iter, int * chip_info, int * chip_positions, struct info_param *param, struct info_chips **chips, int ***chip_coord)
{
  int   i, j, h, w;
  float tchip;
  // printf("C debug 1\n");
  // simulation parameters
  param->scale = scale;
  param->nchip = nchip;
  param->t_ext = t_ext;
  param->tmax_chip = tmax_chip;
  param->t_delta = t_delta;
  param->max_iter = max_iter;
  // printf("C debug 2\n");
  
  if (param->scale > 12) {
    printf ("\n\nERROR: maximum scale factor is 12 \n\n");
    exit (-1);
  }
  // printf("C debug 3\n");

  // chip sizes and temperatures
  *chips = (struct info_chips *) malloc (param->nchip * sizeof(struct info_chips));
  // printf("C debug 4\n");

  for (i=0; i<param->nchip; i++)
  {
    // h     = chip_info[i*3];
    // w     = chip_info[i*3+1];
    // tchip = chip_info[i*3+2];

    (*chips)[i].h     = chip_info[i*3];
    (*chips)[i].w     = chip_info[i*3+1];
    (*chips)[i].tchip = chip_info[i*3+2];
  }
  // printf("C debug 5\n");


  // chip positions
  
  *chip_coord = (int **) malloc (sizeof(int*));
  (*chip_coord)[0] = (int*) malloc (2 * param->nchip * sizeof(int));
  // printf("Size of chip_coord: %i\n",2 * param->nchip);
  // printf("C debug 6\n");

  for (j=0; j<param->nchip; j++){
    (*chip_coord)[0][2*j]   = chip_positions[j*2];
    (*chip_coord)[0][2*j+1] = chip_positions[j*2+1];
  }
  // printf("C debug 7\n");
}



/************************************************************************************/
void results_conf (double Tmean, struct info_param param, float *grid, float *grid_chips, struct info_results *BT)
{
  int    i, j;

  BT->Tmean = Tmean;
  for (i=1; i<NROW-1; i++)
  for (j=1; j<NCOL-1; j++) 
  {
    BT->bgrid[i*NCOL+j] = grid[i*NCOL+j];
    BT->cgrid[i*NCOL+j] = grid_chips[i*NCOL+j];
  }

}



/************************************************************************************/
void fprint_grid (FILE *fd, float *grid, struct info_param param)
{
  int i, j;

  // j - i order for better visualitation
  for (j=NCOL-2; j>0; j--)
  {
    for (i=1; i<NROW-1; i++) fprintf (fd, "%1.2f ", grid[i*NCOL+j]);
    fprintf (fd, "\n");
  }
  fprintf (fd, "\n");
}



/************************************************************************************/
void results (struct info_param param, struct info_results *BT, char *finput)
{
  FILE  *fd;
  char  name[100];

  sprintf (name, "%s_ser.res", finput);
  fd = fopen (name, "w");
  fprintf (fd, "Tmin_ini %1.1f  Tmax_ini %1.1f  \n", param.t_ext, param.tmax_chip);
  fprintf (fd, "%d\t  %d \n", NCOL-2, NROW-2);

  fprint_grid (fd, BT->bgrid, param);

  fprintf (fd, "\n\n >>>Tmean: %1.2f\n\n", BT->Tmean);
  fclose (fd);

  sprintf (name, "%s_ser.chips", finput);
  fd = fopen (name, "w");
  fprintf (fd, "Tmin_chip %1.1f  Tmax_chip %1.1f  \n", param.t_ext, param.tmax_chip);
  fprintf (fd, "%d\t  %d \n", NCOL-2, NROW-2);

  fprint_grid (fd, BT->cgrid, param);

  fclose (fd);
}

