#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a4d84b6761f643db810043dc4af25bea");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "7ffef3010e3443b4b164e661f36d8c9c");

	int n;
	klee_make_symbolic(&n, sizeof(n), "f67c0e6370464d4abadbefdda7264cd8");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_rec(A, B, n);
}
