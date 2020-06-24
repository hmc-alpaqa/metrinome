#include <stdio.h> 

  
// Driver code 
int main() 
{ 
    int x = 10; 
  
    while (x < 15) {
        if (x > 5){
            x = 6;
            //printf("x is greater than 5"); 
        } else {
            x = 4;
            //printf("x is not greater than 5"); 
        }
    ++x;
    }
 

    if (x < 0) {
        return -1;
    } else {
        return 1;
    }
  
    //printf("Output is: %d\n", x; 
    return 0; 
}


// // Driver code 
// int main() 
// { 
//     int ret; 

//     while(ret < 0) {
//         ++ret;
//     }
//     // inline function call 
//     if (ret < 0) {
//         return -1;
//     } else {
//         return 1;
//     }
  
//     printf("Output is: %d\n", ret); 
//     return 0; 
// }
