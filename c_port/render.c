#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "render.h"
#include "attractor.h"
#include "transform.h"

Display *display;
int screen;
Window root;
Visual *visual;
Window win;

void updateXImage(XImage *img, uint8_t r, uint8_t g, uint8_t b) {
	/* updates the XImage to be filled with a solid RGB color */
	for (int i = 0; i < 4 * img->width * img->height; i += 4) {
		img->data[i + 0] = b;
		img->data[i + 1] = g;
		img->data[i + 2] = r;
	}
}

void initXWindows(void) {
	/* perform initialization logic for the XWindow, storing values in global constants */
	display = XOpenDisplay(NULL);
	screen = DefaultScreen(display);
	root = RootWindow(display, screen);
	visual = DefaultVisual(display, screen);
	win = XCreateSimpleWindow(display, root, 50, 50, WIDTH, HEIGHT, 1, 0, 0);
	
	int eventMask = ButtonPressMask | ButtonReleaseMask | PointerMotionMask;
	XGrabPointer(display, win, False, eventMask, GrabModeAsync, GrabModeAsync, None, None, CurrentTime);
	XSelectInput(display, win, ExposureMask | KeyPressMask | eventMask);
	
	XMapWindow(display, win);
	XFlush(display);
}

void renderXImage(XImage *img) {
	/* main event loop which catches events and handles them appropriately */
	GC defaultGC = DefaultGC(display, screen);
	int mouseDown = 0;
	
	XEvent event;
	while(1) {
		XNextEvent(display, &event);
		switch (event.type) {
			case KeyPress: return;
			case Expose:
				XPutImage(display, win, defaultGC, img, 0, 0, (WIDTH-XRES)/2, (HEIGHT-YRES)/2, XRES, YRES);
				break;
			case ButtonPress:
				if (event.xbutton.button == Button1)
					mouseDown = 1;
				break;
			case ButtonRelease:
				if (event.xbutton.button == Button1)
					mouseDown = 0;
				break;
			case MotionNotify:
				if (mouseDown && XEventsQueued(display, QueuedAfterFlush) < 1) {
					int x = event.xmotion.x;
					int y = event.xmotion.y;
					updateXImage(img, x & 255, 20, y & 255);
					XPutImage(display, win, defaultGC, img, 0, 0, (WIDTH-XRES)/2, (HEIGHT-YRES)/2, XRES, YRES);
				}
				break;
			default: break;
		}
	}
}


int main(int argc,char **argv) {
	/* entry point, seeds the RNG and creates the windows and attractors */
	initXWindows();
	
	srand(2234);
	srand(1111); // random blue patches
	srand(1000); // same
	srand(3215); // kinda neat
	srand(4440); // REALLY BLUE
	srand(7540); // mostly empty
	srand(3452);
	srand(1);
	srand(4);
	char *data = malloc(XRES * YRES * 4);
	XImage *img = XCreateImage(display, visual, DefaultDepth(display, screen), ZPixmap,
			0, data, XRES, YRES, 32, 0);

	updateXImage(img, 200, 20, 20);

	char seed[] = "ODPUMUHYVHMSYKLVJQHGPHEGIJKPFCFPQIFAUNOKFJFCSJGQUCFFKLYESOQL";
	char seed2[] = "KUIGFJAQPTYSSAIWUTSYRXMFFMNVBMLLJTUOGUFXQHQKHCJEVCGODSTIHJEJ";
	char seed3[] = "KLYCUAVJBAQBNUDRICOHHKPVIHIBSPIDDHHBJFKLFEOVBTPJWGSGRKCARNBM";
	char seed4[] = "PIIGEDYLHLKWHQXFCUPHPRNGSBIYBYSTKDAOGCCONONUGMDKJSRBMFJFJSGK";

	double *attractor = generateAttractor(NULL);

	printf("Attractor constructed\n");
	positionsToBGRA(img->data, attractor);
	printf("Attractor transformed\n");

	renderXImage(img);

	XCloseDisplay(display);
	free(attractor);
	free(data);
	
	return 0;
}
