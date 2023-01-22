#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "452be0585e344fb0b25c2e64f64556e7");

	int n;
	klee_make_symbolic(&n, sizeof(n), "83ab13c00deb46c0b70f0d773ddc02a0");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	selection_sort(A, n);
	return 0;
}
