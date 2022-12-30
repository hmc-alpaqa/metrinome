#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a5ab1c56f5894ab58749cb9469baaa48");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "649b5a6511c548de84c1250f42e67996");

	int n;
	klee_make_symbolic(&n, sizeof(n), "0eac5bfc40b4436db7f55f4e102832ff");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_iter(A, B, n);
}
