#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/02_fib_no_helper.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "6d23515e4ca945d8bb40b7f51fb5505e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return mainn(n);
}
