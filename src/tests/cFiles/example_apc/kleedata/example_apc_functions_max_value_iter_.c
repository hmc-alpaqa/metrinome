#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "7a7a5b8521d94411a4861ef406b5dd10");

	int n;
	klee_make_symbolic(&n, sizeof(n), "e9c20745ab1b4e6fa647daf653181ff9");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_iter(A, n);
}
