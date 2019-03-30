#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fenv.h>
#include "attractor.h"
#include "transform.h"

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

void printCoeffs(double *coeffs) {
	printf("Coefficients: ");
	for (int i = 0; i < 60; i++) {
		printf("%c", (int)(coeffs[i] * 10 + 12.1) + 'A');
	}
	printf("\n");
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

int trajectoryEscapes(double *coeffs, double radius) {
	double x = 0, y = 0, z = 0;

	for (int i = 0; i < T_SEARCH; i++) {
		double xnew = evaluateStep(x, y, z, coeffs);
		double ynew = evaluateStep(x, y, z, coeffs + 20);
		double znew = evaluateStep(x, y, z, coeffs + 40);
		x = xnew, y = ynew, z = znew;
		if (xnew*xnew + ynew*ynew + znew*znew > radius*radius)
			return 1;
	}
	return 0;
}

int trajectoryIterate(double* dest, double *coeffs, int start, int end) {
	double x = 0, y = 0, z = 0;

	feclearexcept(FE_OVERFLOW);
	for (int i = 0; i < start; i++) {
		double xnew = evaluateStep(x, y, z, coeffs);
		double ynew = evaluateStep(x, y, z, coeffs + 20);
		double znew = evaluateStep(x, y, z, coeffs + 40);
		x = xnew, y = ynew, z = znew;
	}
	
	if (fetestexcept(FE_OVERFLOW)) {
		fprintf(stderr, "Error: Trajectory escaped to infinity\n");
		return 0;
	}

	for (int i = 0; i < 3 * (end - start); i += 3) {
		dest[i + 0] = evaluateStep(x, y, z, coeffs);
		dest[i + 1] = evaluateStep(x, y, z, coeffs + 20);
		dest[i + 2] = evaluateStep(x, y, z, coeffs + 40);
		x = dest[i], y = dest[i+1], z = dest[i+2];
	}

	return 1;
}

double* generateAttractor(char *seed) {
	double *coeffs = malloc(60 * sizeof(double));
	double *trajectory = malloc(3 * T_SEARCH * sizeof(double));
	double *positions = malloc(3 * (T_RENDER - T_IDX) * sizeof(double));

	if (seed == NULL || !coeffsFromSeed(coeffs, seed)) {
		while (1) {
			generateCoeffs(coeffs);
			//coeffsFromSeed(coeffs, seed);
			if (trajectoryEscapes(coeffs, RADIUS)) {
				continue;
			}
			trajectoryIterate(trajectory, coeffs, 0, T_SEARCH);
			if (checkPixelDensity(trajectory) && trajectoryIterate(positions, coeffs, T_IDX, T_RENDER)) {
				printCoeffs(coeffs);
				printSlice(positions, 0, 60, 1);

				return positions;
			}
		}
	}

}


