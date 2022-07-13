#include <stdio.h>
#include <stdlib.h>

int isprime(int n)
{
	int p;
	for (p = 2; p*p <= n; p++)
		if (n%p == 0) return 0;
	return n > 2;
}

int spiral(int w, int h, int x, int y)
{
	return y ? w + spiral(h - 1, w, y - 1, w - x - 1) : x;
}
