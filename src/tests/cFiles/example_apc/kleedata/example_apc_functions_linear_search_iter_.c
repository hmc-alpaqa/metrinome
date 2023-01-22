#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int A[SIZE];
	klee_make_symbolic(&A, sizeof(A), "b8f9ff3adc7349a9b99eb29ad680708e");

	int n;
	klee_make_symbolic(&n, sizeof(n), "95cb62914a544d20898c41c66bda27ba");
	if ((n<-1) || (n>1024)) {
		 return 0;}

	int x;
	klee_make_symbolic(&x, sizeof(x), "0b4f6240e21c40e6ad04b3ed98ea4da2");
	if ((x<-1) || (x>1024)) {
		 return 0;}
	return linear_search_iter(A, n, x);
}
