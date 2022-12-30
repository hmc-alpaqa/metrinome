#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "2f7f094cefcc441cbc07f4aa732d5d1f");

	int n;
	klee_make_symbolic(&n, sizeof(n), "e8bc528eadf6494cb1198ffcda4453b9");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	selection_sort(A, n);
	return 0;
}
