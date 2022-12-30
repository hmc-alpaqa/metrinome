#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "9dfe0b4f593a45cca2dc8e113a5d09b6");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "5ff2613b00394a5b9ee52f4a17947873");

	int n;
	klee_make_symbolic(&n, sizeof(n), "5f5836835fce446f8fdbb0900637495f");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return matrix_product_iter(A, B, n);
}
