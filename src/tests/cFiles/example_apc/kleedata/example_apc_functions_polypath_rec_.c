#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "17d6ded7211a4951993550508c6b77d1");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return polypath_rec(n);
}
