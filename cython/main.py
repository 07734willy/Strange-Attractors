from search import search_attractors
from compute import compute_attractors
from render_v1 import render_attractors as render1
from render_v2 import render_attractors as render2
import numpy as np 
import time 

search_iterates = 2000
render_iterates = 500000
render_check_ratio = 0.01
n_attractors = 2

alpha = 0.01 * 50000000/render_iterates

for i in range(n_attractors):

	start = time.time()

	dimension = 9

	coeffs, seed = search_attractors(search_iterates, dimension)
	itdata, error = compute_attractors(coeffs, render_iterates, render_check_ratio, dimension)

	np.save(f'd_{dimension}_{seed}_arr', itdata)

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


