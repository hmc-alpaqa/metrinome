#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "49f22ac6c10a41c689964251a4c1bdf5");

	int n;
	klee_make_symbolic(&n, sizeof(n), "a6194b1b3248405ea516c52afe4f99d3");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "64ab9c5242e74a47a4144aaca431d4cd");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_rec(A, n, x);
}
