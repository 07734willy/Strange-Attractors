#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "attractor.h"
#include "render.h"

double xmin, ymin, zmin;
double xmax, ymax, zmax;

void setRangeLimits(double* positions, int length) {
	xmin = xmax = positions[0];
	ymin = ymax = positions[1];
	zmin = zmax = positions[2];

	for (int i = 3; i < 3 * length; i += 3) {
		double x = positions[i + 0];
		double y = positions[i + 1];
		double z = positions[i + 2];

		if (x < xmin)
			xmin = x;
		else if (x > xmax) xmax = x;
		if (y < ymin)
			ymin = y;
		else if (y > ymax)
			ymax = y;
		if (z < zmin)
			zmin = z;
		else if (z > zmax)
			zmax = z;
	}
}

void scalePositions(double *positions, int length, int xres, int yres) {
	for (int i = 0; i < 3 * length; i += 3) {
		positions[i + 0] = (positions[i + 0] - xmin) * (xres-1.0) / (xmax-xmin);
		positions[i + 1] = (positions[i + 1] - ymin) * (yres-1.0) / (ymax-ymin);
		positions[i + 2] = (positions[i + 2] - zmin) * (1.0-ALPHA_MIN) / (zmax-zmin) + ALPHA_MIN;
	}
}

void sumAlpha(double *dest, double *positions, int length, int xres, int yres) {
	for (int i = 3; i < 3 * length; i += 3) {
		int x = (int)positions[i + 0];
		int y = (int)positions[i + 1];
		double z = positions[i + 2];

		int pos = 3 * xres * y + 3 * x;
		double dx = fabs(positions[i + 0] - positions[i - 3]);
		double dy = fabs(positions[i + 1] - positions[i - 2]);
		double dz = fabs(positions[i + 2] - positions[i - 1]);

		dest[pos + 0] += (1-dx/XRES) * ALPHA * z;
		dest[pos + 1] += (1-dy/YRES) * ALPHA * z;
		dest[pos + 2] += (1-dz/(1.0-ALPHA_MIN)) * ALPHA * z;
	}
}

void rgbToBGRA(uint8_t *dest, double *channels) {
	//int count = 0;
	for (int i = 0; i < XRES * YRES; i++) {
		int r = (int)(255 * channels[3 * i + 0]);
		int g = (int)(255 * channels[3 * i + 1]);
		int b = (int)(255 * channels[3 * i + 2]);

		dest[4 * i + 0] = b > 255 ? 255 : b;
		dest[4 * i + 1] = g > 255 ? 255 : g;
		dest[4 * i + 2] = r > 255 ? 255 : r;
		
		//count += b > 0 || g > 0 || r > 0;
	}
	//printf("count: %d\n", count);
}

void positionsToBGRA(uint8_t *dest, double *positions) {

	double *transformed = malloc(3 * NUM_POSITIONS * sizeof(double));
	double *channels = calloc(3 * XRES * YRES, sizeof(double));
	
	// TODO add in logic to transform / rotate
	
	memcpy(transformed, positions, 3 * NUM_POSITIONS * sizeof(double));
	
	//printSlice(transformed, 0, 90, 1);
	setRangeLimits(transformed, NUM_POSITIONS);
	scalePositions(transformed, NUM_POSITIONS, XRES, YRES);

	//printSlice(transformed, 0, 90, 1);
	sumAlpha(channels, transformed, NUM_POSITIONS, XRES, YRES);
	rgbToBGRA(dest, channels);
	
	free(transformed);
	free(channels);
}

int checkPixelDensity(double* positions) {
	setRangeLimits(positions, T_SEARCH);
	scalePositions(positions, T_SEARCH, XRES/DENSITY_SCALE, YRES/DENSITY_SCALE);

	double *channels = calloc(3 * (XRES/DENSITY_SCALE) * (YRES/DENSITY_SCALE), sizeof(double));
	sumAlpha(channels, positions, T_SEARCH, XRES/DENSITY_SCALE, YRES/DENSITY_SCALE);
	int count = 0;

	for (int i = 0; i < (XRES/DENSITY_SCALE) * (YRES/DENSITY_SCALE); i += 3) {
		int r = (int)(255 * channels[3 * i + 0]);
		int g = (int)(255 * channels[3 * i + 1]);
		int b = (int)(255 * channels[3 * i + 2]);

		count += b > 0 || g > 0 || r > 0;
	}

	return count >= (XRES/DENSITY_SCALE) * (YRES/DENSITY_SCALE) * MIN_DENSITY;
}

