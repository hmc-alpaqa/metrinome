#include "11_array_max.c"

int main()
{
    int arr[] = {1, 2401, 145, 20, 8, -101, 300};
    int n = sizeof(arr)/sizeof(arr[0]);
    printf("%d\n", largest_element(arr, n));
    return 0;
}
