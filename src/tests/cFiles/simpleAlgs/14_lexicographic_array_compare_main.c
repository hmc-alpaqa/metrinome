#include "14_lexicographic_array_compare.c"

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
