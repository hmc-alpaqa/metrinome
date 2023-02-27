#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/spiral-matrix-2.c>
#define SIZE 10
int main() {

	int w;
	klee_make_symbolic(&w, sizeof(w), "3ac2f8a5c28643cf850fd76b8d2b03ae");
	if ((w<-1) || (w>1024)) {
		 return 0;}

	int h;
	klee_make_symbolic(&h, sizeof(h), "47a83e44160e4eafb85b6f9cf1b27e55");
	if ((h<-1) || (h>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "a212f9f7b69e444e8d3c97c18c32c0d8");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int y;
	klee_make_symbolic(&y, sizeof(y), "21a613f1e64c4032bcbbd1e27451bf12");
	if ((y<-1) || (y>1024)) {
		 return 0;}
	return spiral(w, h, x, y);
}
