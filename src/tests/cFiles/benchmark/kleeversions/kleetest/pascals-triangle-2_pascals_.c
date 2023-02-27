#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/pascals-triangle-2.c>
#define SIZE 10
int main() {

	int *x;
	klee_make_symbolic(&x, sizeof(x), "910aaf4af132462db40603531309b581");

	int *y;
	klee_make_symbolic(&y, sizeof(y), "b7bff9a70c844e389d9462c9f9a3f10d");

	int d;
	klee_make_symbolic(&d, sizeof(d), "69094fb4d86c4afca38ba612e8c82bcc");
	if ((d<-1) || (d>1024)) {
		 return 0;}
	return pascals(x, y, d);
}
