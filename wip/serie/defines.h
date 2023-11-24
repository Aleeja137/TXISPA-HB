/**********************************************************
 * defines.h 
 * definitions for the thermal simulation of the card
***********************************************************/ 

// minimal card and maximum size
#define RSIZE 200
#define CSIZE 100

#define NROW (RSIZE*param.scale + 2)  // extended row number
#define NCOL (CSIZE*param.scale + 2)  // extended column number


struct info_param {
  int    nconf, nchip, max_iter, scale;  // num. of configurations to test, num. of chips, max. num. iterations, card size scale
  float  t_ext, tmax_chip, t_delta;      // external temp., max. temp. of a chip, temp. incr. for convergence
};

struct info_chips {
  int  	 h, w;    //  size (h, w)
  float  tchip;   // temperature
};


struct info_results {
  double Tmean;		           // mean temp.
  int    conf;                     // conf number
  float  *bgrid;   // final grid
  float  *cgrid;   // initial grid (chips)
};

