#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a4c3fd80a5c4499ebe7734f33250ec4b");

	int n;
	klee_make_symbolic(&n, sizeof(n), "7f5fda3e9a9d4423baa45dce23d3dbb8");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_rec(A, n);
}
