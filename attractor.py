import time
import matplotlib.pyplot as plt
import numpy as np
import ctypes
import math

@profile
def iterator(x, y, z, coeff, n, terms):
    """ main iteration step function """
 
    # coefficients
    xc = coeff[0: n]
    yc = coeff[n: 2*n]
    zc = coeff[2*n: 3*n]
 
    # polynomial terms
    xyz = terms(x, y, z)
 
    # polynomial evaluation
    x = (xc*xyz).sum()
    y = (yc*xyz).sum()
    z = (zc*xyz).sum()
 
    return x, y, z
 
def quadterms(x, y, z):
    """ quadratic terms """
    return np.asarray(
        [1, x, y, z,
        x*y, x*z, y*z,
        x**2, y**2, z**2]
        )
 
@profile
def cubicterms(x, y, z):
    """ cubic terms """
    return np.asarray(
        [1, x, y, z,
        x*y, x*z, y*z,
        x**2, y**2, z**2,
        x*y*z, x*x*y, x*x*z, y*y*x, y*y*z, z*z*x, z*z*y,
        x*x*x, y*y*y, z*z*z]
        )
 
def coeff_to_string(coeff):
    """convert coefficients to alphabetical values (see Sprott)"""
    att_string = ''.join([chr(int((c + 7.7)*10)) for c in coeff])
    return att_string
 
@profile
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
        print('Invalid value')
        return False
 
    return check_density(render)
   
@profile
def check_density(render, min_fill=1.5):
    """ check if pixel density exceeds threshold """
    filled_pixels = np.count_nonzero(render)
    fill_percentage = 100 * filled_pixels/np.size(render)
   
    if fill_percentage > min_fill:
        print(coeff_to_string(coeff))
        print('Non-zero points: %d (%.2f%%)' % (filled_pixels, fill_percentage))
        print('')
        return True
   
    return False

@profile
def set_aspect(xdata, ydata, width, height, debug=False, margin=1.1):
    """ get boundaries for given aspect ratio w/h """
    xmin, xrng = get_minmax_rng(xdata)
    ymin, yrng = get_minmax_rng(ydata)
 
    if debug:
        print('Data range | X: %.2f | Y: %.2f | Intrinsic aspect ratio: %.2f' % (xrng,yrng,xrng/yrng))
   
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
        print('Rescaled data range | X: %.2f | Y: %.2f | New aspect ratio: %.2f' % (xrng,yrng,xrng/yrng))
 
    return xmin, ymin, xrng, yrng
 
@profile
def get_minmax_rng(data):
    max_val = data.max()
    min_val = data.min()
    data_range = max_val - min_val
 
    return min_val, data_range
 
@profile
def get_index(x, xmin, xrng, xres):
    """ map coordinate to array index """
    return int((x-xmin)/xrng * (xres-1))
 
@profile
def get_dx(xdata):
    dx = abs(xdata - np.roll(xdata, 1))[1:]
    mdx = np.amax(dx)
    return dx, mdx
 
@profile
def zalpha(z, zmin, zrng, a_min=0):
    """ return alpha based on z depth """
    alpha = a_min + (1-a_min)*(z-zmin)/zrng
    return alpha
 
