#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "91520515bee641b0b8d1d8e0eebd92ee");

	int n;
	klee_make_symbolic(&n, sizeof(n), "3c04c2adb4da42e09db3964cf6ed31bf");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	mergeSort(A, n);
	return 0;
}
