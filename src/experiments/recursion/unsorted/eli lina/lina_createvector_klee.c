#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  int N;
  int M;
  int I;
	klee_make_symbolic(&N, sizeof(N), "050108b36bc146809a91ad69ef9cc3e6");
  klee_make_symbolic(&M, sizeof(M), "7424f67b3ede4418a0318087a60b905e");
  klee_make_symbolic(&I, sizeof(I), "0336925b15f2430db8c35e6d2fd06443");
	create_vector(N, M, I);
  return 0;
}