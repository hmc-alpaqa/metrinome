#include "31_sieve_of_eratosthenes.c"

int main() {
  int const n = 100;
  int primes[n];
  sieve(primes, n);
  for (int i = 2; i < n; i++)
    if (primes[i]) printf("%d is prime\n", i);
}
