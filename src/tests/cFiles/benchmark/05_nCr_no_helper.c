#include <stdio.h>

int main()
{
    int n, r;
    printf("Enter the value of n :");
    scanf("%d", &n);

    printf("Enter the value of r :");
    scanf("%d", &r);

    int fact_n, fact_r, fact_nr;

    int i;
    int fact = 1;

    for (i = 1; i <= n; i++)
    {
        fact = fact * i;
    }
    fact_n = fact;

    fact = 1;
    for (i = 1; i <= r; i++)
    {
        fact = fact * i;
    }
    fact_r = fact;

    fact = 1;
    for (i = 1; i <= n-r; i++)
    {
        fact = fact * i;
    }
    fact_nr = fact;

    int c;

    c = fact_n / (fact_r * fact_nr);


    printf("\nCombinations : %d", c);

    return 0;
}
