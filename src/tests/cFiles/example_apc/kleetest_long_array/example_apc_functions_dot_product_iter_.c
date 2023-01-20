#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "bceca810a5474e4994855e5f813d72c2");

	int B[SIZE];
	klee_make_symbolic(&B, sizeof(B), "9ae15af73195427b947af5beb39c3caa");

	int n;
	klee_make_symbolic(&n, sizeof(n), "86ea8cd98b5a4c229d4fd98433f5a3a8");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return dot_product_iter(A, B, n);
}
