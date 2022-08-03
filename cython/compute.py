from iterator_cubic_8d import iteration_cubic_8d
import time
import numpy as np

def compute_attractors(coeffs, render_iterates, render_check_ratio,dimension):

	check_index = int(render_iterates * render_check_ratio)

	itdata = np.asarray(iteration_cubic_8d(check_index,coeffs,dimension))

	if np.isnan(itdata[-1,-1]) or np.isinf(itdata[-1,-1]):
		print('Error during calculation')
		error = True
	else:
		start = time.time()
		itdata = np.asarray(iteration_cubic_8d(render_iterates,coeffs,dimension))
		end = time.time()
		print(f'Iteration complete: {end-start:.2f} seconds')
		error = False

	return itdata, error



