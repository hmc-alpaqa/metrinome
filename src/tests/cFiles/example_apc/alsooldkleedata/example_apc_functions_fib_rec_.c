#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "6eb459170cf64c86844d10051bc10762");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_rec(n);
}
