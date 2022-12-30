#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "b7e243a9aff34eb492629a923b96e2f7");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_iter(n);
}
