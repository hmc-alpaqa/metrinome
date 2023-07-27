// sorts a list of numbers
// apc case 2
// from recursion/files/sorting-algorithms-quicksort-2.c


#include <stdlib.h>     // REQ: rand()

void swap(int *a, int *b) {
  int c = *a;
  *a = *b;
  *b = c;
}

int partition(int A[], int p, int q) {
  swap(&A[p + (rand() % (q - p + 1))], &A[q]);   // PIVOT = A[q]

  int i = p - 1;
  for(int j = p; j <= q; j++) {
    if(A[j] <= A[q]) {
      swap(&A[++i], &A[j]);
    }
  }

  return i;
}