#include "22_selectionsort.c"

int main(){
  int n = 10;
  int array[10] = {5,3,2,1,4,8,7,9,6,10};

  selection_sort(array, n);

  printf("Sorted list in ascending order:\n");

  for (int i = 0; i < n; i++)
     printf("%d\n", array[i]);

  return 0;
}
