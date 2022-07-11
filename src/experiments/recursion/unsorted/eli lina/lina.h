typedef struct vect1
{
    int i;
    int j;
    int k;
}Vector;

typedef struct vect2
{
    double i;
    double j;
    double k;
}dVector;

typedef struct complex_no
{
    int re;
    int im;
} COMPLEX ;

void Read_Vector(Vector*);

Vector createvector(int, int, int);

dVector create_dvector(double ,double ,double );

double max(dVector);

dVector scale(dVector, double);

int dotProduct(Vector*, Vector *);

void crossProduct(Vector* ,Vector*, Vector*);

int scalarTripleProduct(Vector* ,Vector* ,Vector*);

void vectorTripleProduct(Vector* ,Vector* ,Vector *, Vector*);

void printVector(Vector a);

void print_dVector(dVector dv);

void Read_cmpMat(COMPLEX**, int);

void disp_cmpMat(COMPLEX**, int);

COMPLEX cmp(int a, int b);

COMPLEX conjugate(struct complex_no a);

void comp_transpose (COMPLEX ** a, int n);

int ishermitian(COMPLEX**, int, COMPLEX**);

void Read_intMat(int**, int);

void disp_intMat(int**, int);

void disp_floatMat(float** , int);

void transpose (float **a, int n);

void cofactor (int **a, int **b, int i, int j, int n);

int determinant (int **a, int n);

void matrix_inverse (int **a, int n, float **cof_matrix2);

void matrix_multiplication(int **mult1, float **mult2, float **prod, int n);

dVector vect_mat_multiplication(dVector v, double** mat);  //3*3 matrix multiplied by 3*1 vector

void cramer(int **res, int *vol, float *sol, int n);

double* for_sub(int*, double*, double**, int);

double* bac_sub(double**, double*, int);

double* lup_sol(double**, double**, int*, double*, int);
