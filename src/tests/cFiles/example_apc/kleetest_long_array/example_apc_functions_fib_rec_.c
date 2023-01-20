#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "8a699c016a934930ba53536d8d6e9f1c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return fib_rec(n);
}
