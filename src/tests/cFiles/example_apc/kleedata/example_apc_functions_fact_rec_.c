#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "cf005be01f9d43dcb198e698cfd54a00");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_rec(n);
}
