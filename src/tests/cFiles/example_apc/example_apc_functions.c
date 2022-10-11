#include <stdio.h>
#include <limits.h>
// import boolean type
#include <stdbool.h>

int linear_search_iter(int A[], int n, int x)
{
    int i;
    for (i = 0; i < n; i++)
        if (A[i] == x)
            return 1;
    return 0;
}

int linear_search_rec(int A[], int n, int x)
{
    if (n == 0)
    {
        return 0;
    }
    else if (A[0] == x)
    {
        return 1;
    }
    else
    {
        return linear_search_rec(A + 1, n - 1, x);
    }
}

int fib_iter(int n)
{
    int a = 0;
    int b = 1;
    int f;
    for (int i = 0; i < n; i++)
    {
        f = a + b;
        a = b;
        b = f;
    }
    return a;
}

int fib_rec(int n)
{
    if (n == 0)
    {
        return 0;
    }
    else if (n == 1)
    {
        return 1;
    }
    else
    {
        return fib_rec(n - 1) + fib_rec(n - 2);
    }
}

int fact_iter(int n)
{
    int f = 1;
    for (int i = 1; i <= n; i++)
    {
        f = f * i;
    }
    return f;
}

int fact_rec(int n)
{
    if (n == 0)
    {
        return 1;
    }
    else
    {
        return n * fact_rec(n - 1);
    }
}

int binary_search_iter(int A[], int n, int x)
{
    int a = 0;
    int b = n;
    while (a < b)
    {
        int m = (a + b) / 2;
        if (A[m] == x)
        {
            return 1;
        }
        if (A[m] < x)
        {
            a = m + 1;
        }
        else
        {
            b = m;
        }
    }
    return 0;
}

int binary_search_rec(int A[], int n, int x)
{
    if (n == 0)
    {
        return 0;
    }
    else if (A[n / 2] == x)
    {
        return 1;
    }
    else if (A[n / 2] < x)
    {
        return binary_search_rec(A + n / 2 + 1, n / 2, x);
    }
    else
    {
        return binary_search_rec(A, n / 2, x);
    }
}

int power_iter(int x, int n)
{
    int p = 1;
    for (int i = 0; i < n; i++)
    {
        p = p * x;
    }
    return p;
}

int power_rec(int x, int n)
{
    if (n == 0)
    {
        return 1;
    }
    else
    {
        return x * power_rec(x, n - 1);
    }
}

// recursive and iterative versions of these
// algorithms could be interesting
// -----------------------------------------
// find max value in array

int max_value_iter(int A[], int n) 
{
    int best = INT_MIN;
    for(int i = 0; i < n; i++) {
        if(best < A[i]) {
            best = A[i];
        }
    }
}

int max_value_rec(int A[], int n) 
{
    if(n==1) {
        return A[0];
    } else {
        int rec = max_value_rec(A+1, n-1);
        if(rec>A[0]) {
            return rec;
        } else {
            return A[0];
        }
    }
}
// vector product

int dot_product_iter(int A[], int B[], int n)
{
    int product = 0;
    for (int i = 0; i < n; i++) {
        product = product + A[i] * B[i];
    }
    return product;
}

// function that multiplies two vectors
int vector_product_iter(int A[], int B[], int n)
{
    int product = 0;
    for (int i = 0; i < n; i++) {
        product = product + A[i] * B[i];
    }
    return product;
}

// function that multiplies two vectors recursively
int vector_product_rec(int A[], int B[], int n)
{
    if(n==1) {
        return A[0]*B[0];
    } else {
        return A[0]*B[0] + vector_product_rec(A+1, B+1, n-1);
    }
}

// function that multiplies two 2d matrices
int* matrix_product_iter(int A[], int B[], int n)
{
    int* product = malloc(n*n*sizeof(int));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            product[i*n+j] = 0;
            for (int k = 0; k < n; k++) {
                product[i*n+j] = product[i*n+j] + A[i*n+k] * B[k*n+j];
            }
        }
    }
    return product;
}

// function that multiplies two 2d matrices recursively


