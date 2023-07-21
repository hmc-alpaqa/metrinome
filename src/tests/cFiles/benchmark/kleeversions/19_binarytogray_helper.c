/*  
 * C Program to Convert Binary Code of a Number into its Equivalent 
 * Gray's Code without using Recursion
 */
#include <stdio.h>
#include <math.h>
 
int bintogray(int);
 
int main ()
{
    int bin, gray;
 
    printf("Enter a binary number: ");
    scanf("%d", &bin);
    gray = bintogray(bin);
    printf("The gray code of %d is %d\n", bin, gray);
    return 0;
}
 
int bintogray(int bin)
{
    int a, b, result = 0, i = 0;
 
    while (bin != 0)
    {
        a = bin % 10;
        bin = bin / 10;
        b = bin % 10;
        if ((a && !b) || (!a && b))
        {
            result = result + pow(10, i);
        }
        i++;
    }
    return result;
}
