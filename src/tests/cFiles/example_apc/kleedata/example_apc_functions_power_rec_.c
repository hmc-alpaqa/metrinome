#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 1000
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "7854902b86ac4d5a8a751253a6742eb4");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "668f2f38756340b09bc035c86f25d677");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_rec(x, n);
}
