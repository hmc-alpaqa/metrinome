#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/truncatable-primes-3.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "241a32c1a3ac4b39af53c9aa4284aae3");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	right(n);
	return 0;
}
