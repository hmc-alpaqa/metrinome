#include <stdio.h>

int binary_search(int search, int array[], int n){
    int first = 0;
    int last = n - 1;
    int middle = (first+last)/2;

     while (first <= last) {
        if (array[middle] < search)
          first = middle + 1;
        else if (array[middle] > search)
          last = middle - 1;
        else if (array[middle] == search) 
          return middle;
        middle = (first + last)/2;
  }
  return -1;
}

int main()
{
  const int n = 10; //number of elements
  int val = 13; 
  int array[10] = {2, 4, 8, 10, 12, 15, 19, 20, 22, 30};

  int location = binary_search(val, array, n);
  
  printf("%d\n", location);
  return 0;
}
