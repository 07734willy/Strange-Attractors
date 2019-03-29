import time
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import math

N_ATTRACTORS = 0                # initialize number of attractors
MAX_ATTRACTORS = 1              # number of attractors to search for
 
T_SEARCH = 2000                 # number of iterations to perform during search
T_RENDER = int(10e6)            # number of iterations to perform during render
T_IDX = int(0.01 * T_RENDER)    # first index after transient
 
ATT_COEFFS = []                 # list for storing coefficients
MODE = "Cubic"


""" import external C helper functions """
dll = ctypes.cdll.LoadLibrary("./helper.so")
c_iterator = dll.iterator
c_sum_alpha = dll.sum_alpha

def iterator(x, y, z, coeff, repeat, radius=0):
    """ compute an array of positions visited by recurrence relation """
    c_iterator.restype = ctypes.POINTER(ctypes.c_double * (3 * repeat))

    start = to_double_ctype(np.array([x, y, z]))
    coeff = to_double_ctype(coeff)
    out = to_double_ctype(np.zeros(3 * repeat))

    res = c_iterator(start, coeff, repeat, ctypes.c_double(radius), out).contents
    return np.array(res).reshape((repeat, 3)).T

def sum_alpha(yres, xres, Is, Js, rx, ry, rz):
    """ compute the sum of zalpha values at each pixel """
    c_sum_alpha.restype = ctypes.POINTER(ctypes.c_double * (yres * xres * 3))
    size = len(Is)
    
    out = to_double_ctype(np.zeros(yres * xres * 3))
    Is, Js = to_int_ctype(Is), to_int_ctype(Js)
    rx = to_double_ctype(rx)
    ry = to_double_ctype(ry)
    rz = to_double_ctype(rz)

    res = c_sum_alpha(yres, xres, size, Is, Js, rx, ry, rz, out).contents
    return np.array(res).reshape((yres, xres, 3))

def to_double_ctype(arr):
    """ convert arr to a ctype array of doubles """
    arr_type = ctypes.POINTER(ctypes.c_double * len(arr))
    return arr.astype(np.float64).ctypes.data_as(arr_type)

def to_int_ctype(arr):
    """ convert arr to a ctype array of ints """
    arr_type = ctypes.POINTER(ctypes.c_int32 * len(arr))
    return arr.astype(np.int32).ctypes.data_as(arr_type)

def coeff_to_string(coeff):
    """convert coefficients to alphabetical values (see Sprott)"""
    att_string = "".join([chr(int((c + 7.7)*10)) for c in coeff])
    return att_string
 
def pixel_density(xdata, ydata, xres=320, yres=180):
    """ check for density of points in image """
 
    xmin, ymin, xrng, yrng = set_aspect(xdata, ydata, xres, yres)
    render = np.zeros((yres, xres))
 
    try:
        for x, y in zip(xdata, ydata):
            J = get_index(x, xmin, xrng, xres)
            I = get_index(y, ymin, yrng, yres)
            render[I, J] += 1
    except ValueError:
        print("Invalid value (pixel density)")
        return False
 
    return check_density(render)

def check_density(render, min_fill=1.5):
    """ check if pixel density exceeds threshold """
    filled_pixels = np.count_nonzero(render)
    fill_percentage = 100 * filled_pixels/np.size(render)
   
    if fill_percentage > min_fill:
        print(coeff_to_string(coeff))
        print("Non-zero points: {} ({:.2f}%)".format(filled_pixels, fill_percentage))
        print("")
        return True
   
    return False

def set_aspect(xdata, ydata, width, height, debug=False, margin=1.1):
    """ get boundaries for given aspect ratio w/h """
    xmin, xrng = get_minmax_rng(xdata)
    ymin, yrng = get_minmax_rng(ydata)
 
    if debug:
        print("Data range | X: {:.2f} | Y: {:.2f} | Intrinsic aspect ratio: {:.2f}".format(xrng, yrng, xrng/yrng))
   
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
        print("Rescaled data range | X: {:.2f} | Y: {:.2f} | New aspect ratio: {:.2f}".format(xrng, yrng, xrng/yrng))
 
    return xmin, ymin, xrng, yrng

