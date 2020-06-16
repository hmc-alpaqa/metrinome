#include "31_sieve_of_eratosthenes.c"

#define MAXVAL 10000

int main() {
  int primes[MAXVAL];
  sieve(primes, MAXVAL);
  for (int i = 2; i < MAXVAL; i++)
    if (primes[i]) printf("%d is prime\n", i);
}
