#include <stdio.h>

int main_func(int n)
{
    int sum = 0, i, num;
    // printf("Enter number: ");
    // scanf("%d", &n);
    num = n;
    while (n != 0)
    {
        i = n % 10;
        sum = sum + (i * i * i);
        n = n / 10;
    }
    if (sum == num)
    {
        return 1;
    }
    else
    {
        return 0;
    }
    return 0;
}
