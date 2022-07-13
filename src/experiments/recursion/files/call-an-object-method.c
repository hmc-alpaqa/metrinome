#include<stdlib.h>
#include<stdio.h>

typedef struct{
        int x;
        int (*funcPtr)(int);
}functionPair;

int factorial(int num){
        if(num==0||num==1)
                return 1;
        else
                return num*factorial(num-1);
}
