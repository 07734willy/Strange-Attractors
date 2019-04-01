#ifndef RENDER_H
#define RENDER_H

#define MIN(X, Y) (((Y) < (X)) ? (Y) : (X))
#define MAX(X, Y) (((Y) > (X)) ? (Y) : (X))

#define SHRINK_RATIO 19 / 20

#define XRES (MIN(WIDTH, HEIGHT) * SHRINK_RATIO)
#define YRES (MIN(WIDTH, HEIGHT) * SHRINK_RATIO)

#define WIDTH 1800
#define HEIGHT 900

#define ALPHA 0.010
#define ALPHA_MIN 0.25

#endif
