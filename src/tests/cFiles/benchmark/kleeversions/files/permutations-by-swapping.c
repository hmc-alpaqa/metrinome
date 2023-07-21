#include<stdlib.h>
#include<string.h>
#include<stdio.h>

int flag = 1;

void heapPermute(int n, int arr[],int arrLen){
	int temp;
	int i;

	if(n==1){
		printf("\n[");

		for(i=0;i<arrLen;i++)
			printf("%d,",arr[i]);
		printf("\b] Sign : %d",flag);

		flag*=-1;
	}
	else{
		for(i=0;i<n-1;i++){
			heapPermute(n-1,arr,arrLen);

			if(n%2==0){
				temp = arr[i];
				arr[i] = arr[n-1];
				arr[n-1] = temp;
			}
			else{
				temp = arr[0];
				arr[0] = arr[n-1];
				arr[n-1] = temp;
			}
		}
		heapPermute(n-1,arr,arrLen);
	}
}
