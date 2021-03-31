#include <stdio.h>

__attribute__((always_inline)) inline void accept(int Arr[], int s);
__attribute__((always_inline)) inline void display(int Arr[], int s);
__attribute__((always_inline)) inline void ssort(int Arr[], int s);

int main()
{
    int list[100], n;
    printf("Enter size of Array : ");
    scanf("%d", &n);
    accept(list, n);
    printf("\nBefore sorting");
    display(list, n);
    ssort(list, n);
    printf("\nAfter sorting");
    display(list, n);

    return 0;
}

__attribute__((always_inline)) inline void accept(int Arr[], int s)
{
    int i;
    for (i = 0; i < s; i++)
    {
        printf("Enter element %d : ", i + 1);
        scanf("%d", &Arr[i]);
    }
}

__attribute__((always_inline)) inline void display(int Arr[], int s)
{
    int i;
    printf("\n");
    for (i = 0; i < s; i++)
    {
        printf("%d ", Arr[i]);
    }
}

__attribute__((always_inline)) inline void ssort(int Arr[], int s)
{
    int i, j, temp, small;
    for (i = 0; i < s - 1; i++)
    {
        small = i;
        for (j = i + 1; j < s; j++)
        {
            if (Arr[j] < Arr[small])
            {
                small = j;
            }
            if (small != i)
            {
                temp = Arr[i];
                Arr[i] = Arr[small];
                Arr[small] = temp;
            }
        }
    }
}
