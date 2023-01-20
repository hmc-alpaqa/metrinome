#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "e7d85d474d54498f83a0155bc54e2d9c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return polypath_rec(n);
}
