#include <stdio.h>

// Matrix multiplication for 3x3 matrices
void matrixMultiplication(int mat1[][3], int mat2[][3], int result[][3], int rows1, int cols1, int rows2, int cols2) {
    if (cols1 != rows2) {
        printf("Matrix multiplication is not possible.\n");
        return;
    }

    for (int i = 0; i < rows1; i++) {
        for (int j = 0; j < cols2; j++) {
            result[i][j] = 0;
            for (int k = 0; k < cols1; k++) {
                result[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }
}

void displayMatrix(int matrix[][3], int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
    printf("\n");
}

int main() {
    int mat1[3][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int mat2[3][3] = {{9, 8, 7}, {6, 5, 4}, {3, 2, 1}};
    int result[3][3];

    int rows1 = 3, cols1 = 3;
    int rows2 = 3, cols2 = 3;

    printf("Matrix 1:\n");
    displayMatrix(mat1, rows1, cols1);

    printf("Matrix 2:\n");
    displayMatrix(mat2, rows2, cols2);

    matrixMultiplication(mat1, mat2, result, rows1, cols1, rows2, cols2);

    printf("Resultant Matrix:\n");
    displayMatrix(result, rows1, cols2);

    return 0;
}