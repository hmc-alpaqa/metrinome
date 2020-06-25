#include <stdio.h>
// it prints function calls - does not replace inlining :( 


int bounded_fib(int n) {
    int n1 = 0; 
    int n2 = 1;
    int count = 0;

    while(count < n && count < 100){
       int nth;
       nth = n1 + n2;
    
       n1 = n2;
       n2 = nth;

       count++;
    }
    return n1;
}

// https://www.programiz.com/c-programming/examples/source-code-output
int main() {
    int x = bounded_fib(2);
    FILE *fp;
    int c;
   
    // open the current input file
    fp = fopen(__FILE__,"r");

    do {
         c = getc(fp);   // read character 
         putchar(c);     // display character
    }
    while(c != EOF);  // loop until the end of file is reached
    
    fclose(fp);
    return 0;
}