#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "12a76c8be3aa487ea90fd0cef7902bce");

	int n;
	klee_make_symbolic(&n, sizeof(n), "10b75c996ee84b3eb9d97bd78f01435b");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return max_value_rec(A, n);
}
