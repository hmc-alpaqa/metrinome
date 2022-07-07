#include <stdio.h>

char * base;
void get_diff()
{
	char x;
	if (base - &x < 200)
		printf("%p %d\n", &x, base - &x);
}

void recur()
{
	get_diff();
	recur();
}
