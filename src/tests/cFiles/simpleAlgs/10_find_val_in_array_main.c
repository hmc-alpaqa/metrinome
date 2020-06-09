# include "10_find_val_in_array.c"

int main(){
    const int n = 10;
    int i;
    int a[n] = {1,2,3,4,5,4,3,2,1,0};
     
    i = find_first(3, a, n);
    printf("%d\n", i);

    i = find_first(19, a, n);
    printf("%d\n", i);
}
