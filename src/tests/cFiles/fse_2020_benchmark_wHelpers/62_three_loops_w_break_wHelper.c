#include<stdio.h>

void firstLoop(int n, int a);
void secondLoop(int n, int b);
void thirdLoop(int n, int c);

void three_loops(int n, int a, int b, int c){
	firstLoop(n, a);

	printf("\n");
	secondLoop(n, b);

	printf("\n");
	thirdLoop(n, c);

}

void firstLoop(int n, int a){
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > a){
			break;
		}
	}
}

void secondLoop(int n, int b){
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > b){
			break;
		}
	}
}

void thirdLoop(int n, int c){
	for(int i = 0; i < n; ++i){
		printf("%d ", i);
		if(i > c){
			break;
		}
	}
}