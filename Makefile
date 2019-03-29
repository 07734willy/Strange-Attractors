all:
	gcc -c -fPIC -Ofast -funsafe-math-optimizations iterator.c -o iterator.o
	gcc -shared -Wl,-soname,iterator.so -o iterator.so iterator.o

clean:
	rm iterator.o
