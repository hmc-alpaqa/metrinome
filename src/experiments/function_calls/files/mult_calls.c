#include <stdbool.h>

bool givetrue(int a);


bool partition(int arr[], int low, int high, bool iF) {

    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (iF) {
            i++;
            // return givetrue(high);
            givetrue(high);
        }
    }
    givetrue(high);
    return true;
}


bool givetrue(int a) {
    return true;
}

// int gcd(int a, int b)
// {
//     while (a != b)
//     {
//         if (a > b)
//         {
//             a = a - b;
//         }
//         else
//         {
//             b = b - a;
//         }
//     }
//     return a;
// }