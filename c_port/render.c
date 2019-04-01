#include <GL/glew.h>
#include <SDL.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include "render.h"
#include "attractor.h"
#include "transform.h"


void render(SDL_Window* window, double *attractor, double *rgb) {
	glClearColor(0.0, 0.0, 0.0, 1.0);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glEnable (GL_BLEND);
	//glBlendFunc(GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR);
	
	double dampen = 0.7;
	glBlendColor(ALPHA * dampen, ALPHA * dampen, ALPHA * dampen, 1);
	glBlendFunc(GL_CONSTANT_COLOR, GL_ONE);
	glBegin(GL_POINTS);
	for (int i = 0; i < 3 * NUM_POSITIONS; i += 3) {
		glColor4d(rgb[i + 0],
				rgb[i + 1],
				rgb[i + 2],
				1);
		glVertex3d(attractor[i + 0], 
				attractor[i + 1],
				attractor[i + 2]);
	}
	glEnd();

	glFlush();
	SDL_GL_SwapWindow(window);
}

void mainLoop(SDL_Window* window, double *attractor) {
	glClearColor(0.0, 0.0, 0.0, 1.0);
	glPointSize(1.0);
	//glMatrixMode(GL_PROJECTION);
	//glTranslated(0, 0, 1);
	double* rgb = positionsToRGB(attractor);
	int dx, dy;
	while (1) {
		SDL_Event ev;
		while (SDL_PollEvent(&ev)) {
			switch (ev.type) {
				case SDL_QUIT:
					return;
				case SDL_MOUSEMOTION:
					SDL_GetRelativeMouseState(&dx, &dy);
					double delta = 1.0;
					glRotated(dx * delta, 0, 1, 0);
					//glRotated(-dy * delta, 1, 0, 0);
					break;
				default: break;
			}
		}
		render(window, attractor, rgb);
	}
}

int main(int argc, char* argv[]) {
	SDL_Init(SDL_INIT_VIDEO);
	SDL_Window* window = SDL_CreateWindow("Point Cloud",
			SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
			XRES, YRES,
			SDL_WINDOW_RESIZABLE | SDL_WINDOW_OPENGL);
	SDL_GLContext glcontext = SDL_GL_CreateContext(window);

	GLenum  glew_status = glewInit();

	srand(2234);
	srand(1111); // random blue patches
	srand(1000); // same
	srand(3215); // kinda neat
	srand(4440); // REALLY BLUE
	srand(7540); // mostly empty
	srand(3452);

	char seed[] = "ODPUMUHYVHMSYKLVJQHGPHEGIJKPFCFPQIFAUNOKFJFCSJGQUCFFKLYESOQL";
	char seed2[] = "KUIGFJAQPTYSSAIWUTSYRXMFFMNVBMLLJTUOGUFXQHQKHCJEVCGODSTIHJEJ";
	char seed3[] = "KLYCUAVJBAQBNUDRICOHHKPVIHIBSPIDDHHBJFKLFEOVBTPJWGSGRKCARNBM";
	char seed4[] = "PIIGEDYLHLKWHQXFCUPHPRNGSBIYBYSTKDAOGCCONONUGMDKJSRBMFJFJSGK";

	double *attractor = generateAttractor(seed3);

	printf("Attractor constructed\n");
	//positionsToBGRA(img->data, attractor);
	//printf("Attractor transformed\n");

	mainLoop(window, attractor);
	
	SDL_GL_DeleteContext(glcontext);
	SDL_DestroyWindow(window);
	SDL_Quit();
}
