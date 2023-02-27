#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/ulam-spiral--for-primes--2.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "f9e7458ec3a74c69ad470697d6b47c0e");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return isprime(n);
}
