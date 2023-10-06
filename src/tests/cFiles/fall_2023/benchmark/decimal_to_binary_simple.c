#include <stdio.h>

// Convert decimal number into binary
long decimalToBinary(int decimal) {
    long binary = 0;
    int base = 1;

    while (decimal > 0) {
        int remainder = decimal % 2;
        decimal = decimal / 2;
        binary += remainder * base;
        base *= 10;
    }

    return binary;
}

// int main() {
//     int decimalNumber;

//     printf("Enter a decimal number: ");
//     scanf("%d", &decimalNumber);

//     long binaryNumber = decimalToBinary(decimalNumber);

//     printf("Binary equivalent: %ld\n", binaryNumber);

//     return 0;
// }