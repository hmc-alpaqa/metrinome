#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "e062cfe5f9ec4f90b760ba50892dbab7");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_rec(n);
}
