#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "d0c545d68c4c4efb843fa8c4c6747636");

	int n;
	klee_make_symbolic(&n, sizeof(n), "312aa4ab7c1c4abe85db9d7ff99e6988");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "90d9e11d20244245a2896478373ea0da");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_iter(A, n, x);
}
