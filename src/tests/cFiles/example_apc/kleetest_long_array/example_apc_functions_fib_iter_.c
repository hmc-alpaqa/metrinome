#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f45ea588065849a084915761ff6750b5");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_iter(n);
}
