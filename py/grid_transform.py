from __future__ import print_function
import matplotlib.pyplot as plt 
import numpy as np 

lims       = 0.5
divs       = 20
boxwidth   = 2*lims/divs
detail     = 1000
coeff      = np.random.randint(-100,100,12)/100.
lt = '.'

hlines_main = []
vlines_main = []
hlines_sub  = []
vlines_sub  = []

class LineObject(object):
	def __init__(self,xs,ys):
		self.xs = xs
		self.ys = ys

def iterator(x,y,coeff):
	a = coeff[0:6]
	b = coeff[6:12]

	fx = a[0] + a[1] * x + a[2] * y + a[3] * x * y + a[4] * x**2 + a[5] * y**2
	fy = b[0] + b[1] * x + b[2] * y + b[3] * x * y + b[4] * x**2 + b[5] * y**2

	return fx,fy

def drawframe():

	plt.cla()
	coeffstr   = ['%.2f' % c for c in coeff]
	plt.title(' '.join(coeffstr))

	for j, (vline, hline) in enumerate(zip(vlines_main,hlines_main)):
		if j == divs/2:
			ax.plot(vline.xs,vline.ys,lt,ms=1,c='k',alpha=1.0,lw=1.5,zorder=3)
			ax.plot(hline.xs,hline.ys,lt,ms=1,c='k',alpha=1.0,lw=1.5,zorder=3)
		else:
			ax.plot(vline.xs,vline.ys,lt,ms=1,c='k',alpha=0.5,lw=1,zorder=2)
			ax.plot(hline.xs,hline.ys,lt,ms=1,c='k',alpha=0.5,lw=1,zorder=2)

	for j, (vline, hline) in enumerate(zip(vlines_sub,hlines_sub)):
		ax.plot(vline.xs,vline.ys,lt,ms=1,c='r',alpha=0.5,zorder=1)
		ax.plot(hline.xs,hline.ys,lt,ms=1,c='r',alpha=0.5,zorder=1)
	fig.canvas.draw()

def press(event):

	global coeff, hlines_main,hlines_sub,vlines_main,vlines_sub,lt
	# print('press', event.key)

	if event.key not in ('l','r'):
		
		for vline,hline in zip(vlines_main,hlines_main):
			hline.xs,hline.ys = iterator(hline.xs,hline.ys,coeff)
			vline.xs,vline.ys = iterator(vline.xs,vline.ys,coeff)

		for vline,hline in zip(vlines_sub,hlines_sub):
			hline.xs,hline.ys = iterator(hline.xs,hline.ys,coeff)
			vline.xs,vline.ys = iterator(vline.xs,vline.ys,coeff)

		drawframe()

	elif event.key == 'l':
		if lt == '.':
			lt = '-'
		else:
			lt = '.'
		drawframe()

	else:

		coeff      = np.random.randint(-100,100,12)/100.
		hlines_main = []
		vlines_main = []
		hlines_sub  = []
		vlines_sub  = []

		for x in np.linspace(-lims,lims,divs+1):
			vlines_main.append(LineObject(np.full(detail,x),np.linspace(-lims,lims,detail)))
			hlines_main.append(LineObject(np.linspace(-lims,lims,detail),np.full(detail,x)))

		for x in np.linspace(-lims+boxwidth/2.,lims-boxwidth/2.,divs):
			vlines_sub.append(LineObject(np.full(detail,x),np.linspace(-lims,lims,detail)))
			hlines_sub.append(LineObject(np.linspace(-lims,lims,detail),np.full(detail,x)))

		drawframe()

fig, ax = plt.subplots()
fig.canvas.mpl_connect('key_press_event', press)
plt.suptitle('Press r to reset coefficients and iterations. | Press l to switch between line styles.\
 \n Press any other key to show next iteration.')
ax.set_aspect('equal')

for x in np.linspace(-lims,lims,divs+1):
	vlines_main.append(LineObject(np.full(detail,x),np.linspace(-lims,lims,detail)))
	hlines_main.append(LineObject(np.linspace(-lims,lims,detail),np.full(detail,x)))

for x in np.linspace(-lims+boxwidth/2.,lims-boxwidth/2.,divs):
	vlines_sub.append(LineObject(np.full(detail,x),np.linspace(-lims,lims,detail)))
	hlines_sub.append(LineObject(np.linspace(-lims,lims,detail),np.full(detail,x)))

drawframe()


plt.show()

