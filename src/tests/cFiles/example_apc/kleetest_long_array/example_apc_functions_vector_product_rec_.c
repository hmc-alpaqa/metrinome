#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "f480fff1d2f24c7b98987972c77397b5");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "814867e0775f4f388ccc099ec42163bd");

	int n;
	klee_make_symbolic(&n, sizeof(n), "c2dca48bd42b46c8bba38bd5ba4a5c98");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_rec(A, B, n);
}
