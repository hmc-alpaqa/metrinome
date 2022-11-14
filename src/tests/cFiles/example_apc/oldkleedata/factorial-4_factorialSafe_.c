#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/factorial-4.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "b2b733943efd4db1bb66d80deb7d4d5d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return factorialSafe(n);
}