@profile
def save_image(xdata, ydata, zdata, plane, alpha=0.025, xres=3200, yres=1800):
 
    xmin, ymin, xrng, yrng = set_aspect(xdata, ydata, xres, yres, debug=True)
    zmin, zrng = get_minmax_rng(zdata)
    

    dxs, mdx = get_dx(xdata)
    dys, mdy = get_dx(ydata)
    dzs, mdz = get_dx(zdata)
 
    render  = np.zeros((yres, xres, 3))
 
    print('Calculating pixel values')
    try:
        Js = (xdata[1:]-xmin) * (xres-1) / xrng
        Is = (ydata[1:]-ymin) * (yres-1) / yrng

        clip = np.logical_and(Js < xres, Is < yres)
        Js = Js.astype(int)[clip]
        Is = Is.astype(int)[clip]
        
        a_min = 0.25
        Zs = (zdata[1:]-zmin) * (1-a_min) / zrng + a_min

        rx = (1-dxs/mdx)*alpha*Zs[clip]
        ry = (1-dys/mdy)*alpha*Zs[clip]
        rz = (1-dzs/mdz)*alpha*Zs[clip]

        sum_alpha = import_sum_alpha()
        render3 = sum_alpha(yres, xres, Is, Js, rx, ry, rz)

        """
        render2 = np.zeros((yres, xres, 3))
        np.add.at(render2, (Is, Js, [0]*len(rx)), rx)
        np.add.at(render2, (Is, Js, [1]*len(ry)), ry)
        np.add.at(render2, (Is, Js, [2]*len(rz)), rz)

        #print(render2[:2,:2,:2], render3[:2,:2,:2])
        assert(np.allclose(render2, render3))
        """

        if SLOW_MODE:
            for i, (x, y, z, dx, dy, dz) in enumerate(zip(xdata[1:], ydata[1:], zdata[1:], dxs, dys, dzs)):
     
                J = get_index(x, xmin, xrng, xres)
                I = get_index(y, ymin, yrng, yres)
                assert(J == Js[i])
                assert(I == Is[i])

                # pre-z_alpha
                z_alpha = zalpha(z, zmin, zrng, a_min=0.25)
                assert(z_alpha == Zs[i])
                render[I, J, 0] += (1-dx/mdx)*alpha*z_alpha
                render[I, J, 1] += (1-dy/mdy)*alpha*z_alpha
                render[I, J, 2] += (1-dz/mdz)*alpha*z_alpha

            assert(np.allclose(render, render2))
            assert(np.equal(render, render2))

    except ValueError:
        print('Invalid value')
        raise
    
    render = render3
    for k in range(3):
        render[:, :, k][np.where(render[:, :, k] > 1)] = 1
 
    fname = '%s-%dK-%s.png' % (coeff_to_string(coeff), T_RENDER/1000, plane)
    plt.imsave(fname, render, dpi=300)
    end = time.time()
    print('Saved ' + fname)
    print('%.2f sec' % (end-start))


def import_iterator(libpath="./iterator.so"):
    iterator = ctypes.cdll.LoadLibrary(libpath).iterator
    def to_ctype(arr):
        arr_type = ctypes.POINTER(ctypes.c_double * len(arr))
        return arr.astype(np.float64).ctypes.data_as(arr_type)
    
    def wrap_iterator(start, coeff, repeat, radius=0):
        #iterator.restype = np.ctypeslib.ndpointer(dtype=ctypes.c_double, shape=(3*repeat,))
        iterator.restype = ctypes.POINTER(ctypes.c_double * (3 * repeat))

        start = to_ctype(start)
        coeff = to_ctype(coeff)
        out = to_ctype(np.zeros(3 * repeat))

        res = iterator(start, coeff, repeat, ctypes.c_double(radius), out).contents
        return np.array(res).reshape((repeat, 3)).T
    
    return wrap_iterator

def import_sum_alpha(libpath="./iterator.so"):
    sum_alpha = ctypes.cdll.LoadLibrary(libpath).sum_alpha
    def to_double_ctype(arr):
        arr_type = ctypes.POINTER(ctypes.c_double * len(arr))
        return arr.astype(np.float64).ctypes.data_as(arr_type)
    def to_int_ctype(arr):
        arr_type = ctypes.POINTER(ctypes.c_int32 * len(arr))
        return arr.astype(np.int32).ctypes.data_as(arr_type)
    
    def wrap_sum_alpha(yres, xres, Is, Js, rx, ry, rz):
        sum_alpha.restype = ctypes.POINTER(ctypes.c_double * (yres * xres * 3))
        size = len(Is)
        
        out = to_double_ctype(np.zeros(yres * xres * 3))
        Is, Js = to_int_ctype(Is), to_int_ctype(Js)
        rx = to_double_ctype(rx)
        ry = to_double_ctype(ry)
        rz = to_double_ctype(rz)

        res = sum_alpha(yres, xres, size, Is, Js, rx, ry, rz, out).contents
        return np.array(res).reshape((yres, xres, 3))
    
    return wrap_sum_alpha


