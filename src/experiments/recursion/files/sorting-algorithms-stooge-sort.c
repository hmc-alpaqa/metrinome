#include <stdio.h>

#define SWAP(r,s)  do{ t=r; r=s; s=t; } while(0)

void StoogeSort(int a[], int i, int j)
{
   int t;

   if (a[j] < a[i]) SWAP(a[i], a[j]);
   if (j - i > 1)
   {
       t = (j - i + 1) / 3;
       StoogeSort(a, i, j - t);
       StoogeSort(a, i + t, j);
       StoogeSort(a, i, j - t);
   }
}
