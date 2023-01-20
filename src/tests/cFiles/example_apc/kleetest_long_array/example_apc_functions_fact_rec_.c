#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c3b0d82a72fd4443b0fa59bd884674af");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_rec(n);
}
