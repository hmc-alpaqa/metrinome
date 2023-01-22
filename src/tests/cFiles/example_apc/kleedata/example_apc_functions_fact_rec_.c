#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "cb52b90d805c4a529470217dc2dac4be");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_rec(n);
}
