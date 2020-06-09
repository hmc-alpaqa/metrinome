#include<stdio.h>

void selection_sort(int list[], int count){
  int i, j, temp;
  for(i = 0; i < count; i++){
     for(j = i + 1; j < count; j++){
        if(list[i]>list[j]){
           temp=list[i];
           list[i]=list[j];
           list[j]=temp;
        }
     }
  }

}

int main(){
  int n = 10;
  int array[10] = {5,3,2,1,4,8,7,9,6,10};

  selection_sort(array, n);

  printf("Sorted list in ascending order:\n");

  for (int i = 0; i < n; i++)
     printf("%d\n", array[i]);

  return 0;
}
