#ifndef TRANSFORM_H
#define TRANSFORM_H
#include <stdint.h>

void positionsToBGRA(uint8_t *dest, double *positions);
int checkPixelDensity(double* positions);

#endif
