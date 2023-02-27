#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/iterated-digits-squaring-2.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "91ee233b30744431afdd4c1055f53a83");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorial(n);
}
