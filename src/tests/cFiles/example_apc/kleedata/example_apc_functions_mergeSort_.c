#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "f6c6bf508582480db3d398232d6cb65d");

	int n;
	klee_make_symbolic(&n, sizeof(n), "d3f1d93f7b5e4644bccf32a5648aadc7");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	mergeSort(A, n);
	return 0;
}
