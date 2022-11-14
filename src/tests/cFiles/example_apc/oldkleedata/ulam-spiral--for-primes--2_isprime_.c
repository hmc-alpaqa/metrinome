#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ulam-spiral--for-primes--2.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "c1509d24d5264281b972ad363bc17c5c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return isprime(n);
}
