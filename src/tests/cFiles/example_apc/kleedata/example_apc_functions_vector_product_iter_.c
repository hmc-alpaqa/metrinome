#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "ac372a263b4144c28cba4ce66d0004ce");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "d2e7a32acc7a417d9ce0f68b9124b33d");

	int n;
	klee_make_symbolic(&n, sizeof(n), "0965dd51f0df4cf48b6bec8240078a74");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_iter(A, B, n);
}
