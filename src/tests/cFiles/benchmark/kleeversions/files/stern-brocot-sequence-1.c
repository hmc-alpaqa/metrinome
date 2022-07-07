#include <stdio.h>

typedef unsigned int uint;

/* the sequence, 0-th member is 0 */
uint f(uint n)
{
	return n < 2 ? n : (n&1) ? f(n/2) + f(n/2 + 1) : f(n/2);
}

uint gcd(uint a, uint b)
{
	return a ? a < b ? gcd(b%a, a) : gcd(a%b, b) : b;
}

void find(uint from, uint to)
{
	do {
		uint n;
		for (n = 1; f(n) != from ; n++);
		printf("%3u at Stern #%u.\n", from, n);
	} while (++from <= to);
}
