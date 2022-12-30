#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "ffd29a6c5bd14ce7a73c4e778ca61bdb");

	int n;
	klee_make_symbolic(&n, sizeof(n), "a95024baabfe4f73b16ddcee0056cdfd");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "2683788758214e27926f9b502a8d79f6");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_rec(A, n, x);
}
