#include <stdio.h>

void ssort(int Arr[], int s)
{
    int i, j, temp, small;
    for (i = 0; i < s - 1; i++)
    {
        small = i;
        for (j = i + 1; j < s; j++)
        {
            if (Arr[j] < Arr[small])
            {
                small = j;
            }
            if (small != i)
            {
                temp = Arr[i];
                Arr[i] = Arr[small];
                Arr[small] = temp;
            }
        }
    }
}
