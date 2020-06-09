#include<stdio.h>
int insertion_sort(int list[], int count){
  int i, j, temp;
  for(i = 1; i < count; i++){
     temp = list[i];
     j = i - 1;
     while( temp < list[j] && j >= 0){
        list[j + 1] = list[j];
        j = j - 1;
     }
     list[j + 1] = temp;
  }

  return 0;
}

int main(){
  int n = 10;
  int array[10] = {5,3,2,1,4,8,7,9,6,10};

  insertion_sort(array, n);

  for (int i = 0; i < n; i++)
     printf("%d\n", array[i]);

  return 0;
}
