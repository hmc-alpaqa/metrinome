#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "2de5ac8c0eb54ca88ae710d1093537ff");
	return minmaxsum_iter(A);
}
