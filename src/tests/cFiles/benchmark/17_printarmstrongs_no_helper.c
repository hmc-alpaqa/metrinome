/*C program to print all Armstrong Numbers from 1 to N. */
 
#include <stdio.h>
 
int main()
{
    int i,n;
 
    printf("Enter the value of N: ");
    scanf("%d",&n);
 
    printf("All Armstrong numbers from 1 to %d:\n",n);
    for(i=1;i<=n;i++)
    {
        int tempNumber, rem, sum, result;
        tempNumber=i;
 
        sum=0;
        while(tempNumber!=0)
        {
            rem=tempNumber%10;
            sum=sum + (rem*rem*rem);
            tempNumber/=10;
        }  
        /* checking number is Armstrong or not */
        if(sum==i) { 
            result = 1;
        }
        else {
            result = 0;
        }

        if(result == 1) {
            printf("%d,",i);
        }
    }
     
    return 0;
}
