/*
 * C program to accept numbers as an input from user
 * and to sort them in ascending order.
 */
#include <stdio.h>

int main()
{
    int i, count, number[20];
 
    printf("How many numbers you are gonna enter:");
    scanf("%d", &count);
    printf("\nEnter the numbers one by one:");
   
    for (i = 0; i < count; ++i){
        scanf("%d", &number[i]);
    }
 
    int temp, j, k;
    for (j = 0; j < count; ++j)
    {
       for (k = j + 1; k < count; ++k)
       {
         if (number[j] > number[k])
         {
            temp = number[j];
            number[j] = number[k];
            number[k] = temp;
         }
      }
    }
    printf("Numbers in ascending order:\n");
    for (i = 0; i < count; ++i){
       printf("%d\n", number[i]);
    }

    return 0;
}
