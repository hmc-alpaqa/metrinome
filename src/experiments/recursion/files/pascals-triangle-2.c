#include <stdio.h>

#define D 32
int pascals(int *x, int *y, int d)
{
	int i;
	for (i = 1; i < d; i++)
		printf("%d%c", y[i] = x[i - 1] + x[i],
			i < d - 1 ? ' ' : '\n');

	return D > d ? pascals(y, x, d + 1) : 0;
}
