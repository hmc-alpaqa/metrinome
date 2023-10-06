#include <stdio.h>

#define twidth 5
#define mdr(rmdr, rmp, n)\
    do { *rmp = 0; _mdr(rmdr, rmp, n); } while (0)

void _mdr(int *rmdr, int *rmp, long long n)
{
    /* Adjust r if 0 case, so we don't return 1 */
    int r = n ? 1 : 0;
    while (n) {
        r *= (n % 10);
        n /= 10;
    }

    (*rmp)++;
    if (r >= 10)
        _mdr(rmdr, rmp, r);
    else
        *rmdr = r;
}
