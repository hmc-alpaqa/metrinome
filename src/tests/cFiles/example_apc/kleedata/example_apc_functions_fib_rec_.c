#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "14805202dd934221a5520bf2a6536be9");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_rec(n);
}
