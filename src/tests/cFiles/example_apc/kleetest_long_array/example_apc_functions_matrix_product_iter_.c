#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "c22dcdae3012432c87be6f51511eec55");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "60a93bedeb0640e2acb0b05eeaa6bee0");

	int n;
	klee_make_symbolic(&n, sizeof(n), "96b1136724604cd3baaa2e6ecd7c1351");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return matrix_product_iter(A, B, n);
}
