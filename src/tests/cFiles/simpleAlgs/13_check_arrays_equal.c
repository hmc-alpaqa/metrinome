#include<stdio.h>


int equal_arrays(int* x, int* y, int size){
    for(int i = 0; i < size; ++i){
        if(x[i] != y[i]){
            return 0;
        }
    }
    return 1;
}

int main(){
    const int n = 10;
    int same;
    int a[n] = {1,2,3,4,5,4,3,2,1,0};
    int b[n] = {1,2,3,4,5,4,3,2,1,0};
    int c[n] = {1,2,7,4,5,4,3,2,1,0};
     
    same = equal_arrays(a, b, n);
    printf("%d\n", same);

    same = equal_arrays(a, c, n);
    printf("%d\n", same);
}