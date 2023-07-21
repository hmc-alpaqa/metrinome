#include<stdio.h>
#include<math.h>
#include<stdlib.h>
#include"lina.h"



//All values required below are user-inputed.

/*1)Programs for Vector Operations*/

    //Function to create and return a vector
Vector createvector(int i,int j,int k)
{
    Vector a={i,j,k};
    return a;
}
    //Function to create and return a vector of doubles
dVector create_dvector(double i,double j,double k)
{
    dVector a={i,j,k};
    return a;
}

void Read_Vector(Vector* V)
{
    int i1, j1, k1;
    printf("Enter i-component of vector: ");
    scanf("%d", &i1);
    printf("Enter j-component of vector: ");
    scanf("%d", &j1);
    printf("Enter k-component of vector: ");
    scanf("%d", &k1);
    V->i=i1;
    V->j=j1;
    V->k=k1;
}
    //Return largest element in vector of doubles
double max(dVector dv)
{
    double temp = dv.i > dv.j? dv.i: dv.j;
    double res = temp>dv.k? temp: dv.k;
    return res;   
}

    //Scale the vector of doubles by dividing all elements by the max value
dVector scale(dVector dv, double maxx)
{
    dv.i /= maxx;
    dv.j /= maxx;
    dv.k /= maxx;
    return dv;
}

    //Function to find dot product of two vectors
int dotProduct(Vector* a, Vector* b)
{
    return (a->i)*(b->i)+(a->j)*(b->j)+(a->k)*(b->k);
}

    //Function to find cross product of two vectors
void crossProduct(Vector* a, Vector* b, Vector* c)
{
    c->i = a->j*b->k - a->k*b->j;
    c->j = a->k*b->i - a->i*b->k;
    c->k = a->i*b->j - a->j*b->i;
}

    //Function to find scalar triple product of 3 vectors
int scalarTripleProduct(Vector* a,Vector* b,Vector* c)
{
    Vector* temp = malloc(sizeof(Vector));
    crossProduct(b,c, temp);
    int stp = dotProduct(a,temp);
    free(temp);
    return stp;
}

    //Function to find vector triple product of 3 vectors
void vectorTripleProduct(Vector* a,Vector* b,Vector* c, Vector* d)
{
    Vector* temp = malloc(sizeof(Vector));
    crossProduct(b,c, temp);
    crossProduct(a,temp, d);
    free(temp);
}

    //Function to print a vector
void printVector(Vector a)
{
    printf("< %d, %d, %d>\n",a.i,a.j,a.k);
}
    //Function to print a vector of doubles
void print_dVector(dVector dv)
{
    printf("<%.3lf, %.3lf, %.3lf>\n", dv.i, dv.j, dv.k);
}


/*2) Programs for Operations on Complex Numbers and Arrays of Complex Numbers.*/
void Read_cmpMat(COMPLEX **a, int n)
{
    int r, ima;
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            printf("Enter real part: "); scanf("%d", &r);
            printf("Enter imaginary part: "); scanf("%d", &ima);
            printf("\n");
            a[i][j].re = r; a[i][j].im = ima;
        }
    }
}

COMPLEX cmp(int a, int b)
{
    COMPLEX x = {a, b};
    return x;
}

void disp_cmpMat(COMPLEX** a, int n)
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
            printf("%d + %di\t", a[i][j].re, a[i][j].im);
        printf("\n");
    }
}
    //Function for finding conjugate of a complex number
COMPLEX conjugate(struct complex_no a)
{
    struct complex_no a_con;
    a_con.re=a.re;
    a_con.im=0-a.im;
    return a_con;
}

    //Function for transposing a complex matrix
void comp_transpose (COMPLEX ** a, int n)
{
    COMPLEX temp;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < i; j++)
        {
            temp = *(*(a + i) + j);
            *(*(a + i) + j) = *(*(a + j) + i);
            *(*(a + j) + i) = temp;
        }
    }
}

    //Function for checking if a complex matrix is hermitian or not
