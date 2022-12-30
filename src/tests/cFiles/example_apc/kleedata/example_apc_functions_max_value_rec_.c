#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "152aad5b693d4d9f882034bbd6aedfab");

	int n;
	klee_make_symbolic(&n, sizeof(n), "5e546193ca9546cca96f7717e6f0d11d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_rec(A, n);
}
