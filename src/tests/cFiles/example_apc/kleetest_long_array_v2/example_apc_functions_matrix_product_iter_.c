#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "42fd10dc04a94856bf124c7211c3d08a");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "23d7b1d1b91546079e38f586b7324c81");

	int n;
	klee_make_symbolic(&n, sizeof(n), "9f1397a185464eec89c34fa91f6bb56d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return matrix_product_iter(A, B, n);
}
