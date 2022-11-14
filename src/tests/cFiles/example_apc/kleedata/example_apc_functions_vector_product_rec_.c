#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "44430b0f36944da18bd3a38145c7ce8c");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "c4772c86822145dfbfd5249fdfd9c7ce");

	int n;
	klee_make_symbolic(&n, sizeof(n), "75f1f7229c8b43908f700f264897826e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_rec(A, B, n);
}
