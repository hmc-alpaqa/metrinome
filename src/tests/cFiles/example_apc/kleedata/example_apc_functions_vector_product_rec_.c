#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "513a50e520e24a7686cee48493d2c131");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "2e11789236e44567a99509b37a38afda");

	int n;
	klee_make_symbolic(&n, sizeof(n), "948ea1f798f944dfba30e79d2e53e4c0");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_rec(A, B, n);
}
