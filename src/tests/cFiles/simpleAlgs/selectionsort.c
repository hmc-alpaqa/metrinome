#include<stdio.h>
void selectionsort(int count, int number[]){
  int i, j, temp;
  // Logic of selection sort algorithm
  for(i=0;i<count;i++){
     for(j=i+1;j<count;j++){
        if(number[i]>number[j]){
           temp=number[i];
           number[i]=number[j];
           number[j]=temp;
        }
     }
  }

  printf("Sorted elements: ");
  for(i=0;i<count;i++)
     printf(" %d",number[i]);
}
int main(){
   /* Here i & j for loop counters, temp for swapping,
    * count for total number of elements, number[] to
    * store the input numbers in array. You can increase
    * or decrease the size of number array as per requirement
    */
   int i, count, number[25];

   printf("How many numbers u are going to enter?: ");
   scanf("%d",&count);

   printf("Enter %d elements: ", count);
   // Loop to get the elements stored in array
   for(i=0;i<count;i++)
      scanf("%d",&number[i]);


  selectionsort(count, number);
  return 0;
}
