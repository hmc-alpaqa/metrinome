#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "8aece47b8bc04f5184c1785ad2edd919");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_iter(n);
}
