#include<stdio.h>

void three_loops_bounds(int a, int b, int c){
	for(int i = 0; i < a; ++i){
		printf("%d ", i);
	}

	printf("\n");
	for(int i = 0; i < b; ++i){
		printf("%d ", i);
	}

	printf("\n");
	for(int i = 0; i < c; ++i){
		printf("%d ", i);
	}

}
