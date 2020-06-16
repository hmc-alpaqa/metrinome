#include<stdio.h>
#include "51_variance.c"

#define MAXSIZE 10

int main(){

	double data[MAXSIZE] = {1, 2, 5, 6, 10, 2, 4, 5, 1, 15};
	double v = variance(data, MAXSIZE);
	printf("%f\n", v);

}