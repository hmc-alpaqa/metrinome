#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "91157e78545341e38da0558fb8974f00");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "551baadc003a4539be30a061bfee0efa");

	int n;
	klee_make_symbolic(&n, sizeof(n), "95dc4c22ce104ece89e75c554fd51220");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return dot_product_iter(A, B, n);
}
