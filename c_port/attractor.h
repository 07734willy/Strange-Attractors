#ifndef ATTRACTOR_H
#define ATTRACTOR_H

#define T_SEARCH 2000
#define T_RENDER ((int)1e7)
#define T_IDX ((int)(T_RENDER/100))

#define RADIUS 10
#define MIN_DENSITY 0.15
#define DENSITY_SCALE 25

#define NUM_POSITIONS (T_RENDER - T_IDX)

double* generateAttractor(char *seed);
void printSlice(double *array, int start, int end, int stride);

#endif
