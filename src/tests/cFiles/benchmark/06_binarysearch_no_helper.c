#include <stdio.h>

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

    int s = n;
    int data = val;

    int mid, first = 0, last = s - 1;
    
    while (first <= last)
    {
        mid = (first + last) / 2;
        if (data > list[mid])
        {
            first = mid + 1;
        }
        else if (data < list[mid])
        {

            last = mid - 1;
        }
        else
        {
            found = mid + 1;
        }
    }

    found = - 1;

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
