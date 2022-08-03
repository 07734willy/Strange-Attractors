import numpy as np 
import time 

from search import search_attractors
from compute import compute_attractors

# these should be compiled first (see setup files)
from render_v1 import render_attractors as render1
from render_v2 import render_attractors as render2


# iterations used in search 
search_iterates = 2000    

# iterations used for rendering (more is better)
render_iterates = 500000

# check after fraction of iterations
# to make sure there is no accidental overflow
render_check_ratio = 0.01

# number of attractors to find and render
n_attractors = 2

# alpha value of the pixels (adjust to render_iterates)
# too low may result in overly dark images
# too high may result in over-saturated images
# it is useful to render 1 or 2 attractors and adjust based on results
# can also set manually in render functions below
alpha = 0.01 * 50000000/render_iterates

for i in range(n_attractors):

	start = time.time()

	# dimension of attractor (takes very long to find anything if > 10)
	dimension = 3

	coeffs, seed = search_attractors(search_iterates, dimension)
	itdata, error = compute_attractors(coeffs, render_iterates, render_check_ratio, dimension)

	# optional save of iteration data (for later processing)
	# np.save(f'd_{dimension}_{seed}_arr', itdata)

	if not error:

		render1(
			itdata[10000:, dimension - 3], 
			itdata[10000:, dimension - 2], 
			itdata[10000:, dimension - 1], 
			coeffs, dimension, seed, 'xyz-v1', alpha = 0.0065)
		
		render2(
			itdata[10000:, dimension - 3], 
			itdata[10000:, dimension - 2], 
			itdata[10000:, dimension - 1], 
			coeffs, dimension, seed, 'xyz-v2', alpha = alpha)

	print(f'Total time: {time.time()-start:.2f} seconds')


# add main function here -- 