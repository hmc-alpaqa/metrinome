#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "36b6054408704f749bd8f4a8d7836fe9");

	int n;
	klee_make_symbolic(&n, sizeof(n), "c4a28da6d00a44699b378c235cfca7bb");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "2759ad187a99402b93500540514c6238");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_iter(A, n, x);
}
