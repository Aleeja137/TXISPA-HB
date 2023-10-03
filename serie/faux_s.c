/* File: faux.c */ 

#include <stdio.h>
#include <values.h>

#include "defines.h"



/************************************************************************************/
void read_data (char *file_name, struct info_param *param, struct info_chips **chips, int ***chip_coord)
{
  int   i, j, h, w;
  float tchip;
  FILE  *fdin;


  fdin = fopen (file_name, "r");
  if (fdin == NULL) {
    printf ("\n\nERROR: input file \n\n");
    exit (-1);
  }

  // simulation parameters
  fscanf (fdin, "%d %d %d %f %f %f %d", &param->scale, &param->nconf, &param->nchip, &param->t_ext, &param->tmax_chip, &param->t_delta, &param->max_iter);
  if (param->scale > 12) {
    printf ("\n\nERROR: maximum scale factor is 12 \n\n");
    exit (-1);
  }

  // chip sizes and temperatures
  *chips = (struct info_chips *) malloc (param->nchip * sizeof(struct info_chips));

  for (i=0; i<param->nchip; i++)
  {
    fscanf (fdin, "%d %d %f", &h, &w, &tchip);
    (*chips)[i].h = h;
    (*chips)[i].w = w;
    (*chips)[i].tchip = tchip;
  }


  // chip positions
  
  *chip_coord = (int **) malloc (param->nconf * sizeof(int*));
  for (i=0; i<param->nconf; i++) (*chip_coord)[i] = (int*) malloc (2 * param->nchip * sizeof(int));

  for (i=0; i<param->nconf; i++)
  for (j=0; j<param->nchip; j++)
    fscanf (fdin, "%d %d", &(*chip_coord)[i][2*j], &(*chip_coord)[i][2*j+1]);

  fclose (fdin);
}



/************************************************************************************/
void results_conf (int conf, double Tmean, struct info_param param, float *grid, float *grid_chips, struct info_results *BT)
{
  int    i, j;
  
  if (BT->Tmean > Tmean) 
  {
    BT->Tmean = Tmean;
    BT->conf = conf;
    for (i=1; i<NROW-1; i++)
    for (j=1; j<NCOL-1; j++) 
    {
      BT->bgrid[i*NCOL+j] = grid[i*NCOL+j];
      BT->cgrid[i*NCOL+j] = grid_chips[i*NCOL+j];
    }
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

  printf ("\n\n >>> BEST CONFIGURATION: %2d\t Tmean: %1.2f\n\n", BT->conf+1, BT->Tmean); 

  sprintf (name, "%s_ser.res", finput);
  fd = fopen (name, "w");
  fprintf (fd, "Tmin_ini %1.1f  Tmax_ini %1.1f  \n", param.t_ext, param.tmax_chip);
  fprintf (fd, "%d\t  %d \n", NCOL-2, NROW-2);

  fprint_grid (fd, BT->bgrid, param);

  fprintf (fd, "\n\n >>> BEST CONFIGURATION: %d\t Tmean: %1.2f\n\n", BT->conf+1, BT->Tmean);
  fclose (fd);

  sprintf (name, "%s_ser.chips", finput);
  fd = fopen (name, "w");
  fprintf (fd, "Tmin_chip %1.1f  Tmax_chip %1.1f  \n", param.t_ext, param.tmax_chip);
  fprintf (fd, "%d\t  %d \n", NCOL-2, NROW-2);

  fprint_grid (fd, BT->cgrid, param);

  fclose (fd);
}

