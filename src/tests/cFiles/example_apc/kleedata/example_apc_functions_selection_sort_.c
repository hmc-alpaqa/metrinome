#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "99ced1e37a84419cb7ba5b19e3538cfa");

	int n;
	klee_make_symbolic(&n, sizeof(n), "ae8a38fdf7e04faf96dd333c8917c0ba");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	selection_sort(A, n);
	return 0;
}
