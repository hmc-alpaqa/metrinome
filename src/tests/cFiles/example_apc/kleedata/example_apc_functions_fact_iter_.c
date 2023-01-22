#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "e29ddaa6ea32496c9c0c2a3a8a6b2a9c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_iter(n);
}
