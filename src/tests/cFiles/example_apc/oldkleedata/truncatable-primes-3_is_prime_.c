#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/truncatable-primes-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "47c70d3408684f51aaf94bcb21c4c50c");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	return is_prime(n);
}