int ishermitian(COMPLEX **a, int n, COMPLEX** hermit)
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            *(*(hermit+i)+j)=*(*(a+i)+j);
        }
    }

    comp_transpose(hermit, n);

    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            *(*(hermit+i)+j)=conjugate(*(*(hermit+i)+j));
        }
    }

    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            if (a[i][j].re!=hermit[i][j].re && a[i][j].im != hermit[i][j].im) return 0;
        }
    }

    return 1;
}


/*3) Programs on Operations on Integers Arrays and Integer Matrices*/

void Read_intMat(int **a, int n)
{
    int r;
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            printf("Enter array element: ");
            scanf("%d", &r);
            a[i][j]=r;
        }
    }
}

void disp_intMat(int** a, int n)
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
            printf("%d\t", a[i][j]);
        printf("\n");
    }
}

void disp_floatMat(float **inv,int n)
{
    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
            printf("%.2f\t", inv[i][j]);
        printf("\n");
    }
}


    //Function for transposing integer 2D matrix
void transpose (float **a, int n)
{
    float temp;
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < i; j++)
        {
            temp = *(*(a + i) + j);
            *(*(a + i) + j) = *(*(a + j) + i);
            *(*(a + j) + i) = temp;
        }
    }
}

    //Function for finding cofactor of an array
        //**a --> source matrix
        //**b --> cofactor matrix
void cofactor (int **a, int **b, int i, int j, int n)
{
    int row = 0, col = 0;
    for (int loop_1 = 0; loop_1 < n; loop_1++)
    {
        for (int loop_2 = 0; loop_2 < n; loop_2++)
        {
            if (loop_1 != i && loop_2 != j)
            {
                *(*(b + row) + col) = *(*(a + loop_1) + loop_2);
                col++;
                if (col == (n - 1))
                {
                    col = 0;
                    row++;
                }
            }
        }
    }
}

    //Function for finding determinant of an array
int determinant (int **a, int n)
{
    int res = 0;
    int det_sign = 1;
    int **cof_matrix;

    if (n == 1)
    {
        return *(*(a + 0) + 0);
    }

    cof_matrix = (int **) malloc ((n - 1) * sizeof (int *));

    for (int i = 0; i < (n - 1); i++)
    {
        cof_matrix[i] = (int *) malloc ((n - 1) * sizeof (int));
    }

    for (int j = 0; j < n; j++)
    {
        cofactor (a, cof_matrix, 0, j, n);
        res += (det_sign * (*(*(a + 0) + j)) * determinant (cof_matrix, n - 1));
        det_sign = 0 - det_sign;
    }
 
    return res;
}

    //Function to find inverse of an array
        //**a --> pointer to the source matrix
        //**inv --> pointer to inverse matrix
void matrix_inverse (int **a, int n, float **inv)
{
    int d = determinant (a, n);
    int det_sign = 1;
    int res = 0;
    int **cof_matrix1;
    cof_matrix1 = malloc ((n - 1) * sizeof (int *));

    for (int i = 0; i < (n - 1); i++)
    {
        cof_matrix1[i] = malloc ((n - 1) * sizeof (int));
    }

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            cofactor (a, cof_matrix1, i, j, n);
            res = det_sign * determinant (cof_matrix1, n-1);
            inv[i][j] = (float) res;
            det_sign = 0 - det_sign;
        }
    }
    transpose (inv, n);

    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n; j++)
        {
            inv[i][j] = (float) inv[i][j]/(float) d;
        }
    }
}

    //Function for matrix multiplication
        //**mult1, **mult2 --> pointers to the multiplicand and the multiplier matrices.
        //**prod --> pointer to the product matrix.
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


/*4) Program to Solve a System of Simultaneous Linear Equations*/

    //Cramer's Rule: An explicit formula for the solving of linear equations; primarily useful in mesh analysis. Hence,
    //the notations here are typical of electrical engineering analysis, where **res --> pointer to the resistance matric
    //and *vol --> pointer to the voltage matrix.

