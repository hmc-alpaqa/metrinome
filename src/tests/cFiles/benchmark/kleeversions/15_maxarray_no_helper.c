#include <stdio.h>


int mainn(int arr[], int size)
{
    // int arr[] = {1, 24, 145, 20, 8, -101, 300};
    // int n = sizeof(arr)/sizeof(arr[0]);
    int x;
    int n = size;
    // int arr[size];
    // srand(0);
    // for (x = 0; x < size; x++) {
    //     arr[x] = rand();
    // }
    int i, max_element;

    // Initialization to the first array element
    max_element = arr[0];

    /* Here we are comparing max_element with
     * all other elements of array to store the
     * largest element in the max_element variable
     */
    for (i = 1; i < n; i++)
        if (arr[i] > max_element)
            max_element = arr[i];

    // printf("Largest element of array is %d", max_element);
    return 0;
}
