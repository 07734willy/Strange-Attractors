import numpy as np 

def get_minmax_rng(data):
	max_val = data.max()
	min_val = data.min()
	data_range = max_val - min_val

	return min_val, data_range

def get_dx(xdata):
	print('Calculating differences')
	dx = abs(xdata - np.roll(xdata, 1))[1:]
	return dx

def zalpha(z, zmin, zrng, a_min=0):
	""" return alpha based on z depth """
	alpha = a_min + (1-a_min)*(z-zmin)/zrng
	return alpha

def get_index(x, xmin, xrng, xres):
	""" map coordinate to array index """
	return int((x-xmin)/xrng * (xres-1))

def set_aspect(xdata, ydata, width, height, debug=False, margin=1.1):
	""" get boundaries for given aspect ratio w/h """
	xmin, xrng = get_minmax_rng(xdata) 
	ymin, yrng = get_minmax_rng(ydata)

	xdata_rng = xrng 
	ydata_rng = yrng 

	if debug:
		print('Data range | X: {:.2f} | Y: {:.2f} | Intrinsic aspect ratio: {:.2f}'.format(xrng, yrng, xrng/yrng))
	
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
		print('Rescaled data range | X: {:.2f} | Y: {:.2f} | New aspect ratio: {:.2f}'.format(xrng, yrng, xrng/yrng))

	return xmin, ymin, xrng, yrng, xdata_rng, ydata_rng

def pixel_density(xl, yl, xres=320, yres=180):
	""" check for density of points in image """

	xmin, ymin, xrng, yrng, xdr, ydr = set_aspect(xl, yl, xres, yres)
	render = np.zeros((yres, xres))

	try:
		for x, y in zip(xl, yl):
			J = get_index(x, xmin, xrng, xres)
			I = get_index(y, ymin, yrng, yres)
			render[I, J] += 1
	except ValueError:
		print('Invalid value')
		return False

	return check_density(render)
	
def check_density(render, min_fill=2.0):
	""" check if pixel density exceeds threshold """
	filled_pixels = np.count_nonzero(render)
	fill_percentage = 100 * filled_pixels/np.size(render)
	if fill_percentage > min_fill:
		return True
	
	return False