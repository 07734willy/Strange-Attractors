import numpy as np 
import matplotlib.pyplot as plt
from functions import *
from renderer_v1 import render_pixels
import time 

def render_attractors(xl, yl, zl, coeff, dimension, seed, tag, alpha = 0.0075, xres = 3200, yres = 1800):

	xa = np.asarray(xl)
	ya = np.asarray(yl)
	za = np.asarray(zl)

	xmin, ymin, xrng, yrng, xdr, ydr = set_aspect(xa, ya, 
		xres, yres, debug=True)
	zmin, zrng = get_minmax_rng(za)

	if not np.isnan(xrng):

		print('Calculating pixel values')
		start = time.time()

		dxs = get_dx(xl)
		dys = get_dx(yl)
		dzs = get_dx(zl)

		print(f'Calculated difference arrays {time.time()-start:.1f} seconds')
		render = np.asarray(render_pixels(xres, yres, 
			xa[1:], ya[1:], za[1:],
			dxs, dys, dzs, 
			xrng, xmin, yrng, ymin, zrng, zmin,
			xdr, ydr, alpha))

		print(f'Calculated pixel values {time.time()-start:.1f} seconds')

		for k in range(3):
			render[:, :, k][np.where(render[:, :, k] > 1)] = 1

		print(f'Truncated oversaturated pixels {time.time()-start:.1f} seconds')

		fname = f'render/D{dimension}-{seed}-{tag}.png'
		plt.imsave(fname, render, dpi=300)
		print('Saved ' + fname)
		print(f'{time.time()-start:.1f} seconds')
