// Copied from experiments/recursion/files/lina.c

// Function for matrix multiplication
//     **mult1, **mult2 --> pointers to the multiplicand and the multiplier matrices.
//     **prod --> pointer to the product matrix.

void matrix_multiplication(int **mult1, float **mult2, float **prod, int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            prod[i][j]=0;
            for (int k = 0; k < n; k++)
            {
                prod[i][j]+=(mult1[i][k]*mult2[k][j]);
            }
        }
    }
}