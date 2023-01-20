#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "67e2c33486f848d7bc2ecc8af71d327d");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "cb1333ac92d24617bfa64c1bd6f72ea4");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_iter(x, n);
}
