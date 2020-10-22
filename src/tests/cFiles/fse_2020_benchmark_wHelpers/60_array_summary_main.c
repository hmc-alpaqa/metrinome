#include<stdio.h>
#include "60_array_summary_wHelper.c"

#define MAXSIZE 10

int main(){
    int results[3] = {0, 0, 0};
	int data[MAXSIZE] = {7, 2, 1, 9, 12, 15, 8, 38, 32, 30};
	array_summary(data, MAXSIZE, results);
	printf( results[0], results[1], results[2]);

}
