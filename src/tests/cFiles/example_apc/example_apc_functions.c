#include <stdio.h> 
  
int linear_search_iter(int A[], int n, int x) 
{ 
    int i; 
    for (i = 0; i < n; i++) 
        if (A[i] == x) 
            return 1; 
    return 0; 
}
​
int linear_search_rec(int A[], int n, int x) 
{ 
    if(n == 0){
        return 0;
    }
    else if(A[0] == x){
        return 1;
    }
    else{
        return linear_search_rec(A + 1, n - 1, x);
    }
} 
​
int fib_iter(int n){
    int a = 0;
    int b = 1;
    int f;
    for(int i = 0; i < n; i++){
        f = a + b;
        a = b;
        b = f;
    }
    return a;
}
​
int fib_rec(int n){
    if(n == 0){
        return 0;
    }
    else if(n == 1){
        return 1;
    }
    else{
        return fib_rec(n-1) + fib_rec(n-2);
    }
}
​
int fact_iter(int n){
    int f = 1;
    for(int i = 1; i <= n; i++){
        f = f * i;
    }
    return f;
}
​
int fact_rec(int n){
    if(n == 0){
        return 1;
    }
    else{
        return n * fact_rec(n-1);
    }
}
​
int binary_search_iter(int A[], int n, int x){
    int a = 0;
    int b = n;
    while(a < b){
        int m = (a + b) / 2;
        if(A[m] == x){
            return 1;
        }
        if(A[m] < x){
            a = m + 1;
        }
        else{
            b = m;
        }
    }
    return 0;
}
​
int binary_search_rec(int A[], int n, int x){
    if(n == 0){
        return 0;
    }
    else if(A[n/2] == x){
        return 1;
    }
    else if(A[n/2] < x){
        return binary_search_rec(A + n/2 + 1, n/2, x);
    }
    else{
        return binary_search_rec(A, n/2, x);
    }
}
​
int power_iter(int x, int n){
    int p = 1;
    for(int i = 0; i < n; i ++){
        p = p * x;
    }
    return p;
}
​
int power_rec(int x, int n){
    if(n == 0){
        return 1;
    }
    else{
        return x * power_rec(x, n-1);
    }
}
​
// recursive and iterative versions of these
// algorithms could be interesting
// -----------------------------------------
// find max value in array
// find a specific value in an array
// vector product
// matrix multiplication
// matrix exponentiation
// matrix determinant (3x3? or nxn?)
// matrix inverse
// gaussian elimination
// newton's method for root finding
// insertion sort
// selection sort
// sqrt of n via binary search
// merge sort
// quick sort 
// breadth first search
// depth first search
// shortest path (bellman ford?)
// dijkstra's algorithm
// spanning tree of a graph
// linear-time median algorithm
// convex hull of set of points in 2d
// simpson's adaptive algorith for numeric integration
// longest common subsequence of two arrays of integers
// edit distance between two arrays of integers
// hyper op / ackerman 
​
int main(void) 
{ 
    int A[] = { 2, 3, 4, 10, 40, 50 }; 
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
    int result = power_rec(3,5); 
    printf("%d\n", result);
    
    return 0; 
}