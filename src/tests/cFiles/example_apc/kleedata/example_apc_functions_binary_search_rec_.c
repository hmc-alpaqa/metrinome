#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "9fc8ce76aed84567a2b350384c5c330e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "2d70510762e841b48b4b09b3fb9752ad");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "469b960920aa46a8b2b300395465c67f");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_rec(A, n, x);
}