// matrix multiplication
// matrix exponentiation
// matrix determinant (3x3? or nxn?)
// matrix inverse
// newton's method for root finding
// function that performs insertion sort on array
void insertionSort(int arr[], int n)
{
    int i, key, j;
    for (i = 1; i < n; i++) 
    {
        key = arr[i];
        j = i - 1;

        while (j >= 0 && arr[j] > key) 
        {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

// selection sort on array
void selection_sort(int A[], int n)
{
    for (int i = 0; i < n; i++)
    {
        int min = i;
        for (int j = i + 1; j < n; j++)
        {
            if (A[j] < A[min])
            {
                min = j;
            }
        }
        int temp = A[i];
        A[i] = A[min];
        A[min] = temp;
    }
}

// bubble sort on array
void bubble_sort(int A[], int n)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            if (A[j] > A[j + 1])
            {
                int temp = A[j];
                A[j] = A[j + 1];
                A[j + 1] = temp;
            }
        }
    }
}

// function that performs quicksort on array
void quickSort(int A[], int n)
{
    if (n <= 1)
    {
        return;
    }
    int pivot = A[n / 2];
    int left = 0;
    int right = n - 1;
    while (left <= right)
    {
        while (A[left] < pivot)
        {
            left++;
        }
        while (A[right] > pivot)
        {
            right--;
        }
        if (left <= right)
        {
            int temp = A[left];
            A[left] = A[right];
            A[right] = temp;
            left++;
            right--;
        }
    }
    quickSort(A, right + 1);
    quickSort(A + left, n - left);
}

// function that performs mergesort on array
void mergeSort(int A[], int n)
{
    if (n <= 1)
    {
        return;
    }
    int m = n / 2;
    mergeSort(A, m);
    mergeSort(A + m, n - m);
    int* temp = malloc(n * sizeof(int));
    int i = 0;
    int j = m;
    int k = 0;
    while (i < m && j < n)
    {
        if (A[i] < A[j])
        {
            temp[k] = A[i];
            i++;
        }
        else
        {
            temp[k] = A[j];
            j++;
        }
        k++;
    }
    while (i < m)
    {
        temp[k] = A[i];
        i++;
        k++;
    }
    while (j < n)
    {
        temp[k] = A[j];
        j++;
        k++;
    }
    for (int i = 0; i < n; i++)
    {
        A[i] = temp[i];
    }
    free(temp);
}

// sqrt of n via binary search


// merge sort
// quick sort
// breadth first search
// depth first search
// shortest path (bellman ford?)
// function that implements dijkstra's algorithm
void dijkstra(int graph[9][9], int src)
{
    int dist[9];
    bool sptSet[9];
    for (int i = 0; i < 9; i++)
    {
        dist[i] = INT_MAX;
        sptSet[i] = false;
    }
    dist[src] = 0;
    for (int count = 0; count < 9 - 1; count++)
    {
        int u = minDistance(dist, sptSet);
        sptSet[u] = true;
        for (int v = 0; v < 9; v++)
        {
            if (!sptSet[v] && graph[u][v] && dist[u] != INT_MAX && dist[u] + graph[u][v] < dist[v])
            {
                dist[v] = dist[u] + graph[u][v];
            }
        }
    }
    printSolution(dist, 9);
}

// spanning tree of a graph
// linear-time median algorithm
// convex hull of set of points in 2d
// simpson's adaptive algorith for numeric integration
// longest common subsequence of two arrays of integers
// edit distance between two arrays of integers
// hyper op / ackerman

int main(void)
{
    int A[] = {2, 3, 4, 10, 40, 50};
    int x = 42;
    int n = sizeof(A) / sizeof(A[0]);
    // int result_iter = linear_search_iter(A, n, x);
    // printf("%d\n", result_iter);
    // int result_rec = linear_search_rec(A, n, x);
    // printf("%d\n", result_rec);
    // int input = 4;
    // int result_fib_iter = fib_iter(input);
    // printf("%d\n", result_fib_iter);
    // int result_fib_rec = fib_rec(input);
    // printf("%d\n", result_fib_rec);
    // int result = power_rec(3, 5);
    // printf("%d\n", result);

    return 0;
}