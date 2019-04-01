from __future__ import division
import time
import matplotlib.pyplot as plt
import numpy as np
from numpy import tensordot as tdot

"""
code for finding and saving images of strange attractors in n
dimensions. currently using cubic order for the equations
"""

def N_iterator(coordinates,coefficients,d):
	""" single iteration """

	coordinates = reshape_coordinates(coordinates)

	f = np.zeros(d+1)
	for X in range(d):
		f[X+1] = (coordinates*coefficients[X, :, :, :]).sum()
	f[0] = 1

	return f

def pixel_density(iterates, xres=320, yres=180):
	""" check for density of points in image """

	xmin, ymin, xrng, yrng = set_aspect(iterates[:,0], iterates[:,1], xres, yres)
	render = np.zeros((yres, xres))

	try:
		for x, y in zip(iterates[:,0], iterates[:,1]):
			J = get_index(x, xmin, xrng, xres)
			I = get_index(y, ymin, yrng, yres)
			render[I, J] += 1
	except ValueError:
		print 'Invalid value'
		return False

	return check_density(render)
	
def check_density(render, min_fill=2.0):
	""" check if pixel density exceeds threshold """
	filled_pixels = np.count_nonzero(render)
	fill_percentage = 100 * filled_pixels/np.size(render)
	if fill_percentage > min_fill:
		print seed
		print 'Non-zero points: %d (%.2f%%)' % (filled_pixels, fill_percentage)
		print ''
		return True
	
	return False

def set_aspect(xdata, ydata, width, height, debug=False, margin=1.1):
	""" get boundaries for given aspect ratio w/h """
	xmin, xrng = get_minmax_rng(xdata) 
	ymin, yrng = get_minmax_rng(ydata)

	if debug:
		print 'Data range | X: %.2f | Y: %.2f | Intrinsic aspect ratio: %.2f' % (
			xrng, yrng, xrng/yrng)
	
	xmid = xmin + xrng/2
	ymid = ymin + yrng/2

	if xrng/yrng < width/height:
		xrng = width/height * yrng
	else:
		yrng = height/width * xrng

	xrng *= margin
	yrng *= margin

	xmin = xmid - xrng/2.
	ymin = ymid - yrng/2
	if debug:
		print 'Rescaled data range | X: %.2f | Y: %.2f | New aspect ratio: %.2f' % (
			xrng, yrng, xrng/yrng)

	return xmin, ymin, xrng, yrng

def get_minmax_rng(data):
	max_val = data.max()
	min_val = data.min()
	data_range = max_val - min_val

	return min_val, data_range

def get_index(x, xmin, xrng, xres):
	""" map coordinate to array index """
	return int((x-xmin)/xrng * (xres-1))

def get_dx(xdata):
	""" distance between iterates for color mapping """
	dx = abs(xdata - np.roll(xdata, 1))[1:]
	mdx = max(dx)
	return dx, mdx

def zalpha(z, zmin, zrng, a_min=0):
	""" return alpha based on z depth """
	alpha = a_min + (1-a_min)*(z-zmin)/zrng
	return alpha

def reshape_coordinates(coordinates):
	""" reshape coordinates to align with coefficient array """
	return tdot(coordinates, tdot(coordinates, coordinates, axes=0), axes=0)

def make_coefficients(d):
	""" generate array of cubic coefficients """

	coefficients = np.zeros((d,d+1,d+1,d+1))

	for X in range(d):
		for i in range(d + 1):
			for j in range(d + 1):
				for k in range(d + 1):
					if i == j and i == k:
						coefficients[X, i, j, k] = np.random.uniform(-10, 11)/(10+2*d)
					elif i != j and j != k and k != i:
						a = np.random.randint(-10, 11)/(10+2*d)
						coefficients[X, i, j, k] = a/6
						coefficients[X, i, k, j] = a/6
						coefficients[X, j, i, k] = a/6
						coefficients[X, j, k, i] = a/6
						coefficients[X, k, i, j] = a/6
						coefficients[X, k, j, i] = a/6
					else:
						b = np.random.randint(-10, 11)/(10+2*d)
						coefficients[X, i, j, k] = b/3
						coefficients[X, j, k, i] = b/3
						coefficients[X, k, i, j] = b/3

	return coefficients

