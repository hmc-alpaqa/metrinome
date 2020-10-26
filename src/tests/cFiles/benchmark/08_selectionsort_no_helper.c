#include <stdio.h>

int main()
{
    int list[100], n;
    printf("Enter Size of Array : ");
    scanf("%d", &n);

    int a;
    for (a = 0; a < n; a++)
    {
        printf("Enter element %d : ", a + 1);
        scanf("%d", &list[a]);
    }

    printf("\nBefore sorting");

    int b;
    printf("\n");
    for (b = 0; b < n; b++)
    {
        printf("%d ", list[b]);
    }

    int s = n;
    int i, j, temp, small;
    for (i = 0; i < s - 1; i++)
    {
        small = i;
        for (j = i + 1; j < s; j++)
        {
            if (list[j] < list[small])
            {
                small = j;
            }
            if (small != i)
            {
                temp = list[i];
                list[i] = list[small];
                list[small] = temp;
            }
        }
    }
    printf("\nAfter sorting");

    int d;
    printf("\n");
    for (d = 0; d < n; d++)
    {
        printf("%d ", list[d]);
    }

    return 0;
}
