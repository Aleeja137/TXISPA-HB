/* File: faux.h */ 

extern void read_data(int scale, int nchip, float t_ext, float tmax_chip, float t_delta, int max_iter, int * chip_info, int * chip_positions, struct info_param *param, struct info_chips **chips, int ***chip_coord);
// extern void read_data (char *, struct info_param *, struct info_chips **, int ***);
extern void results_conf (double, struct info_param, float *, float *, struct info_results *);
extern void results (struct info_param, struct info_results *, char *);

