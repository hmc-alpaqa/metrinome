#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a1fae8b16d7c4eeb9f96de9c17bffd56");
	return minmaxsum_iter(A);
}
