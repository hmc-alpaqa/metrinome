#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "e982958b8c5a48d782f845d676b46d47");

	int n;
	klee_make_symbolic(&n, sizeof(n), "567dee89a4de42be973b0d129078fd2e");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "cf6fa57a9e7f43918a69b49b55f27cf9");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return binary_search_iter(A, n, x);
}
