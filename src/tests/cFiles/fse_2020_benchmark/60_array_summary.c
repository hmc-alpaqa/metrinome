#include <stdio.h>

__attribute__((always_inline)) inline void array_summary (int arr[], int num, int results[]) {
    int i, max_element;

    max_element = arr[0];
    for (i = 1; i < num; i++)
        if (arr[i] > max_element) max_element = arr[i];

    int j, min_element;
    min_element = arr[0];
    for (j = 1; j < num; j++)
        if (arr[j] < min_element) min_element = arr[j];

    int k, sum;
    sum = 0;
    for (k = 1; k < num; k++)
        sum += arr[k];
    int out[3] = {max_element, min_element, sum/num};
    results = out;
}
