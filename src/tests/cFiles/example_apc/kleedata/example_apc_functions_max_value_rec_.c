#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "11573b065bd44e36b19683191460fb2e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "b87ba35bb0c344c29a1b2080f026ec34");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_rec(A, n);
}
