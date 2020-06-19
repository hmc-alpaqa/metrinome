#include <stdio.h>

void determinant(int a[2][2]) {
  int i, j, determinant;
  for (i = 0; i < 2; i++) {
    for (j = 0; j < 2; j++) {
      printf("%d\t", a[i][j]);  // to print the complete row
    }
    printf("\n");  // to move to the next row
  }

  // finding the determinant of a 2x2 matrix
  determinant = a[0][0] * a[1][1] - a[1][0] * a[0][1];
  printf("\n\nDterminant of 2x2 matrix is : %d - %d =  %d", a[0][0] * a[1][1],
         a[1][0] * a[0][1], determinant);
}

int main() {
  int a[2][2];
  a[0][0] = 1;
  a[0][1] = 2;
  a[1][0] = 5;
  a[1][1] = 9;
  determinant(a);
}
