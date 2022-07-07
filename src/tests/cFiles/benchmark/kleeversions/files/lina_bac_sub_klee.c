#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  double** N;
  double* M;
  int I;
	klee_make_symbolic(&N, sizeof(N), "c111378af88246ebad10b00891184343");
  klee_make_symbolic(&M, sizeof(M), "548bc5a6acfb4a979248e11bba3df778");
  klee_make_symbolic(&I, sizeof(I), "3773fd6ed4ed4d8bbfb731e41766f4e3");
	bac_sub(N, M, I);
  return 0;
}
