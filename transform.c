#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <float.h>
#include <math.h>
#include "attractor.h"
#include "render.h"

double xmin, ymin, zmin;
double xmax, ymax, zmax;
double dxmax, dymax, dzmax;

void setRangeLimits(double* positions) {
	xmin = xmax = positions[0];
	ymin = ymax = positions[1];
	zmin = zmax = positions[2];
	dxmax = dymax = dzmax = -DBL_MAX;

	for (int i = 3; i < 3 * NUM_POSITIONS; i += 3) {
		double x = positions[i + 0];
		double y = positions[i + 1];
		double z = positions[i + 2];

		if (x < xmin)
			xmin = x;
		else if (x > xmax)
			xmax = x;
		if (y < ymin)
			ymin = y;
		else if (y > ymax)
			ymax = y;
		if (z < zmin)
			zmin = z;
		else if (z > zmax)
			zmax = z;

		double dx = fabs(x - positions[i - 3]);
		double dy = fabs(y - positions[i - 2]);
		double dz = fabs(z - positions[i - 1]);

		if (dx > dxmax)
			dxmax = dx;
		if (dy > dymax)
			dymax = dy;
		if (dz > dzmax)
			dzmax = dz;
	}
}

void scalePositions(double *positions) {
	for (int i = 0; i < 3 * NUM_POSITIONS; i += 3) {
		positions[i + 0] = (positions[i + 0] - xmin) * (XRES-1.0) / (xmax-xmin);
		positions[i + 1] = (positions[i + 1] - ymin) * (YRES-1.0) / (ymax-ymin);
		positions[i + 2] = (positions[i + 2] - zmin) * (1.0-ALPHA_MIN) / (zmax-zmin) + ALPHA_MIN;
	}
}

void sumAlpha(double *dest, double *positions) {
	for (int i = 3; i < 3 * NUM_POSITIONS; i += 3) {
		double x = (int)positions[i + 0];
		double y = (int)positions[i + 1];
		double z = positions[i + 2];

		int pos = 3 * XRES * y + 3 * x;
		double dx = fabs(positions[i + 0] - positions[i - 3]);
		double dy = fabs(positions[i + 1] - positions[i - 2]);
		double dz = fabs(positions[i + 2] - positions[i - 1]);

		dest[pos + 0] += (1-dx/XRES) * ALPHA * z;
		dest[pos + 1] += (1-dy/YRES) * ALPHA * z;
		dest[pos + 2] += (1-dz/dzmax) * ALPHA * z;
	}
}

void rgbToBGRA(uint8_t *dest, double *channels) {
	for (int i = 0; i < XRES * YRES; i++) {
		int r = (int)(255 * channels[3 * i + 0]);
		int g = (int)(255 * channels[3 * i + 1]);
		int b = (int)(255 * channels[3 * i + 2]);

		dest[4 * i + 0] = b > 255 ? 255 : b;
		dest[4 * i + 1] = g > 255 ? 255 : g;
		dest[4 * i + 2] = r > 255 ? 255 : r;
	}
}

void positionsToBGRA(uint8_t *dest, double *positions) {

	double *transformed = malloc(3 * NUM_POSITIONS * sizeof(double));
	double *channels = calloc(3 * XRES * YRES, sizeof(double));
	
	// TODO add in logic to transform / rotate
	
	memcpy(transformed, positions, 3 * NUM_POSITIONS * sizeof(double));
	
	//printSlice(transformed, 0, 90, 1);
	setRangeLimits(transformed);
	scalePositions(transformed);

	//printSlice(transformed, 0, 90, 1);
	sumAlpha(channels, transformed);
	rgbToBGRA(dest, channels);
	
	free(transformed);
	free(channels);
}
