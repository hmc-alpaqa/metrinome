#include<stdio.h>

int is_sorted(int* array, int size){
    for(int i = 0; i < size - 1; ++i){
        if(array[i] > array[i + 1]){
            return 0;
        }
    }
    return 1;
}

int main(){
    const int n = 10;
    int s;
    int a[n] = {1,2,4,4,5,7,10,10,19,23};
     
    s = is_sorted(a, n);
    printf("%d\n", s);
}