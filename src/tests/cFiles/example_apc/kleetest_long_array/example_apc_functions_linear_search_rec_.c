#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "bdd8181d39d34d88a7b19aff67d252e8");

	int n;
	klee_make_symbolic(&n, sizeof(n), "ae9eede02fe6497fa9e01aed8b2438b4");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "1487879cab524d9780d811715d931cc6");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_rec(A, n, x);
}
