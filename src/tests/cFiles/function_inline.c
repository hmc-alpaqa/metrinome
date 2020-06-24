// https://www.geeksforgeeks.org/inline-function-in-c/
#include <stdio.h> 

// another inline function
__attribute__((always_inline)) static inline int foo2(int x) 
{ 
    if (x > 5){
        x = 6;
        //printf("x is greater than 5"); 
    } else {
        x = 4;
        //printf("x is not greater than 5"); 
    }
} 
 
// Inline function in C 
__attribute__((always_inline)) static inline int foo(int x) 
{ 
    //while (x < 15){
    x = foo2(x);
    ++x;
        //++x;
    //}

    if (x < 0) {
        return -1;
    } else {
        return 1;
    }
}  
  
// Driver code 
int main() 
{ 
    int ret = 10; 
  
    // inline function call 
    ret = foo(ret); 
  
    printf("Output is: %d\n", ret); 
    return 0; 
}
