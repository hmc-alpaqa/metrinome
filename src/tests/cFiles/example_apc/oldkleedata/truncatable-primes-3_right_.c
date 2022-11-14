#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/truncatable-primes-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "679c32ecd33d4943a1d6ad35b3ccd7df");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	right(n);
	return 0;
}
