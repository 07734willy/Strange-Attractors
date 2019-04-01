#ifndef TRANSFORM_H
#define TRANSFORM_H
#include <stdint.h>

#define SQR(X) ((X) * (X))

void positionsToBGRA(uint8_t *dest, double *positions);
int checkPixelDensity(double* positions);
double* positionsToRGB(double* positions);

#endif
