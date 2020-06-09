#include <stdio.h>
void binarysort(int first, int middle, int last, int n, int array[], int search);

int main()
{
  int first;
  int last;
  int middle;
  int n; //number of elements
  int search; 
  int array[10];

//   printf("Enter number of elements\n");
//   scanf("%d", &n);

//   printf("Enter %d integers\n", n);

//   for (c = 0; c < n; c++)
//     scanf("%d", &array[c]);

//   printf("Enter value to find\n");
//   scanf("%d", &search);
  binarysort(first, middle, last, n, array, search);
  
  if (first > last)
    printf("Not found! %d isn't present in the list.\n", search);

  return 0;
}

void binarysort(int first, int middle, int last, int n, int array[], int search) {
    first = 0;
    last = n - 1;
    middle = (first+last)/2;

     while (first <= last) {
        if (array[middle] < search)
            first = middle + 1;
        else if (array[middle] == search) {
         printf("%d found at location %d.\n", search, middle+1);
        break;
        }
        else
            last = middle - 1;

        middle = (first + last)/2;
  }
}