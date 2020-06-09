#include<stdio.h>

int compare_arrays(int* x, int* y, int size){
    for(int i = 0; i < size; ++i){
        if(x[i] < y[i]){
            return -1;
        }
        else if(x [i] > y[i]){
            return 1;
        }
    }
    return 0;
}

int main(){
    const int n = 10;
    int compare;
    int a[n] = {1,2,3,4,5,4,3,2,1,0};
    int b[n] = {1,2,3,4,5,4,3,2,1,0};
    int c[n] = {1,2,7,4,5,4,3,2,1,0};

    compare = compare_arrays(a, c, n);
    printf("%d\n", compare);

    compare = compare_arrays(a, b, n);
    printf("%d\n", compare);

    compare = compare_arrays(c, b, n);
    printf("%d\n", compare);
}