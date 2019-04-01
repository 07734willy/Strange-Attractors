CC=gcc
CFLAGS=$(shell sdl2-config --cflags) $(EXTRA_CFLAGS)
LDLIBS=$(shell sdl2-config --libs) -lGLEW $(EXTRA_LIBS)
EXTRA_CFLAGS?=-I.
EXTRA_LIBS?=-lGL -lm
DEPS = render.h attractor.h transform.h
OBJ =  render.o attractor.o transform.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	$(CC) -o render $(OBJ) $(CFLAGS) $(LDLIBS)

clean:
	rm -f *.o

.PHONY: all clean
