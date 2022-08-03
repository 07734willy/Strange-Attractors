import numpy as np 

def render_pixels(int xres, int yres, 
	double[:] xa, double[:] ya, double[:] za, 
	double[:] dxs, double[:] dys, double[:] dzs,
	double xrng, double xmin, double yrng, double ymin, 
	double zrng, double zmin, double mdx, double mdy, 
	double alpha):

	cdef double[:,:,:] render = np.zeros((yres, xres, 3))
	cdef int length = np.size(xa)
	cdef int I
	cdef int J
	cdef double zalpha = 0
	cdef double mdz = zrng

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
		
		render[I, J, 0] += (1-dx/mdx) * alpha * z_alpha
		render[I, J, 1] += (1-dy/mdy) * alpha * z_alpha
		render[I, J, 2] += (1-dz/mdz) * alpha * z_alpha

	return render