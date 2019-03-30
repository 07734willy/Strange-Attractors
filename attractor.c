#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fenv.h>
#include "attractor.h"
#include "render.h"

void printSlice(double *array, int start, int end, int stride) {
	printf("[");
	if (start < end)
		printf("%f", array[start]);

	for (int i = start + stride; i < end; i += stride)
		printf(", %f", array[i]);

	printf("]\n");
}

int coeffsFromSeed(double *dest, char *seed) {
	if (strlen(seed) != 60) {
		fprintf(stderr, "Error: Seeds must be exactly 60 characters in length");
		return 0;
	}

	for (int i = 0; i < 60; i++) {
		if ('A' > seed[i] || seed[i] > 'Y') {
			fprintf(stderr, "Error: Seeds must contain only the characters A-Y");
			return 0;
		}
		dest[i] = ((seed[i] - 'A') % 25) / 10.0 - 1.2;
	} 
	return 1;
}


int generateCoeffs(double *dest) {
	for (int i = 0; i < 60; i++) {
		dest[i] = (rand() % 25) / 10.0 - 1.2;
	}
	return 1;
}

double evaluateStep(double x, double y, double z, double *coeffs) {
	double sum;
	sum =  coeffs[0];
	sum += coeffs[1] * x;
	sum += coeffs[2] * y;
	sum += coeffs[3] * z;
	sum += coeffs[4] * x * y;
	sum += coeffs[5] * x * z;
	sum += coeffs[6] * y * z;
	sum += coeffs[7] * x * x;
	sum += coeffs[8] * y * y;
	sum += coeffs[9] * z * z;

	sum += coeffs[10] * x * y * z;
	sum += coeffs[11] * x * x * y;
	sum += coeffs[12] * x * x * z;
	sum += coeffs[13] * y * y * x;
	sum += coeffs[14] * y * y * z;
	sum += coeffs[15] * z * z * x;
	sum += coeffs[16] * z * z * y;

	sum += coeffs[17] * x * x * x;
	sum += coeffs[18] * y * y * y;
	sum += coeffs[19] * z * z * z;
	return sum;
}

int validTrajectory(double *coeffs, double radius) {
	double x = 0, y = 0, z = 0;

	for (int i = 0; i < T_SEARCH; i++) {
		double xnew = evaluateStep(x, y, z, coeffs);
		double ynew = evaluateStep(x, y, z, coeffs + 20);
		double znew = evaluateStep(x, y, z, coeffs + 40);
		x = xnew, y = ynew, z = znew;
		if (x*x + y*y + z*z > radius*radius)
			return 0;
	}
	return 1;
}

int trajectoryIterate(double* dest, double *coeffs) {
	double x = 0, y = 0, z = 0;

	feclearexcept(FE_OVERFLOW);
	for (int i = 0; i < T_IDX; i++) {
		double xnew = evaluateStep(x, y, z, coeffs);
		double ynew = evaluateStep(x, y, z, coeffs + 20);
		double znew = evaluateStep(x, y, z, coeffs + 40);
		x = xnew, y = ynew, z = znew;
	}
	
	if (fetestexcept(FE_OVERFLOW)) {
		fprintf(stderr, "Error: Trajectory escaped to infinity\n");
		return 0;
	}

	for (int i = 0; i < 3 * (T_RENDER - T_IDX); i += 3) {
		dest[i + 0] = evaluateStep(x, y, z, coeffs);
		dest[i + 1] = evaluateStep(x, y, z, coeffs + 20);
		dest[i + 2] = evaluateStep(x, y, z, coeffs + 40);
		x = dest[i], y = dest[i+1], z = dest[i+2];
	}

	return 1;
}

double* generateAttractor(char *seed) {
	double *coeffs = malloc(60 * sizeof(double));

	if (seed == NULL || !coeffsFromSeed(coeffs, seed)) {
		do {
			generateCoeffs(coeffs);
		} while (!validTrajectory(coeffs, RADIUS));
	}

	double *positions = malloc(3 * (T_RENDER - T_IDX) * sizeof(double));
	trajectoryIterate(positions, coeffs);

	printSlice(positions, 0, 60, 1);

	return positions;
}


