#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "684ce44987bc4627b817832a93e9d241");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "e123f053f6504b97a5dbc6876d31bd2e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "593be5dd051347b69c559ecefdd22553");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_iter(A, B, n);
}
