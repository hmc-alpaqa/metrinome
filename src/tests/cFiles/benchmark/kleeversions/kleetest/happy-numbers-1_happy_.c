#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/happy-numbers-1.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "a28cc2af0a6f4663a2760008be24d183");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return happy(n);
}
