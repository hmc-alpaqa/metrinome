#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "15c028cc017249e59e88beb9edb2dfb6");

	int n;
	klee_make_symbolic(&n, sizeof(n), "e633d03bbb3e4e8b98097e2499020dce");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_iter(A, n);
}
