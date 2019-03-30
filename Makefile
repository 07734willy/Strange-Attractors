all:
	gcc render.c attractor.c transform.c -Ofast -funsafe-math-optimizations -lX11 -lm -o render

clean:
	$(RM) render
