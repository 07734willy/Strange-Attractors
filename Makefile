all:
	gcc -c -fPIC -O3 -ffast-math -funsafe-math-optimizations iterator.c -o iterator.o
	gcc -shared -Wl,-soname,iterator.so -o iterator.so iterator.o

clean:
	rm iterator.o
