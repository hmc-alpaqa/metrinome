#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int **N;
  int *M;
  float *I;
  int J;
	klee_make_symbolic(&N, sizeof(N), "54a8857d18cf4a5a9ca0a473e8b6468a");
  klee_make_symbolic(&M, sizeof(M), "a8a6c8658a5240219959a86ad4be03a3");
  klee_make_symbolic(&I, sizeof(I), "dada804db93243c6a2cd64b01a588110");
  klee_make_symbolic(&J, sizeof(J), "e3bcf766b4a94da6a21b114ec105432a");
	cramer(N, M, I, J);
  return 0;
}
