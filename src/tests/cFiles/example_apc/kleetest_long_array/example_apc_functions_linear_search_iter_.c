#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "6033f875de3b4f2f83d1d793374eba55");

	int n;
	klee_make_symbolic(&n, sizeof(n), "6b50e4877b344bfc92370cdc0c13d0d3");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "e8cfb7c56f794056ae5e6841ed8296c8");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_iter(A, n, x);
}