@profile
def main():
    global coeff, T_RENDER, start, SLOW_MODE

    SLOW_MODE = False

    iterator2 = import_iterator()

    N_ATTRACTORS = 0                # initialize number of attractors
    MAX_ATTRACTORS = 1              # number of attractors to search for
     
    T_SEARCH = 2000                 # number of iterations to perform during search
    T_RENDER = int(10e6)            # number of iterations to perform during render
    T_IDX = int(0.01 * T_RENDER)    # first index after transient
     
    ATT_COEFFS = []                 # list for storing coefficients
    MODE = 'Cubic'
     
    print('Searching for attractors | Mode: %s' % MODE)

    np.random.seed(2)
    while N_ATTRACTORS < MAX_ATTRACTORS:
     
        # pick random coefficients in the range (-1.2,1.2)
        if MODE == 'Cubic':
            coeff = np.random.randint(-12, 13, 60)/10
            n_coeff = 20
            f = cubicterms
        elif MODE == 'Quadratic':
            coeff = np.random.randint(-12, 13, 30)/10
            n_coeff = 10
            f = quadterms
     
        x, y, z = 0, 0, 0
        xl = np.zeros(T_SEARCH)
        yl = np.zeros(T_SEARCH)
        zl = np.zeros(T_SEARCH)
        out_of_bounds = False
     
        xl, yl, zl = iterator2(np.array([x, y, z]), coeff, T_SEARCH, 10)
        out_of_bounds = zl[-1] > 10
        
        if SLOW_MODE:
            for t in range(T_SEARCH):
                x, y, z = iterator(x, y, z, coeff, n_coeff, f)
                r = np.sqrt(x**2+y**2+z**2)
                xl[t] = x
                yl[t] = y
                zl[t] = z
         
                if r > 10 or np.isnan(r): # trajectory escapes outside radius
                    assert(out_of_bounds)
                    out_of_bounds = True
                    break
            else:
                assert(not out_of_bounds)
        
        if not out_of_bounds:
            if pixel_density(xl, yl):
                ATT_COEFFS.append(coeff)
                N_ATTRACTORS += 1
    print('')
     
    for i, coeff in enumerate(ATT_COEFFS):
     
        start = time.time()
        print('\n' + 'Attractor: ' + coeff_to_string(coeff) + ' | %d/%d' % (i+1, MAX_ATTRACTORS))
     
        x, y, z = 0, 0, 0
        xl = np.zeros(T_RENDER)
        yl = np.zeros(T_RENDER)
        zl = np.zeros(T_RENDER)
       
        print('Iterating %d steps' % T_RENDER)
        
        xl2, yl2, zl2 = iterator2(np.array([x, y, z]), coeff, T_IDX)
        print('Completed C-Iteration')
        
        if SLOW_MODE:
            # calculate initial set of points
            for t in range(T_IDX):
                x, y, z = iterator(x, y, z, coeff, n_coeff, f)
                xl[t] = x
                yl[t] = y
                zl[t] = z
                
                print(x, xl2[t], y, yl2[t], z, zl2[t])
                assert(math.isclose(x, xl2[t]))
                assert(math.isclose(y, yl2[t]))
                assert(math.isclose(z, zl2[t]))
        
        check = np.isnan(x+y+z) # check for overflow
     
        if not check:
            if SLOW_MODE:
                for t in range(T_IDX,T_RENDER):
                    x, y, z = iterator(x, y, z, coeff, n_coeff, f)
                    xl[t] = x
                    yl[t] = y
                    zl[t] = z
            
            xl, yl, zl = iterator2(np.array([x, y, z]), coeff, T_RENDER - T_IDX)
            end = time.time()
            print('Finished iteration: %.1f sec | %d iterations per second' % ((end-start), T_RENDER/(end-start)))
     
            start = time.time()
            save_image(xl[T_IDX:], yl[T_IDX:], zl[T_IDX:], plane='xy')
           
            start = time.time()
            save_image(xl[T_IDX:], zl[T_IDX:], yl[T_IDX:], plane='xz')
     
            start = time.time()
            save_image(yl[T_IDX:], zl[T_IDX:], xl[T_IDX:], plane='yz')
     
        else:
            print('Error during calculation')
       
        i += 1


if __name__ == "__main__":
    main()
