
// from https://www.programminglogic.com/the-sieve-of-eratosthenes-implemented-in-c/
// method 2


#include <stdio.h>
#include <stdlib.h>

// use a single array, fill it with 1s, and then put 0s on all the numbers that are not primes.
// The program below prints the first 650,000 or so primes using this method
int sieveOfEra(int LIMIT) {
    unsigned long long int i,j;
    int *primes;
    int z = 1;

    primes = malloc(sizeof(int)*LIMIT);

    for (i=2;i<LIMIT;i++)
        primes[i]=1;

    for (i=2;i<LIMIT;i++)
        if (primes[i])
            for (j=i;i*j<LIMIT;j++)
                primes[i*j]=0;

    for (i=2;i<LIMIT;i++)
        if (primes[i])
            printf("%dth prime = %dn",z++,i);

    return 0;
}

int main(){
    return sieveOfEra(10000000);
}