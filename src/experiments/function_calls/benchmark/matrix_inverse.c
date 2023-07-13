#include <stdio.h>

#define N 3 // Change this value to match the size of the matrix

void getCofactor(int matrix[N][N], int temp[N][N], int p, int q, int n) {
    int i = 0, j = 0;

    for (int row = 0; row < n; row++) {
        for (int col = 0; col < n; col++) {
            if (row != p && col != q) {
                temp[i][j++] = matrix[row][col];

                if (j == n - 1) {
                    j = 0;
                    i++;
                }
            }
        }
    }
}

int determinant(int matrix[N][N], int n) {
    int D = 0;

    if (n == 1) {
        return matrix[0][0];
    }

    int temp[N][N];
    int sign = 1;

    for (int f = 0; f < n; f++) {
        getCofactor(matrix, temp, 0, f, n);
        D += sign * matrix[0][f] * determinant(temp, n - 1);
        sign = -sign;
    }

    return D;
}

void transpose(int matrix[N][N], int transposed[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            transposed[i][j] = matrix[j][i];
        }
    }
}

void adjoint(int matrix[N][N], int adj[N][N]) {
    if (N == 1) {
        adj[0][0] = 1;
        return;
    }

    int temp[N][N];
    int sign = 1;

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            getCofactor(matrix, temp, i, j, N);
            sign = ((i + j) % 2 == 0) ? 1 : -1;
            adj[j][i] = sign * determinant(temp, N - 1);
        }
    }
}

int inverse(int matrix[N][N], float inverse[N][N]) {
    int det = determinant(matrix, N);

    if (det == 0) {
        printf("Matrix is not invertible.\n");
        return 0;
    }

    int adj[N][N];
    adjoint(matrix, adj);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            inverse[i][j] = adj[i][j] / (float)det;
        }
    }

    return 1;
}

void displayMatrix(int matrix[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%d ", matrix[i][j]);
        }
        printf("\n");
    }
}

void displayInverse(float inverse[N][N]) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            printf("%.2f ", inverse[i][j]);
        }
        printf("\n");
    }
}

int main() {
    int matrix[N][N] = {
        {1, 2, -1},
        {2, 1, 2},
        {-1, 2, 1}
    };

    printf("Matrix:\n");
    displayMatrix(matrix);

    int det = determinant(matrix, N);
    printf("\nDeterminant: %d\n", det);

    int transposedMatrix[N][N];
    transpose(matrix, transposedMatrix);
    printf("\nTranspose:\n");
    displayMatrix(transposedMatrix);

    float inverseMatrix[N][N];
    int inv = inverse(matrix, inverseMatrix);

    if (inv) {
        printf("\nInverse:\n");
        displayInverse(inverseMatrix);
    }

    return 0;
}