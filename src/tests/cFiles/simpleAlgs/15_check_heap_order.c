#include <stdio.h>

int is_heap_order(int a[], int n){
    for(int i = 0; i < (n - 2) / 2; ++i){
        if(a[i] >= a[2*i + 1] || a[i] >= a[2*i + 2] ){
            return 0;
        }
    }
    return 1;
}

int main(){
    const int n = 10;
    int a[10] = {4,10,7,41,52,10,13,43,45,60};
    int h = is_heap_order(a, n);
    printf("%d\n", h);
    return 0;
}