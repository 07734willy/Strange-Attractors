all:
	gcc -c -fPIC -Ofast -funsafe-math-optimizations helper.c -o helper.o
	gcc -shared -Wl,-soname,helper.so -o helper.so helper.o

clean:
	$(RM) helper.o helper.so
