#include <stdio.h>

// Finds inverse for 3x3 matrix
int main() {
    int mat[3][3], i, j;
    float determinant = 0;

    printf("Enter elements of the matrix row-wise:\n");
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            scanf("%d", &mat[i][j]);
        }
    }

    printf("\nGiven matrix is:\n");
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            printf("%d\t", mat[i][j]);
        }
        printf("\n");
    }

    // Finding determinant
    for (i = 0; i < 3; i++) {
        determinant = determinant + (mat[0][i] * (mat[1][(i + 1) % 3] * mat[2][(i + 2) % 3] - mat[1][(i + 2) % 3] * mat[2][(i + 1) % 3]));
    }

    printf("\nDeterminant: %f\n", determinant);
    printf("\nInverse of matrix is: \n");
    for (i = 0; i < 3; i++) {
        for (j = 0; j < 3; j++) {
            printf("%.2f\t", ((mat[(j + 1) % 3][(i + 1) % 3] * mat[(j + 2) % 3][(i + 2) % 3]) - (mat[(j + 1) % 3][(i + 2) % 3] * mat[(j + 2) % 3][(i + 1) % 3])) / determinant);
        }
        printf("\n");
    }

    return 0;
}