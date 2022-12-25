#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

int linear_search_iter(int A[], int n, int x)
{
    for (int i = 0; i < n; i++)
        if (A[i] == x)
            return 1;
    return 0;
}
​
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
​
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
​
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
​
int fact_iter(int n)
{
    int f = 1;
    for (int i = 1; i <= n; i++)
    {
        f = f * i;
    }
    return f;
}
​
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
​
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
​
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
​
int power_iter(int x, int n)
{
    int p = 1;
    for (int i = 0; i < n; i++)
    {
        p = p * x;
    }
    return p;
}
​
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
​
int max_value_iter(int A[], int n)
{
    int best = INT_MIN;
    for (int i = 0; i < n; i++)
    {
        if (best < A[i])
        {
            best = A[i];
        }
    }
    return best;
}
​
int max_value_rec(int A[], int n)
{
    if (n == 1)
    {
        return A[0];
    }
    else
    {
        int rec = max_value_rec(A + 1, n - 1);
        if (rec > A[0])
        {
            return rec;
        }
        else
        {
            return A[0];
        }
    }
}
// vector product
​
int dot_product_iter(int A[], int B[], int n)
{
    int product = 0;
    for (int i = 0; i < n; i++)
    {
        product = product + A[i] * B[i];
    }
    return product;
}
​
// function that multiplies two vectors
int vector_product_iter(int A[], int B[], int n)
{
    int product = 0;
    for (int i = 0; i < n; i++)
    {
        product = product + A[i] * B[i];
    }
    return product;
}
​
// function that multiplies two vectors recursively
int vector_product_rec(int A[], int B[], int n)
{
    if (n == 1)
    {
        return A[0] * B[0];
    }
    else
    {
        return A[0] * B[0] + vector_product_rec(A + 1, B + 1, n - 1);
    }
}
​
// function that multiplies two 2d matrices
int *matrix_product_iter(int A[], int B[], int n)
{
    int *product = (int *)malloc(n * n * sizeof(int));
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            product[i * n + j] = 0;
            for (int k = 0; k < n; k++)
            {
                product[i * n + j] = product[i * n + j] + A[i * n + k] * B[k * n + j];
            }
        }
    }
    return product;
}
​
// function that finds the approximation of a n-root of a number using newton's method
double newtons_method_rec(double number, int root, double guess)
{
    double epsilon = 1e-6;
    double value = 1;
    for (int i = 0; i < root - 1; i++)
    {
        value *= guess;
    }
    double new_guess = guess - (value * guess - number) / (root * value);
    if (abs(new_guess - guess) < epsilon)
    {
        return guess;
    }
    else
    {
        return newtons_method_rec(number, root, new_guess);
    }
}
​
double newtons_method_iter(double number, int root, double guess)
{
    double epsilon = 1e-6;
    while (1)
    {
        double value = 1;
        for (int i = 0; i < root - 1; i++)
        {
            value *= guess;
        }
        double new_guess = guess - (value * guess - number) / (root * value);
        if (abs(new_guess - guess) < epsilon)
        {
            return guess;
        }
        else
        {
            guess = new_guess;
        }
    }
}
​
// function that find the longest common subsequence of two strings
char* longest_common_subsequence(char *a, char *b, int a_len, int b_len)
{
    // create a dp table to store the longest common subsequence
    int dp[a_len + 1][b_len + 1];
    // initialize the dp table
    for (int i = 0; i < a_len + 1; i++)
    {
        for (int j = 0; j < b_len + 1; j++)
        {
            dp[i][j] = 0;
        }
    }
    // fill the dp table
    for (int i = 1; i < a_len + 1; i++)
    {
        for (int j = 1; j < b_len + 1; j++)
        {
            if (a[i - 1] == b[j - 1])
            {
                // if the characters are the same, add 1 to the previous value to store the length of the longest common subsequence
                dp[i][j] = dp[i - 1][j - 1] + 1;
            }
            else
            {
                // if the characters are not equal, take the max of the previous row and column
                dp[i][j] = dp[i - 1][j] > dp[i][j - 1] ? dp[i - 1][j] : dp[i][j - 1];
            }
        }
    }
    // create a string to store the longest common subsequence
    char* lcs = (char *)malloc((dp[a_len][b_len] + 1) * sizeof(char));
    // initialize the string
    for (int i = 0; i < dp[a_len][b_len] + 1; i++)
    {
        // set all characters to null
        lcs[i] = '\0';
    }
    // fill the string
    int i = a_len;
    int j = b_len;
    int k = dp[a_len][b_len];
    while (i > 0 && j > 0)
    {
        if (a[i - 1] == b[j - 1])
        {
            lcs[k - 1] = a[i - 1];
            i--;
            j--;
            k--;
        }
        else if (dp[i - 1][j] > dp[i][j - 1])
        {
            i--;
        }
        else
        {
            j--;
        }
    }
    return lcs;
}
​
// function that finds the longest common substring of two strings
char* longest_common_substring(char *a, char *b, int a_len, int b_len)
{
    int dp[a_len + 1][b_len + 1];
    // initialize the dp table
    for (int i = 0; i < a_len + 1; i++)
    {
        for (int j = 0; j < b_len + 1; j++)
        {
            dp[i][j] = 0;
        }
    }
    // fill the dp table
    int max = 0;
    int max_i = 0;
    int max_j = 0;
    for (int i = 1; i < a_len + 1; i++)
    {
        for (int j = 1; j < b_len + 1; j++)
        {
            if (a[i - 1] == b[j - 1])
            {
                // if the characters are the same, add 1 to the previous value to store the length of the longest common substring
                dp[i][j] = dp[i - 1][j - 1] + 1;
                if (dp[i][j] > max)
                {
                    max = dp[i][j];
                    max_i = i;
                    max_j = j;
                }
            }
            else
            {
                // if the characters are not equal, set the value to 0
                dp[i][j] = 0;
            }
        }
    }
    // create a string to store the longest common substring
    char *lcs = (char *)malloc((max + 1) * sizeof(char));
    // initialize the string
    for (int i = 0; i < max + 1; i++)
    {
        // set all characters to null
        lcs[i] = '\0';
    }
    // fill the string
    int i = max_i;
    int j = max_j;
    int k = max;
    while (i > 0 && j > 0)
    {
        if (a[i - 1] == b[j - 1])
        {
            lcs[k - 1] = a[i - 1];
            i--;
            j--;
            k--;
        }
        else
        {
            break;
        }
    }
    return lcs;
}
​
void insertionSort(int arr[], int n)
{
    int i, key, j;
    for (i = 1; i < n; i++)
    {
        key = arr[i];
        j = i - 1;
​
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}
​
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
​
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
​
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
​
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
    int *temp = (int *)malloc(n * sizeof(int));
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
​
// function that implements ackermann's function
int ackermann_rec(int m, int n)
{
    if (m == 0)
    {
        return n + 1;
    }
    else if (n == 0)
    {
        return ackermann_rec(m - 1, 1);
    }
    else
    {
        return ackermann_rec(m - 1, ackermann_rec(m, n - 1));
    }
}
​
// function that counts down in O(n^2) time
int minmaxsum_iter(int A[])
{
    int max = INT_MIN;
    int min = INT_MAX;
    int n = sizeof(A) / sizeof(A[0]);
    for (int i = 0; i < n; i++)
    {
        if (A[i] > max)
        {
            max = A[i];
        }
    }
    for (int i = 0; i < n; i++)
    {
        if (A[i] < min)
        {
            min = A[i];
        }
    }
    return min + max;
}
​
// recursive function with O(n^2) path complexity
int polypath_rec(int n)
{
    if (n < 0) {
        while(n < 0) {
            n++;
        }
        return n;
    } else {
        if (n%100 == 0) {
            return n;
        } else {
            return polypath_rec(n+1);
        }
    }
}


int polypath_rec1(int n, int k)
{
  if (n > 0)
  {
    return 1 + polypath_rec1(n - 1, k);
  } else {
    int count = 0;
    while(k > 0) {
      count++;
      k--;
    }
    return count;
  }
}

int polypath_rec2(int n)
{
    if (n < 0) {
        while(n < 0) {
            n++;
        }
        return n;
    } else {
        if (n%100 == 0) {
            return n;
        } else {
            return polypath_rec2(n+1);
        }
    }
}


// int main(void)
// {
//     for(int i = 0; i < 10; i++)
//     {
//         printf("%d ", triangle_rec(i));
//         printf("%d ", triangle_iter(i));
//         printf("\n");
//     }
//     // printf("%d ", triangle_rec(4));
//     // printf("%d ", test);
// ​
//     return 0;
// }
