#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "a24829c4dca14610adc286d40507ffaf");

	int n;
	klee_make_symbolic(&n, sizeof(n), "170444b6bfd5416d8c87daa576ebd84b");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "8ffaa2cc9aeb488f9b450b67e84b5133");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_rec(A, n, x);
}
