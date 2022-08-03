import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.widgets import Slider

plt.rcParams['axes.facecolor'] = '#000000'

def iterator(x,y,z,coeffs):

	xc = coeffs[0:10]
	yc = coeffs[10:20]
	zc = coeffs[20:30]
	
	xyz = np.asarray([1,x,y,z,x*y,x*z,y*z,x**2,y**2,z**2])

	x = (xc * xyz).sum()
	y = (yc * xyz).sum()
	z = (zc * xyz).sum()

	return x,y,z

def itdata(coeffs,tmax,colorstep,x0,y0,z0):

	xl,yl,zl = [],[],[]
	colors = []

	x = x0; y = y0; z = z0

	for t in range(tmax):
		x,y,z = iterator(x,y,z,coeffs)
		xl.append(x)
		yl.append(y)
		zl.append(z)

		if abs(x) > 100 or abs(y) > 100 or abs(z) > 100:
			break

	dxs = [abs(xl[i+colorstep]-xl[i]) for i in range(len(xl)-colorstep)]
	dys = [abs(yl[i+colorstep]-yl[i]) for i in range(len(yl)-colorstep)]
	dzs = [abs(zl[i+colorstep]-yl[i]) for i in range(len(zl)-colorstep)]

	mdx = max(dxs)
	mdy = max(dys)
	mdz = max(dzs)

	if mdx == 0:
		mdx = 1
	if mdy == 0:
		mdy = 1
	if mdz == 0:
		mdz = 1

	for dx,dy,dz in zip(dxs,dys,dzs):
		cx = 1-dx/mdx
		cy = 1-dy/mdy
		cz = 1-dz/mdz
		cv = (cx,cy,cz)
		colors.append(cv)

	return xl,yl,zl,colors

def sliders_on_changed(val):

	coeffs = [slider.val for slider in coeff_sliders]

	xl, yl, zl, colors = itdata(coeffs,
		int(tmax_slider.val),int(cstep_slider.val),
		x0_slider.val,y0_slider.val,z0_slider.val)

	xy = np.vstack((xl,yl)).T
	pxy.set_offsets(xy)
	pxy.set_facecolor(colors)
	pxy.set_alpha(alpha_slider.val)
	ax.set_aspect('equal')
	ax.set_xlim(-xlim_slider.val+xc_slider.val,
		xlim_slider.val+xc_slider.val)
	ax.set_ylim(-ylim_slider.val+yc_slider.val,
		ylim_slider.val+yc_slider.val)

	fig.canvas.draw_idle()


colorstep = 1
xl,yl,zl = [],[],[]

fig = plt.figure(1)
ax = plt.subplot2grid((2,3),(0,0),colspan=2,rowspan=2)
pxy = ax.scatter(xl,yl,marker='.',s=6,
			facecolor='w',edgecolor='None',alpha=0.7)
pos = ax.get_position()

coeff_sliders_ax = []
coeff_sliders = []
for i in range(30):
	coeff_sliders_ax.append(fig.add_axes([1.1*pos.x1, pos.y1 - (0.02*i), pos.width/3., 0.01], axisbg='w'))
	if i < 10:
		coeff_sliders.append(Slider(coeff_sliders_ax[i],'a%d' % i,-1,1,valinit=0))
	elif i >= 10 and i < 20:
		coeff_sliders.append(Slider(coeff_sliders_ax[i],'b%d' % (i-10),-1,1,valinit=0))
	else: 
		coeff_sliders.append(Slider(coeff_sliders_ax[i],'c%d' % (i-20),-1,1,valinit=0))
	coeff_sliders[i].on_changed(sliders_on_changed)

xlim_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.63, pos.width/3., 0.01], axisbg='w')
xlim_slider = Slider(xlim_slider_ax,'xlim',0.1,2,valinit=1)
xlim_slider.on_changed(sliders_on_changed)

ylim_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.65, pos.width/3., 0.01], axisbg='w')
ylim_slider = Slider(ylim_slider_ax,'ylim',0.1,2,valinit=1)
ylim_slider.on_changed(sliders_on_changed)

tmax_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.67, pos.width/3., 0.01], axisbg='w')
tmax_slider = Slider(tmax_slider_ax,'tmax',1000,100000,valinit=5000,valfmt='%d')
tmax_slider.on_changed(sliders_on_changed)

alpha_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.69, pos.width/3., 0.01], axisbg='w')
alpha_slider = Slider(alpha_slider_ax,'alpha',0,1,valinit=0.7)
alpha_slider.on_changed(sliders_on_changed)

cstep_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.71, pos.width/3., 0.01], axisbg='w')
cstep_slider = Slider(cstep_slider_ax,'colorstep',1,10,valinit=1)
cstep_slider.on_changed(sliders_on_changed)

x0_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.73, pos.width/3., 0.01], axisbg='w')
x0_slider = Slider(x0_slider_ax,'x0',-1,1,valinit=0.1)
x0_slider.on_changed(sliders_on_changed)

y0_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.75, pos.width/3., 0.01], axisbg='w')
y0_slider = Slider(y0_slider_ax,'y0',-1,1,valinit=0.1)
y0_slider.on_changed(sliders_on_changed)

z0_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.77, pos.width/3., 0.01], axisbg='w')
z0_slider = Slider(z0_slider_ax,'z0',-1,1,valinit=0.1)
z0_slider.on_changed(sliders_on_changed)

xc_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.79, pos.width/3., 0.01], axisbg='w')
xc_slider = Slider(xc_slider_ax,'x center',-1,1,valinit=0.0)
xc_slider.on_changed(sliders_on_changed)

yc_slider_ax = fig.add_axes([1.1*pos.x1, pos.y1 - 0.81, pos.width/3., 0.01], axisbg='w')
yc_slider = Slider(yc_slider_ax,'y center',-1,1,valinit=0.0)
yc_slider.on_changed(sliders_on_changed)

plt.show()