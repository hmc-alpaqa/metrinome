/*
 * C program to accept numbers as an input from user
 * and to sort them in ascending order.
 */
#include <stdio.h>

int mainn(int size)
{
    int x;
    int n = size;
    int number[size];
    srand(0);
    for (x = 0; x < size; x++) {
        number[x] = rand();
    }
    int i, count;
    count = size;


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
