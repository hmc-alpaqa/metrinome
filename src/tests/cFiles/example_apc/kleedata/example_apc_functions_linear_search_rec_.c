#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a5e548d79ae044538e4ba92f00b7698c");

	int n;
	klee_make_symbolic(&n, sizeof(n), "11de162227d64714ab5f96f86b00170b");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "e3265499854c4576a008732fe9427b5b");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_rec(A, n, x);
}
