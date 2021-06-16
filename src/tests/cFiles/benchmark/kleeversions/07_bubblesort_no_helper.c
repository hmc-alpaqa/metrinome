#include <stdio.h>
#include <stdlib.h>

int mainn(int list[], int size)
{
    // int list[100], n;
    // printf("Enter Size of Array : ");
    // scanf("%d", &n);
    //
    // int a;
    // for (a = 0; a < n; a++)
    // {
    //     printf("Enter element %d : ", a + 1);
    //     scanf("%d", &list[a]);
    // }
    //
    // printf("\nBefore sorting");
    int x;
    int n = size;
    // int list[size];
    // srand(0);
    // for (x = 0; x < size; x++) {
    //     list[x] = rand();
    // }

    int b;
    // printf("\n");
    // for (b = 0; b < n; b++)
    // {
    //     printf("%d ", list[b]);
    // }

    int i, j, temp;
    int s = n;
    for (i = 0; i < s - 1; i++)
    {
        for (j = 0; j < (s - 1 - i); j++)
        {
            if (list[j] > list[j + 1])
            {
                temp = list[j];
                list[j] = list[j + 1];
                list[j + 1] = temp;
            }
        }
    }
    // printf("\nAfter sorting");
    //
    // int d;
    // printf("\n");
    // for (d = 0; d < n; d++)
    // {
    //     printf("%d ", list[d]);
    // }

    return 0;
}
