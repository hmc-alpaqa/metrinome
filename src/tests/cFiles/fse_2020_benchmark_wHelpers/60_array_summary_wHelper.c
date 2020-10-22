#include <stdio.h>

int findMaxElem(int arr[], int num);
int findMinElem(int arr[], int num);
int findSum(int arr[], int num);

void array_summary (int arr[], int num, int results[]) {
    int max_element = findMaxElem(arr, num);
    int min_element = findMinElem(arr, num);
    int sum = findSum(arr, num);

    int out[3] = {max_element, min_element, sum/num};
    results = out;
}

int findMaxElem(int arr[], int num){
    int max_element = arr[0];
    for (int i = 1; i < num; i++)
        if (arr[i] > max_element) max_element = arr[i];
    return max_element;
}

int findMinElem(int arr[], int num){
    int j, min_element;
    min_element = arr[0];
    for (j = 1; j < num; j++)
        if (arr[j] < min_element) min_element = arr[j];
    return min_element;
}

int findSum(int arr[], int num){
    int k, sum;
    sum = 0;
    for (k = 1; k < num; k++)
        sum += arr[k];
    return sum;
}