def save_image(iterates, alpha=0.035, xres=3200, yres=1800):

	dims = ['x','y','z','u','v','w','q','r','s','t']

	for i in range(DIMENSION):

		x_idx = i % DIMENSION
		y_idx = (i + 1) % DIMENSION
		z_idx = (i + 2) % DIMENSION

		start = time.time()
		xmin, ymin, xrng, yrng = set_aspect(
			iterates[:, x_idx], 
			iterates[:, y_idx], 
			xres, yres, debug=True)
		zmin, zrng = get_minmax_rng(iterates[:, z_idx])

		dxs, mdx = get_dx(iterates[:, x_idx])
		dys, mdy = get_dx(iterates[:, y_idx])
		dzs, mdz = get_dx(iterates[:, z_idx])

		render  = np.zeros((yres, xres, 3))

		print 'Calculating pixel values'
		try:
			for x, y, z, dx, dy, dz in zip(
				iterates[1:, x_idx], 
				iterates[1:, y_idx], 
				iterates[1:, z_idx], 
				dxs, dys, dzs):

				J = get_index(x, xmin, xrng, xres)
				I = get_index(y, ymin, yrng, yres)

				z_alpha = zalpha(z, zmin, zrng, a_min=0.25)
				render[I, J, 0] += (1-dx/mdx)*alpha*z_alpha
				render[I, J, 1] += (1-dy/mdy)*alpha*z_alpha
				render[I, J, 2] += (1-dz/mdz)*alpha*z_alpha

		except ValueError:
			print 'Invalid value'

		# set pixel that exceed max RGB to 1
		for k in range(3):
			render[:, :, k][np.where(render[:, :, k] > 1)] = 1

		fname = 'D%d-%s-%dK-%s%s.png' % (
			DIMENSION, 
			seed, 
			T_RENDER/1000, 
			dims[x_idx], 
			dims[y_idx])
		plt.imsave(fname, render, dpi=300)
		end = time.time()
		print 'Saved ' + fname
		print '%.2f sec' % (end-start)

N_ATTRACTORS = 0 				# initialize number of attractors
MAX_ATTRACTORS = 20	 			# number of attractors to search for
DIMENSION = 8				    # max = 10
T_SEARCH = 2000 				# number of iterations to perform during search
T_RENDER = int(5e6) 			# number of iterations to perform during render
T_IDX = int(0.01 * T_RENDER) 	# first index after transient

ATT_COEFFS = [] # list for storing coefficients           
ATT_SEED   = [] # list for storing seeds

print 'Searching for attractors | Dimension: %d' % DIMENSION
while N_ATTRACTORS < MAX_ATTRACTORS:

	d = DIMENSION
	seed = np.random.randint(0,1e9)
	np.random.seed(seed)

	coefficients = make_coefficients(d)
	coordinates = np.zeros(d + 1)
	coordinates[0] = 1

	iterates = np.zeros((T_SEARCH,d))
	out_of_bounds = False

	for t in range(T_SEARCH):
		coordinates = N_iterator(coordinates, coefficients, d)
		iterates[t, :] = coordinates[1:]
		r = (coordinates[1:]*coordinates[1:]).sum()

		if r > 100 or np.isnan(r): # trajectory escapes outside radius
			out_of_bounds = True
			break

	if not out_of_bounds:
		if pixel_density(iterates):
			ATT_COEFFS.append(coefficients)
			ATT_SEED.append(seed)
			N_ATTRACTORS += 1
print ''

for i, (coefficients, seed) in enumerate(zip(ATT_COEFFS,ATT_SEED)):

	start = time.time()
	print '\n' + 'Attractor: ' + str(seed) + ' | %d/%d' % (
		i+1, MAX_ATTRACTORS)

	coordinates = np.zeros(d+1)
	coordinates[0] = 1
	iterates = np.zeros((T_RENDER,d))
	
	print 'Iterating %d steps' % T_RENDER
	# calculate initial set of points
	for t in range(T_IDX):
		coordinates = N_iterator(coordinates,coefficients,d)
		iterates[t,:] = coordinates[1:]
	check = np.isnan(iterates[t,:].sum()) # check for overflow

	if not check:
		for t in range(T_IDX,T_RENDER):
			coordinates = N_iterator(coordinates,coefficients,d)
			iterates[t,:] = coordinates[1:]
	
		end = time.time()
		its_per_sec = T_RENDER/(end-start)
		print 'Finished iteration: %.1f sec | %d iterations per second' % (
			(end-start), its_per_sec)

		save_image(iterates)

	else:
		print 'Error during calculation'
	
	i += 1
