#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "3b4ff42ba840452fb075baba1b904583");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "d2a9622d41564b9881b1c3ab37975574");

	int n;
	klee_make_symbolic(&n, sizeof(n), "59e9a16e8ef94e95bbf79a3b1f97cecc");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return dot_product_iter(A, B, n);
}
