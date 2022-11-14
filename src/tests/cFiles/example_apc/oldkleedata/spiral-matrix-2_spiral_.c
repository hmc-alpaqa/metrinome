#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/spiral-matrix-2.c>
#define SIZE 10
int main() {

	int w;
	klee_make_symbolic(&w, sizeof(w), "d6c8702ddec94bcb928a1ed7a2c1bbf0");
	if ((w<-1) || (w>1024)) {
		 return 0;}

	int h;
	klee_make_symbolic(&h, sizeof(h), "9c8161fc645d41e8996edf436c213aa8");
	if ((h<-1) || (h>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "5986696e981841a39d0c1d65ecd33818");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int y;
	klee_make_symbolic(&y, sizeof(y), "7e6d198bfd3a45298a8f9a8bb991633e");
	if ((y<-1) || (y>1024)) {
		 return 0;}
	return spiral(w, h, x, y);
}
