#include<stdio.h>


int greatestof3(int x, int y, int z){

   if((x > y) && (x > z))
      return x; 
   else if((y > z) && (y > x))
      return y;
   else
      return z;
}

