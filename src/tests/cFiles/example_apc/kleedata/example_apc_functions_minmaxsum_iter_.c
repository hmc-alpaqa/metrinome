#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "ddd474ce9a944ac6a4fac7816a291b41");

	int n;
	klee_make_symbolic(&n, sizeof(n), "ab712c20c0ad44758254fb28d6a593fe");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return minmaxsum_iter(A, n);
}
