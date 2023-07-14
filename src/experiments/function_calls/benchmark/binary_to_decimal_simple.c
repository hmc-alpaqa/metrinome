#include <stdio.h>

// Convert binary number into decimal 
int binaryToDecimal(int binary) {
    int decimal = 0, base = 1;

    while (binary > 0) {
        int lastDigit = binary % 10;
        binary = binary / 10;
        decimal += lastDigit * base;
        base *= 2;
    }

    return decimal;
}

// int main() {
//     int binaryNumber;

//     printf("Enter a binary number: ");
//     scanf("%d", &binaryNumber);

//     int decimalNumber = binaryToDecimal(binaryNumber);

//     printf("Decimal equivalent: %d\n", decimalNumber);

//     return 0;
// }