#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "c050ef285b41490b95651bfc87ff0c95");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "069e6c910beb47a184c54664c7f1264e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "32f76dff06474e81a99506ec4a1ded09");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return dot_product_iter(A, B, n);
}
