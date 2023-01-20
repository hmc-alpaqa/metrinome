#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "bf18b8078f494af9af30ffad775912b0");

	int n;
	klee_make_symbolic(&n, sizeof(n), "7d6ace125237408790671d4c63df8e5e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	selection_sort(A, n);
	return 0;
}
