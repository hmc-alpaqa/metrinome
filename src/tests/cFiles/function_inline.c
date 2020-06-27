// https://www.geeksforgeeks.org/inline-function-in-c/
#include <stdio.h> 

// another inline function
__attribute__((always_inline)) static inline int foo2(int x) 
{ 
    ++x;
} 
 
// Inline function 
__attribute__((always_inline)) static inline int foo(int x) 
{ 
    while (x < 23) {
        x = foo2(x);
        ++x;
    }

}  


int main() {
    // inline function call 
    int ret = 0;
    foo(ret);

    return 0;
}