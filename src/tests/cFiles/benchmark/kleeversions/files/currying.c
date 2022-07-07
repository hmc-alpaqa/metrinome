#include<stdarg.h>
#include<stdio.h>

long int factorial(int n){
	if(n>1)
		return n*factorial(n-1);
	return 1;
}

long int sumOfFactorials(int num,...){
	va_list vaList;
	long int sum = 0;

	va_start(vaList,num);

	while(num--)
		sum += factorial(va_arg(vaList,int));

	va_end(vaList);

	return sum;
}
