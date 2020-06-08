// https://www.thecrazyprogrammer.com/2015/05/c-program-for-longest-common-subsequence-problem.html

#include<stdio.h>
#include<string.h>

int i,j,m,n,c[20][20];
char x[20],y[20],b[20][20];

void lcs(char* x, char* y) {
    m=strlen(x);
    n=strlen(y);
    for(i=0;i<=m;i++)
                    c[i][0]=0;
    for(i=0;i<=n;i++)
                    c[0][i]=0;
                    
    //c, u and l denotes cross, upward and downward directions respectively
    for(i=1; i<=m; i++)
        for(j=1;j<=n;j++)
        {
            if(x[i-1]==y[j-1])
            {
                            c[i][j]=c[i-1][j-1]+1;
                            b[i][j]='c';
            }
            else if(c[i-1][j]>=c[i][j-1])
            {
                            c[i][j]=c[i-1][j];
                            b[i][j]='u';
            }
            else
            {
                            c[i][j]=c[i][j-1];
                            b[i][j]='l';
            }
        }
}
 
int main() {
    char * a = "ACFGHD";
    char * b = "ABFHD";
    lcs(a, b); // the longest common subsequence is AFHD
    return 0;
}