#cython: boundscheck=False, wraparound=False, nonecheck=False

import numpy as np 

cdef extern from "math.h": 
	double sqrt(double m)

def render_pixels(int xres, int yres, 
	double[:] xa, double[:] ya, double[:] za, 
	double[:] dxs, double[:] dys, double[:] dzs,
	double xrng, double xmin, double yrng, double ymin, 
	double zrng, double zmin, double alpha):

	cdef double[:,:,:] render = np.zeros((yres, xres, 3))
	cdef int length = np.size(xa) # len(xa)
	cdef int I
	cdef int J
	cdef double zalpha = 0
	cdef double mdx = max(dxs)
	cdef double mdy = max(dys)
	cdef double mdz = max(dzs)

	for i in range(length):

		x = xa[i]
		y = ya[i]
		z = za[i]
		dx = dxs[i]
		dy = dys[i]
		dz = dzs[i]

		J = (x-xmin)/xrng * (xres-1)
		I = (y-ymin)/yrng * (yres-1)

		z_alpha = 0.25 + 0.75 * (z-zmin)/zrng

		R = render[I,J,0]
		G = render[I,J,1]
		B = render[I,J,2]

		normRGB = sqrt(R*R + G*G + B*B)

		render[I, J, 0] += ((1-dx/mdx) * alpha * z_alpha) * (1 - normRGB)
		render[I, J, 1] += ((1-dy/mdy) * alpha * z_alpha) * (1 - normRGB)
		render[I, J, 2] += ((1-dz/mdz) * alpha * z_alpha) * (1 - normRGB)

	return render