#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "ce60d80019854ac4a11cf195fdca9a47");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "8e3dff73bbd843448994e95bffd5520e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "1223419e3cc44f9eb54a9b698c37f551");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return vector_product_iter(A, B, n);
}
