#include <stdio.h>

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

    int s = n;
    int i, j, temp;

    for (i = 1; i < s; i++)
    {
        temp = list[i];
        j = i - 1;
        while ((temp < list[j]) && (j >= 0))
        {
            list[j + 1] = list[j];
            j--;
        }
        list[j + 1] = temp;
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