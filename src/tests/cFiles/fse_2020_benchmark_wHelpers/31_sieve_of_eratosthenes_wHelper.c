#include <stdio.h>
#include <stdlib.h>

// from
// https://www.programminglogic.com/the-sieve-of-eratosthenes-implemented-in-c/
// method 2

// use a single array, fill it with 1s, and then put 0s on all the numbers that
// are not primes. The program below prints the first 650,000 or so primes using
// this method

void initializePrimes(int n, int primes[]);
void setZeros(int i, int primes[], int n);

void sieve(int primes[], int n) {
  int i, j;

  initializePrimes(n, primes);

  for (i = 2; i < n; i++)
    if (primes[i])
      setZeros(i, primes, n);
  return;
}

void initializePrimes(int n, int primes[]){
  for (int i = 2; i < n; i++) primes[i] = 1;
}

void setZeros(int i, int primes[], int n){
  for (int j = i; i * j < n; j++) primes[i * j] = 0;
}