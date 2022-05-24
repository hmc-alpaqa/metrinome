#include <stdio.h>
#include <stdlib.h>

int mainn(int list [], int size)
{
    // int list[100], n, val, i;
    int found, i, n;
    int val = 10;

    // printf("Enter the number of elements you want to insert : ");
    // scanf("%d", &n);
    //
    // printf("Enter element in ascending order \n");
    //
    // for (i = 0; i < n; i++)
    // {
    //     printf("Enter element %d : ", i + 1);
    //     scanf("%d", &list[i]);
    // }
    //
    // printf("Enter the number you want to search : ");
    // scanf("%d", &val);

    n = size;
    // int list[size];
    // srand(0);
    // for (i = 0; i < size; i++) {
    //     list[i] = rand();
    // }


    int s = n;
    int data = val;

    int mid, first = 0, last = s - 1;

    while (first <= last)
    {
        int t1 = first/2;
        int t2 = last/2;
        mid = t1 + t2;
        if (data > list[mid])
        {
            first = mid + 1;
        }
        // else if (data < list[mid])
        // {
        //
        //     last = mid - 1;
        // }
        // else
        // {
        //     found = mid + 1;
        //     break;
        // }
    }

    found = - 1;

    // if (found ==  - 1)
    // {
    //     printf("\nItem not found");
    // }
    // else
    // {
    //     printf("\nItem found at %d", found);
    // }

    return 0;
}
