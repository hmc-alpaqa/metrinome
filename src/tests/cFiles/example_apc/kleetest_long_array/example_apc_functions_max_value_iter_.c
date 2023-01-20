#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "2d3ca54cecef4fd98ba18b44f14f4b48");

	int n;
	klee_make_symbolic(&n, sizeof(n), "a390c1fe11b34970bbc1f2832bbba23e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_iter(A, n);
}
