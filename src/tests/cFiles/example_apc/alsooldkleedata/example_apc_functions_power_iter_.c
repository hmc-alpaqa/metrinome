#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/example_apc_functions.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "7229c2899ea944bf9e41c0e252f6fb7e");
	if ((x<-1) || (x>1024)) {
		 return 0;}

	int n;
	klee_make_symbolic(&n, sizeof(n), "95d014635da94be49aa472f5243ce5be");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return power_iter(x, n);
}
