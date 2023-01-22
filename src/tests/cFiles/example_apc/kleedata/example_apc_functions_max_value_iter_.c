#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "61bce78d80664ec79b0de26ca784b8eb");

	int n;
	klee_make_symbolic(&n, sizeof(n), "44cfe1da9f6d4b28bacff59e9c7b32ec");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_iter(A, n);
}
