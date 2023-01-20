#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "f13a44634f8e48bda8059c556c5fc17e");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "1b427759795f40c59e366084013011eb");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_rec(x, n);
}
