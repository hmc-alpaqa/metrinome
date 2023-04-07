#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// bool is_even(int n);
// bool is_odd(int n);
int max_value_iter(int arr[], int n);
void merge(int arr[], int l, int m, int r);
int fact(int n);
void fcn_medley(int n);
int fact_wrapper(int n);
int fib_iter(int n);
int fib_rec(int n);

// int fact(int n)
// {
//     if (n == 0)
//     {
//         return 1;
//     }
//     else
//     {
//         return n * fact(n - 1);
//     }
// }

// void fcn_medley(int n)
// {
//     fact(n);
//     fib_iter(n);
//     fib_rec(n);
//     fact_wrapper(n);
// }

// int fact_wrapper(int n)
// {
//     return fact(n);
// }

// int fact_wrapper_2x(int n)
// {
//     return fact(n) + fact(n);
// }

// int fib_iter(int n)
// {
//     int a = 0;
//     int b = 1;
//     int f;
//     for (int i = 0; i < n; i++)
//     {
//         f = a + b;
//         a = b;
//         b = f;
//     }
//     return a;
// }

int fib_rec(int n)
{
    if (n > 2)
    {
        return n;
    }
    else
    {
        return fib_rec(n - 1) + fib_rec(n - 2);
    }
}

void mergeSortSimple(int arr[], int l, int r)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;

        // sort first and second halves
        mergeSortSimple(arr, l, m);
        mergeSortSimple(arr, m + 1, r);

        // merge the sorted halves
        // merge(arr, l, m, r);
        // fact(m);
        // max_value_iter(arr, m);
        fib_rec(m);
    }
}

// int fact_wrapper_3x(int n)
// {
//     return fact(n) + fact(n) + fact(n);
// }

// int gcd(int a, int b)
// {
//     while (a != b)
//     {
//         if (a > b)
//         {
//             a = a - b;
//         }
//         else
//         {
//             b = b - a;
//         }
//     }
//     return a;
// }

// int gcd_wrapper(int a, int b)
// {
//     return gcd(a, b);
// }

// void merge(int arr[], int l, int m, int r)
// {
//     int i, j, k;
//     int n1 = m - l + 1;
//     int n2 = r - m;

//     // create temporary arrays
//     int L[n1], R[n2];

//     // copy data to temp arrays L[] and R[]
//     for (i = 0; i < n1; i++)
//         L[i] = arr[l + i];
//     for (j = 0; j < n2; j++)
//         R[j] = arr[m + 1 + j];

//     // merge the temp arrays back into arr[l..r]
//     i = 0;
//     j = 0;
//     k = l;
//     while (i < n1 && j < n2)
//     {
//         if (L[i] <= R[j])
//         {
//             arr[k] = L[i];
//             i++;
//         }
//         else
//         {
//             arr[k] = R[j];
//             j++;
//         }
//         k++;
//     }

//     // copy the remaining elements of L[], if there are any
//     while (i < n1)
//     {
//         arr[k] = L[i];
//         i++;
//         k++;
//     }

//     // copy the remaining elements of R[], if there are any
//     while (j < n2)
//     {
//         arr[k] = R[j];
//         j++;
//         k++;
//     }
// }

// void mergeSort(int arr[], int l, int r)
// {
//     if (l < r)
//     {
//         int m = l + (r - l) / 2;

//         // sort first and second halves
//         mergeSort(arr, l, m);
//         mergeSort(arr, m + 1, r);

//         // merge the sorted halves
//         merge(arr, l, m, r);
//     }
// }

// void mergeSortSingleFcn(int A[], int n)
// {
//     if (n <= 1)
//     {
//         return;
//     }
//     int m = n / 2;
//     mergeSortSingleFcn(A, m);
//     mergeSortSingleFcn(A + m, n - m);
//     int *temp = (int *)malloc(n * sizeof(int));
//     int i = 0;
//     int j = m;
//     int k = 0;
//     while (i < m && j < n)
//     {
//         if (A[i] < A[j])
//         {
//             temp[k] = A[i];
//             i++;
//         }
//         else
//         {
//             temp[k] = A[j];
//             j++;
//         }
//         k++;
//     }
//     while (i < m)
//     {
//         temp[k] = A[i];
//         i++;
//         k++;
//     }
//     while (j < n)
//     {
//         temp[k] = A[j];
//         j++;
//         k++;
//     }
//     for (int i = 0; i < n; i++)
//     {
//         A[i] = temp[i];
//     }
//     free(temp);

//     return;
// }

// void swap(int *a, int *b)
// {
//     int temp = *a;
//     *a = *b;
//     *b = temp;
// }

// int partition(int arr[], int low, int high)
// {
//     int pivot = arr[high];
//     int i = (low - 1);

//     for (int j = low; j <= high - 1; j++)
//     {
//         if (arr[j] < pivot)
//         {
//             i++;
//             swap(&arr[i], &arr[j]);
//         }
//     }
//     swap(&arr[i + 1], &arr[high]);
//     return (i + 1);
// }

// void quickSort(int arr[], int low, int high)
// {
//     if (low < high)
//     {
//         int pi = partition(arr, low, high);
//         quickSort(arr, low, pi - 1);
//         quickSort(arr, pi + 1, high);
//     }
// }

// // calls fact_wrapper -> calls fact
// int sum_factorials(int n)
// {
//     int sum = 0;
//     for (int i = 1; i <= n; i++)
//     {
//         sum += fact_wrapper(i);
//     }
//     return sum;
// }

// bool is_even(int n)
// {
//     if (n == 0)
//     {
//         return true;
//     }
//     else
//     {
//         return is_odd(n - 1);
//     }
// }

// bool is_odd(int n)
// {
//     if (n == 0)
//     {
//         return false;
//     }
//     else
//     {
//         return is_even(n - 1);
//     }
// }

// int max_value_iter(int A[], int n)
// {
//     int best = INT_MIN;
//     for (int i = 0; i < n; i++)
//     {
//         if (best < A[i])
//         {
//             best = A[i];
//         }
//     }
//     return best;
// }

// int max_value_rec(int A[], int n)
// {
//     if (n == 1)
//     {
//         return A[0];
//     }
//     else
//     {
//         int rec = max_value_rec(A + 1, n - 1);
//         if (rec > A[0])
//         {
//             return rec;
//         }
//         else
//         {
//             return A[0];
//         }
//     }
// }

// void heapify(int arr[], int n, int i)
// {
//     int largest = i;
//     int left = 2 * i + 1;
//     int right = 2 * i + 2;

//     if (left < n && arr[left] > arr[largest])
//     {
//         largest = left;
//     }

//     if (right < n && arr[right] > arr[largest])
//     {
//         largest = right;
//     }

//     if (largest != i)
//     {
//         int temp = arr[i];
//         arr[i] = arr[largest];
//         arr[largest] = temp;

//         heapify(arr, n, largest);
//     }
// }

// void heapSort(int arr[], int n)
// {
//     for (int i = n / 2 - 1; i >= 0; i--)
//     {
//         heapify(arr, n, i);
//     }

//     for (int i = n - 1; i >= 0; i--)
//     {
//         int temp = arr[0];
//         arr[0] = arr[i];
//         arr[i] = temp;

//         heapify(arr, i, 0);
//     }
// }

// int main()
// {
//     int arr[] = {12, 11, 13, 5, 6, 7};
//     int n = sizeof(arr) / sizeof(arr[0]);

//     heapSort(arr, n);

//     printf("Sorted array is \n");
//     for (int i = 0; i < n; i++)
//         printf("%d ", arr[i]);
//     printf("\n");
//     return 0;
// }
