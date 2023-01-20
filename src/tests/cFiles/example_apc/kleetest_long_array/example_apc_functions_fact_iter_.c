#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "9512140e7aff49d79e49c4d35811fc89");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fact_iter(n);
}
