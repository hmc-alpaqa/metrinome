#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  Vector* N;
  Vector* M;
  Vector* I;
	klee_make_symbolic(&N, sizeof(N), "f0fed4169ac24c67bbd937a361ce0df3");
  klee_make_symbolic(&M, sizeof(M), "6814abf2ad894e11b2c072143aea40a1");
  klee_make_symbolic(&I, sizeof(I), "bbca38b1980d40b684686d45d3e1d420");
	crossProduct(N, M, I);
  return 0;
}
