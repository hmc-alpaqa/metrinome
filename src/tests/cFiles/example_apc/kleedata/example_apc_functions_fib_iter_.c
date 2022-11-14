#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "35da5c2d86a84082ac60f1fbaea955cd");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_iter(n);
}
