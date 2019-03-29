#include <stdlib.h>
#include <stdio.h>

double* iterator(double* start, double* coeffs, int repeat, double radius, double* out) {
	double x = start[0], y = start[1], z = start[2];

	for (int run = 0; run < repeat; run++) {
		for (int i = 0; i < 3; i++) {
			out[3 * run + i] =  coeffs[20 * i + 0];
			out[3 * run + i] += coeffs[20 * i + 1] * x;
			out[3 * run + i] += coeffs[20 * i + 2] * y;
			out[3 * run + i] += coeffs[20 * i + 3] * z;
			out[3 * run + i] += coeffs[20 * i + 4] * x * y;
			out[3 * run + i] += coeffs[20 * i + 5] * x * z;
			out[3 * run + i] += coeffs[20 * i + 6] * y * z;
			out[3 * run + i] += coeffs[20 * i + 7] * x * x;
			out[3 * run + i] += coeffs[20 * i + 8] * y * y;
			out[3 * run + i] += coeffs[20 * i + 9] * z * z;
			
			out[3 * run + i] += coeffs[20 * i + 10] * x * y * z;
			out[3 * run + i] += coeffs[20 * i + 11] * x * x * y;
			out[3 * run + i] += coeffs[20 * i + 12] * x * x * z;
			out[3 * run + i] += coeffs[20 * i + 13] * y * y * x;
			out[3 * run + i] += coeffs[20 * i + 14] * y * y * z;
			out[3 * run + i] += coeffs[20 * i + 15] * z * z * x;
			out[3 * run + i] += coeffs[20 * i + 16] * z * z * y;

			out[3 * run + i] += coeffs[20 * i + 17] * x * x * x;
			out[3 * run + i] += coeffs[20 * i + 18] * y * y * y;
			out[3 * run + i] += coeffs[20 * i + 19] * z * z * z;
		}
		x = out[3 * run];
		y = out[3 * run + 1];
		z = out[3 * run + 2];

		if (radius && radius * radius < x*x + y*y + z*z) {
			//printf("Failed\n");
			out[3 * repeat - 1] = radius + 1; // hack to quickfail last vector check
			return out;
		}
	}
	return out;
}

double* sum_alpha(int yres, int xres, int len, int* Is, int* Js, double* rx, double* ry, double* rz, double* out) {
	for (int i = 0; i < len; i++) {
		int pos = xres * 3 * Is[i] + 3 * Js[i];
		out[pos + 0] += rx[i];
		out[pos + 1] += ry[i];
		out[pos + 2] += rz[i];
	}
	return out;
}
