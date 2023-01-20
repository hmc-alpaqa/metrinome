#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "e9b900cd15f546daac85b7918ab157db");

	int n;
	klee_make_symbolic(&n, sizeof(n), "0d7442eb0abf4876b06a6509c7ac4c19");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	mergeSort(A, n);
	return 0;
}
