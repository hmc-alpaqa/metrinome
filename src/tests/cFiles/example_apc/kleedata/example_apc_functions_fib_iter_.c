#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "13fe0771590b430e83299f006b93dc0e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_iter(n);
}
