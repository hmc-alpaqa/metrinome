#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "8e303b1a7c144b3f84653c02e3cbb5d2");

	int n;
	klee_make_symbolic(&n, sizeof(n), "eb5f297bd2984792bb4594aee5852f9c");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "02787b3d522e407c97ac237c4509d567");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_iter(A, n, x);
}
