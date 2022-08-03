from __future__ import division
import matplotlib.pyplot as plt 
import numpy as np 
import colorsys
import time

def iterator(x,y,coeff):

	xc = coeff[0:6]
	yc = coeff[6:12]
	
	xy = np.asarray([1,x,y,x*y,x**2,y**2])

	x = (xc * xy).sum()
	y = (yc * xy).sum()

	return x,y

def coeff_to_string(coeff):
	att_string = ''.join([chr(int((c + 7.7)*10)) for c in coeff])
	return att_string

def find_coeffs(low_iters, high_iters, radius, max_attractors = 1):

	att_coeffs = []
	esc_iters = []
	attractors = 0

	while attractors < max_attractors:

		coeff = np.random.randint(-12,13,12)/10
		x,y = 0,0
		
		for t in range(high_iters):

			x,y = iterator(x,y,coeff)
			rr  = x*x + y*y

			if rr > radius*radius:

				if t < low_iters:
					break
				else:
					att_coeffs.append(coeff)
					esc_iters.append(t)
					print 'Saved coefficients'
					print t
					print coeff_to_string(coeff)
					attractors += 1
					break

	return att_coeffs,esc_iters

def render_basins(coeff, xres, yres, xmin, xmax, max_iters, radius):

	start = time.time()

	xrng = xmax - xmin
	yrng = yres/xres * xrng
	ymin = -yrng/2 
	ymax = yrng/2

	print 'Rendering basin'
	print coeff_to_string(coeff)
	print 'Max iterations: %d' % max_iters

	render = np.zeros((yres,xres,3))

	for X in range(xres):
		for Y in range(yres):
			x = xmin + xrng * X/xres
			y = ymin + yrng * Y/yres		

			rr = x*x + y*y
			i = 0

			while rr < radius*radius and i < max_iters:
				x,y = iterator(x,y,coeff)
				rr = x*x + y*y
				i += 1

			render[Y,X,0] = i
			render[Y,X,1] = abs(x)
			render[Y,X,2] = abs(y)

	for i in range(3):
		render[:,:,i] /= render[:,:,i].max()

	fname = coeff_to_string(coeff) + '.png'

	plt.imsave(fname, render, cmap='bone',
		vmin=render.min(), vmax=render.max(), dpi=300)

	end = time.time()
	print '%.2f sec' % (end - start)

xres = 1600
yres = 900

att_coeffs, esc_iters = find_coeffs(
	low_iters = 100, 
	high_iters = 1000,
	radius = 1000,
	max_attractors = 5)

print ''
for coeff,esc_iter in zip(att_coeffs,esc_iters):

	print 'Max number of operations: %d' % (xres*yres*esc_iter)
	
	render_basins(coeff, xres=xres, yres=yres, xmin = -4, xmax = 4, 
		max_iters = 256, radius=100)
	
	print ''



