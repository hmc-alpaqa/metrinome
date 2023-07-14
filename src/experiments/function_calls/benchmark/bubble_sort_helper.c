// Copied from src/tests/cFiles/benchmark/07_bubble_sort_helper.c
// Bubble sort - function to function version

#include <stdio.h>

void accept(int Arr[], int s);
void display(int Arr[], int s);
void bsort(int Arr[], int s);

int main()
{
    int list[100], n;
    printf("Enter Size of Array : ");
    scanf("%d", &n);
    accept(list, n);
    printf("\nBefore sorting");
    display(list, n);
    bsort(list, n);
    printf("\nAfter sorting");
    display(list, n);

    return 0;
}

void accept(int Arr[], int s)
{
    int i;
    for (i = 0; i < s; i++)
    {
        printf("Enter element %d : ", i + 1);
        scanf("%d", &Arr[i]);
    }
}

void display(int Arr[], int s)
{
    int i;
    printf("\n");
    for (i = 0; i < s; i++)
    {
        printf("%d ", Arr[i]);
    }
}

void bsort(int Arr[], int s)
{
    int i, j, temp;
    for (i = 0; i < s - 1; i++)
    {
        for (j = 0; j < (s - 1 - i); j++)
        {
            if (Arr[j] > Arr[j + 1])
            {
                temp = Arr[j];
                Arr[j] = Arr[j + 1];
                Arr[j + 1] = temp;
            }
        }
    }
}