def get_minmax_rng(data):
    max_val = data.max()
    min_val = data.min()
    data_range = max_val - min_val
 
    return min_val, data_range

def get_index(x, xmin, xrng, xres):
    """ map coordinate to array index """
    return int((x-xmin) * (xres-1) / xrng)
 
def get_dx(xdata):
    dx = abs(xdata - np.roll(xdata, 1))[1:]
    mdx = np.amax(dx)
    return dx, mdx
 
def zalpha(z, zmin, zrng, a_min=0):
    """ return alpha based on z depth """
    alpha = a_min + (1-a_min)*(z-zmin)/zrng
    return alpha

def save_image(xdata, ydata, zdata, plane, alpha=0.025, xres=3200, yres=1800):
 
    xmin, ymin, xrng, yrng = set_aspect(xdata, ydata, xres, yres, debug=True)
    zmin, zrng = get_minmax_rng(zdata)

    dxs, mdx = get_dx(xdata)
    dys, mdy = get_dx(ydata)
    dzs, mdz = get_dx(zdata)
 
    print("Calculating pixel values")
        
    xscaled = (xdata[1:]-xmin) * (xres-1) / xrng
    yscaled = (ydata[1:]-ymin) * (yres-1) / yrng

    clip = np.logical_and(xscaled < xres, yscaled < yres)
    xscaled = xscaled.astype(int)[clip]
    yscaled = yscaled.astype(int)[clip]
    
    a_min = 0.25
    zscaled = (zdata[1:]-zmin) * (1-a_min) / zrng + a_min

    xpix = (1-dxs/mdx)*alpha*zscaled[clip]
    ypix = (1-dys/mdy)*alpha*zscaled[clip]
    zpix = (1-dzs/mdz)*alpha*zscaled[clip]

    render = sum_alpha(yres, xres, yscaled, xscaled, xpix, ypix, zpix)
    render = np.clip(render, None, 1)

    fname = "{}-{}K-{}.png".format(coeff_to_string(coeff), T_RENDER//1000, plane)
    plt.imsave(fname, render, dpi=300)
    end = time.time()
    print("Saved " + fname)
    print("{:.2f} sec".format(end-start))

def main():
    global start, ATT_COEFFS, N_ATTRACTORS, coeff
    print("Searching for attractors | Mode: {}".format(MODE))

    np.random.seed(2)
    while N_ATTRACTORS < MAX_ATTRACTORS:
        # pick random coefficients in the range (-1.2,1.2)
        if MODE == "Cubic":
            coeff = np.random.randint(-12, 13, 60)/10
            n_coeff = 20
        else:
            raise ValueError("Only 'Cubic' mode is currently supported")

        x, y, z = 0, 0, 0
        xl, yl, zl = iterator(x, y, z, coeff, T_SEARCH, 10)
        
        if zl[-1] <= 10:
            if pixel_density(xl, yl):
                ATT_COEFFS.append(coeff)
                N_ATTRACTORS += 1
    print("")
     
    for i, coeff in enumerate(ATT_COEFFS):
     
        start = time.time()
        print("\nAttractor: {} | {}/{}".format(coeff_to_string(coeff), i+1, MAX_ATTRACTORS))
        print("Iterating {} steps".format(T_RENDER))
        
        x, y, z = 0, 0, 0
        xl, yl, zl = iterator(x, y, z, coeff, T_IDX)
        x, y, z = xl[-1], yl[-1], zl[-1]
        
        check = not np.isnan(x+y+z) # check for overflow
     
        if check:
            xl, yl, zl = iterator(x, y, z, coeff, T_RENDER - T_IDX)
            end = time.time()
            print("Finished iteration: {:.1f} sec | {} iterations per second".format((end-start), T_RENDER/(end-start)))
     
            start = time.time()
            save_image(xl[T_IDX:], yl[T_IDX:], zl[T_IDX:], plane="xy")
           
            start = time.time()
            save_image(xl[T_IDX:], zl[T_IDX:], yl[T_IDX:], plane="xz")
     
            start = time.time()
            save_image(yl[T_IDX:], zl[T_IDX:], xl[T_IDX:], plane="yz")
     
        else:
            print("Error during calculation")
       
        i += 1

if __name__ == "__main__":
    main()
