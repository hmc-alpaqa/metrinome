#include <stdio.h>
// MEMORY BAD, too much memory
int mainn(int size)
{
    // int A[100], B[100], C[200], i, n, m, k;

    // printf("\nEnter number of elements you want to insert in first array :");
    // scanf("%d", &n);
    //
    // printf("Enter element in descending order\n");
    //
    // for (i = 0; i < n; i++)
    // {
    //     printf("Enter element %d :", i + 1);
    //     scanf("%d", &A[i]);
    // }
    //
    // printf("\nEnter number of elements you want to insert in second array :");
    // scanf("%d", &m);
    //
    // printf("Enter element in descending order\n");
    //
    // for (i = 0; i < m; i++)
    // {
    //     printf("Enter element %d :", i + 1);
    //     scanf("%d", &B[i]);
    // }
    int i,k;
    int x;
    int n = size;
    int m = size;
    int A[size];
    int B[size];
    int C[2*size];
    srand(0);
    for (x = 0; x < size; x++) {
        A[x] = rand();
        B[x] = rand();
    }

    // merge(A, B, C, n, m, &k);

    i = 0;
    int j = 0, t;
    k = 0;

    while (i < n && j < m)
    {
        if (A[i] > B[j])
        {
            C[(k)++] = A[i++];
        }
        else if (A[i] < B[j])
        {
            C[(k)++] = B[j++];
        }
        else
        {
            C[(k)++] = A[i++];
            j++;
        }
    }

    for (t = i; t < n; t++)
    {
        C[(k)++] = A[t];
    }

    for (t = j; t < m; t++)
    {
        C[(k)++] = B[t];
    }

    printf("\nThe Merged Array in Descending Order\n");

    for (i = 0; i < k; i++)
    {
        printf("%d ", C[i]);
    }

    return 0;
}
