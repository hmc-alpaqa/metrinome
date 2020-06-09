#include <stdio.h>

int largest_element(int arr[], int num)
{
    int i, max_element;
    max_element = arr[0];
    for (i = 1; i < num; i++)
        if (arr[i] > max_element)
            max_element = arr[i];
    return max_element;
}

int main()
{
    int arr[] = {1, 2401, 145, 20, 8, -101, 300};
    int n = sizeof(arr)/sizeof(arr[0]);
    printf("%d\n", largest_element(arr, n));
    return 0;
}
