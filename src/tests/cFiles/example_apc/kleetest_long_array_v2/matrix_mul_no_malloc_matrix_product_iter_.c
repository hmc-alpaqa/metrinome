#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/matrix_mul_no_malloc.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "30ebd39527954aecbe719b4eff4b7767");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "4cbccc63490f43dca948bb7333b710d3");

	int n;
	klee_make_symbolic(&n, sizeof(n), "55800b81db66446cb319e47b5dedc067");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int product[SIZE];
	klee_make_symbolic(&product, sizeof(product), "df688d4c4d5e4a92aeca41ce8643e8b6");
	matrix_product_iter(A, B, n, product);
	return 0;
}
