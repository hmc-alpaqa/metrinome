// Copied from src/tests/cFiles/benchmark/06_binarysearch_helper.c
// Function to function binary search version

#include <stdio.h>

int bSearchAsc(int A[], int s, int data);

int main()
{
    int list[100], n, val, i;
    int found;

    printf("Enter the number of elements you want to insert : ");
    scanf("%d", &n);

    printf("Enter element in ascending order \n");

    for (i = 0; i < n; i++)
    {
        printf("Enter element %d : ", i + 1);
        scanf("%d", &list[i]);
    }

    printf("Enter the number you want to search : ");
    scanf("%d", &val);

    found = bSearchAsc(list, n, val);

    if (found ==  - 1)
    {
        printf("\nItem not found");
    }
    else
    {
        printf("\nItem found at %d", found);
    }

    return 0;
}

int bSearchAsc(int A[], int s, int data)
{
    int mid, first = 0, last = s - 1;
    
    while (first <= last)
    {
        mid = (first + last) / 2;
        if (data > A[mid])
        {
            first = mid + 1;
        }
        else if (data < A[mid])
        {

            last = mid - 1;
        }
        else
        {
            return mid + 1;
        }
    }

    return  - 1;
}