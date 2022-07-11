#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int** N;
  int M;
	klee_make_symbolic(&N, sizeof(N), "acde9f5bac7c45748ddc1b992363d66b");
  klee_make_symbolic(&M, sizeof(M), "d4dc03148fe441c58155be553f8a155d");
	disp_intMat(N, M);
  return 0;
}
