#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <fenv.h>
#include "attractor.h"
#include "transform.h"
#include "render.h"

void printSlice(double *array, int start, int end, int stride) {
	/* prints a human-readable output of an array, using python-style slicing */
	printf("[");
	if (start < end)
		printf("%f", array[start]);

	for (int i = start + stride; i < end; i += stride)
		printf(", %f", array[i]);

	printf("]\n");
}

long factorial(int num) {
	/* computes the factorial of `num` */
	long prod = 1;
	for (int i = num; i > 0; i--)
		prod *= i;
	return prod;
}

int countCoeff(int num_dimensions, int order) {
	/* returns the number of distinct terms in the multinomial */
	long count = 1;
	for (int i = num_dimensions + order; i > MAX(num_dimensions, order); i--)
		count *= i;
	int res = count / factorial(MIN(num_dimensions, order));
	return res;
}

int coeffsFromSeed(double *dest, char *seed) {
	/* fills an array with the numerical values represented by an alphabetical seed */
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
	/* generates a random set of coefficients */
	for (int i = 0; i < countCoeff(NUM_DIMENSIONS, ORDER) * NUM_DIMENSIONS; i++) {
		dest[i] = (rand() % 25) / 10.0 - 1.2;
	}
	return 1;
}

void printCoeffs(double *coeffs) {
	/* prints the coefficients in alphabetical format */
	printf("Coefficients: ");
	for (int i = 0; i < countCoeff(NUM_DIMENSIONS, ORDER) * NUM_DIMENSIONS; i++) {
		printf("%c", (int)(coeffs[i] * 10 + 12.1) + 'A');
	}
	printf("\n");
}

double recursiveEval(double factor, double *position, int ndim, double **coeffs, int order) {
	/* evaluator that computes the sum of terms for a subset of the original multinomial */
	if (!order)
		return factor * *((*coeffs)++);
	
	double sum = 0;
	for (int i = 0; i < ndim; i++)
		sum += recursiveEval(factor * position[i], position + i, ndim - i, coeffs, order - 1);
	
	return sum;
}

double evaluateNDStep(double *position, double *coeffs) {
	/* serves as a wrapper around `recursiveEval` */
	double *coefficients = coeffs;
	return recursiveEval(1, position, NUM_DIMENSIONS + 1, &coefficients, ORDER);
}

int trajectoryEscapes(double *coeffs, double radius) {
	/* returns whether the trajectory escapes our radius */
	double evenPos[NUM_DIMENSIONS+1] = {0};
	double  oddPos[NUM_DIMENSIONS+1] = {0};
	evenPos[0] = oddPos[0] = 1;
	
	int numCoeff = countCoeff(NUM_DIMENSIONS, ORDER);

	for (int i = 0; i < T_SEARCH - 1; i += 2) {
		for (int j = 0; j < NUM_DIMENSIONS; j++)
			oddPos[j + 1] = evaluateNDStep(evenPos, coeffs + numCoeff * j);

		double dist = 0;
		for (int j = 0; j < NUM_DIMENSIONS; j++) {
			evenPos[j + 1] = evaluateNDStep(oddPos, coeffs + numCoeff * j);
			dist += evenPos[j + 1] * evenPos[j + 1];
		}
		if (dist > radius * radius)
			return 1;
	}
	return 0;
}

int trajectoryIterate(double* dest, double *coeffs, int start, int end) {
	/* evaluates the expressions from [start, end) iterations, returning the points visited */
	double evenPos[NUM_DIMENSIONS+1] = {0};
	double  oddPos[NUM_DIMENSIONS+1] = {0};
	evenPos[0] = oddPos[0] = 1;

	int numCoeff = countCoeff(NUM_DIMENSIONS, ORDER);

	feclearexcept(FE_OVERFLOW);
	for (int i = 0; i < start - 1; i += 2) {
		for (int j = 0; j < NUM_DIMENSIONS; j++)
			oddPos[j + 1] = evaluateNDStep(evenPos, coeffs + numCoeff * j); // TODO fix these hard-coded 20's

		for (int j = 0; j < NUM_DIMENSIONS; j++)
			evenPos[j + 1] = evaluateNDStep(oddPos, coeffs + numCoeff * j);
	}
	
	if (fetestexcept(FE_OVERFLOW)) {
		fprintf(stderr, "Error: Trajectory escaped to infinity\n");
		return 0;
	}

	for (int i = 0; i < NUM_DIMENSIONS * (end - (start & ~1)); i += NUM_DIMENSIONS) {
		for (int j = 0; j < NUM_DIMENSIONS; j++)
			dest[i + j] = evaluateNDStep(evenPos, coeffs + numCoeff * j);
		memcpy(evenPos + 1, dest + i, NUM_DIMENSIONS * sizeof(double));
	}
	return 1;
}

double* generateAttractor(char *seed) {
	/* produces an attractor from the `seed` provided, or generates a random attractor if `seed` is NULL */
	double *coeffs = malloc(countCoeff(NUM_DIMENSIONS, ORDER) * NUM_DIMENSIONS * sizeof(double));
	double *trajectory = malloc(NUM_DIMENSIONS * T_SEARCH * sizeof(double));
	double *positions = malloc(NUM_DIMENSIONS * (T_RENDER - T_IDX) * sizeof(double));

	if (seed != NULL && coeffsFromSeed(coeffs, seed)) {
		trajectoryIterate(positions, coeffs, T_IDX, T_RENDER);
	} else {
		while (1) {
			generateCoeffs(coeffs);
			
			if (trajectoryEscapes(coeffs, RADIUS))
				continue;

			trajectoryIterate(trajectory, coeffs, 0, T_SEARCH);
			if (checkPixelDensity(trajectory) && trajectoryIterate(positions, coeffs, T_IDX, T_RENDER)) {
				printCoeffs(coeffs);
				break;
			}
		}
	}
	
	free(coeffs);
	free(trajectory);

	return positions;
}


