#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/31_sieve_of_eratosthenes.c>
#define SIZE 100
int main() {

	int primes[SIZE];
	klee_make_symbolic(&primes, sizeof(primes), "535b019b01414b2bbfa88e03c4043bb7");

	int n;
	klee_make_symbolic(&n, sizeof(n), "41db362c46da41d0b71cea609f3c190b");
	sieve(primes, n);
	return 0;
}
