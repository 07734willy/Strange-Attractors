CC=gcc
CFLAGS=-g -Ofast -funsafe-math-optimizations
LIBS=-lX11 -lm
DEPS = render.h attractor.h transform.h
OBJ =  render.o attractor.o transform.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

all: $(OBJ)
	$(CC) -o render $(OBJ) $(CFLAGS) $(LIBS)

clean:
	rm -f *.o render

.PHONY: all clean
