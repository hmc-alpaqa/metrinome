/*C program to print all prime numbers from 1 to N.*/

#include <stdio.h>

int mainn(int n)
{
    int i;
    //
    // printf("Enter the value of N: ");
    // scanf("%d",&n);

    // printf("All prime numbers are from 1 to %d:\n",n);
    for(i=1;i<=n;i++) {
        int flg = 0;
        int num = i;
        int result;
        /*if number (num) is divisble by any number from 2 to num/2
        number will not be prime.*/
        for(i=2;i<(num-1);i++) {
            if(num%i==0) {
                flg=1;
                break;
            }
        }
        if(flg) {
            result = 0;
        }
        else {
            result = 1;
        }
        if(result == 1){
            // printf("%d,",i);
        }
    }

    return 0;
}
