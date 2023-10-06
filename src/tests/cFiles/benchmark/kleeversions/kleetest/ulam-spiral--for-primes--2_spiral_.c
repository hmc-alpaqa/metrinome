#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ulam-spiral--for-primes--2.c>
#define SIZE 10
int main() {

	int w;
	klee_make_symbolic(&w, sizeof(w), "8a952ba9ab8145b4bd4ba822296e4fdf");
	if ((w<-1) || (w>1024)) {
		 return 0;}

	int h;
	klee_make_symbolic(&h, sizeof(h), "0cff0159acc5435eb51c26602e58442b");
	if ((h<-1) || (h>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "6f0cd12cc7184219bded0d10da0932cb");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int y;
	klee_make_symbolic(&y, sizeof(y), "d9cc076e47524f89ba2ac4d9faf63e9b");
	if ((y<-1) || (y>1024)) {
		 return 0;}
	return spiral(w, h, x, y);
}
