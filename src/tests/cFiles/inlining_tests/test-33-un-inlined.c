#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

void check(int i, int j, int first, int last, int n) {
  if(n >=1 ){
    if (i == first || i == last || j == first || j == last)
        printf("%d ", n);
    else
        check(i, j, first + 1, last - 1, n - 1);
  }
}

int main() 
{
    int n;
    scanf("%d", &n);
    int rows = 2 * n - 1;

    for (int i = 0; i < rows; i ++) {
        for (int j = 0; j < rows; j ++) {
            check(i, j, 0, rows - 1, n);
        }
        printf("\n");
    }
    return 0;
}
