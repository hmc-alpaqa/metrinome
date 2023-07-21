#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int **N;
  int **M;
  int I;
  int J;
  int K;
	klee_make_symbolic(&N, sizeof(N), "f4cb6d4427ae43139ead246bc4f98d10");
  klee_make_symbolic(&M, sizeof(M), "7424f67b3ede4418a0318087a60b905e");
  klee_make_symbolic(&I, sizeof(I), "0336925b15f2430db8c35e6d2fd06443");
  klee_make_symbolic(&J, sizeof(J), "7b4a85df6c124b62b151adf24d645874");
  klee_make_symbolic(&K, sizeof(K), "7473722e942e4f1cbf509b7af9d6081e");
	cofactor(N, M, I, J, K);
  return 0;
}
