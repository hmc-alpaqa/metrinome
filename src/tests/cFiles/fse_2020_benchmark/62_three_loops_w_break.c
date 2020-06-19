#include<stdio.h>

void three_loops(int n, int a, int b, int c){
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > a){
			break;
		}
	}

	printf("\n");
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > b){
			break;
		}
	}

	printf("\n");
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > c){
			break;
		}
	}

}