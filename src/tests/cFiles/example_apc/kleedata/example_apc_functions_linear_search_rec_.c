#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "e5498c22b0b24a9aa6b5462ae0624492");

	int n;
	klee_make_symbolic(&n, sizeof(n), "f63e315962c0433c97881e41914b1006");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "34b651de3cd04f23b19ea475762ce9e9");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_rec(A, n, x);
}
