#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a3650d0360564d2184ec28984a6c021f");

	int n;
	klee_make_symbolic(&n, sizeof(n), "c330519f4b2541338881f7b55614fafc");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "0e4a65d842c0434aa955faf5fe0534f4");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_iter(A, n, x);
}