void cramer(int **res, int *vol, float *sol, int n)
{
    int det=determinant(res, n);

    int **x;
    x=malloc(n*sizeof(int *));
    for (int i=0; i<n; i++)
    {
        x[i]=malloc(n*sizeof(int));
    }

    //Base Case: If determinant of the resistance matrix == 0, then infinite solutions exist.
    if (det==0)
    {
        printf("Infinite solutions");
        exit(0);
    }

    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            x[i][j]=res[i][j];
        }
    }

    for (int i=0; i<n; i++)
    {
        for (int j=0; j<n; j++)
        {
            x[j][i]=vol[j];
        }
        sol[i]= (float) determinant(x, n)/((float) det);
        for (int j=0; j<n; j++)
        {
            x[j][i]=res[j][i];
        }
    }

    free(x);
}

dVector vect_mat_multiplication(dVector v, double** mat)
{
    dVector result = create_dvector(0.0, 0.0, 0.0);
    int idx;
    result.i = (mat[0][0]*v.i + mat[0][1]*v.j + mat[0][2]*v.k);
    result.j = (mat[1][0]*v.i + mat[1][1]*v.j + mat[1][2]*v.k);
    result.k = (mat[2][0]*v.i + mat[2][1]*v.j + mat[2][2]*v.k);

    return result;
}

/*5) Program to compute dominant eigenvalues and eigenvectors for a 3x3 matrix using Rayleigh's Power Method*/

    //Function to check if the Iterative process has converged or not
    //eps is a small constant 
int has_converged(dVector x0, dVector x1)
{
    double eps = 1e-5;
    if(fabs(x0.i - x1.i) <= eps && fabs(x0.j - x1.j) <= eps && fabs(x0.k - x1.k <= eps))
        return 1;
    else
        return 0;
}

    //Function to carry out iterative Rayleigh's Power Method computation
void rpm(double** A)
{
    dVector x0 = create_dvector(1.0, 1.0, 1.0);
    dVector x1;
    double maxx = 0.0;
    int iter = 1;
    while(1)
    {
        x1 = vect_mat_multiplication(x0, A);
        //print_dVector(x0);
        maxx = max(x1);
        x1 = scale(x1, maxx);
        //print_dVector(x1);
        if(has_converged(x0, x1))
            break;
        else
        {
            x0 = x1;
        }
        printf("ITER %d\n",iter);
        iter++;
    }
    printf("Dominant Eigenvector:");
    print_dVector(x1);
    printf("Dominant Eigenvalue: %.3lf\n", maxx);
}

/* 6. Solving systems of linear equations using LUP Decomposition */

    // Returns the forward substitution vector.
double* for_sub(int* P, double* b, double** L, int n) {
    // NOTE: P, the permutation matrix, is compactly represented.
    
    double* y;
    y=(double*)malloc(sizeof(double)*n);

    double cnt=0;
    for (register int i=0; i<n; i++) {
        for (register int j=0; j<i; j++)
            cnt+=(L[i][j]*y[j]);
        y[i]=b[P[i]]-cnt;
        cnt=0;
    }

    printf("\n\n");

    return y;
}


    // Returns the back substituted vector
double* bac_sub(double** U, double* y, int n) {
    double* x;
    x=(double*)malloc(sizeof(double)*n);

    double cnt=0;
    for (register int i=n-1; i>=0; i--) {
        for (register int j=i+1; j<n; j++)
            cnt+=(double)(((float)U[i][j]) * ((float)x[j]));
        x[i] = (double) (y[i]-cnt)/U[i][i];
        cnt=0;
    }

    return x;
}


    // Return solution to linear equation system, provided its LUP decomposition.
double* lup_sol(double** L, double** U, int* P, double* B, int n) {
    double* y=for_sub(P, B, L, n);
    double* x=bac_sub(U, y, n);

    free(y);
    return x;
}
