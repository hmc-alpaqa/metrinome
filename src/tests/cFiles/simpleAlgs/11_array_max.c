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

