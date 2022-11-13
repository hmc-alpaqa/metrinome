#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/pascals-triangle-2.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "10d0cd20f08f41058deba7f77f9a652b");

	int *y;
	klee_make_symbolic(&y, sizeof(y), "849a7f9361c4411983dc44ba95ec7349");

	int d;
	klee_make_symbolic(&d, sizeof(d), "57a8692e788046a1915ae3aa576bc3cc");
	if ((d<-1) || (d>1024)) {
		 return 0;}
	return pascals(x, y, d);
}
