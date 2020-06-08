#include<stdio.h>

int main()
{
    printf("\n\n\t\tStudytonight - Best place to learn\n\n\n");

    int a[2][2], i, j;
    long determinant;

    printf("\n\nEnter the 4 elements of the array\n");
    for(i = 0; i < 2; i++)
    for(j = 0; j < 2; j++)
    scanf("%d", &a[i][j]);

    printf("\n\nThe entered matrix is: \n\n");
    for(i = 0; i < 2; i++)
    {
        for(j = 0; j < 2; j++)
        {
            printf("%d\t", a[i][j]);   // to print the complete row
        }
        printf("\n"); // to move to the next row
    }

    // finding the determinant of a 2x2 matrix
    determinant = a[0][0]*a[1][1] - a[1][0]*a[0][1];
    printf("\n\nDterminant of 2x2 matrix is : %d - %d =  %d", a[0][0]*a[1][1], a[1][0]*a[0][1], determinant);

    printf("\n\n\t\t\tCoding is Fun !\n\n\n");
    return 0;
}
