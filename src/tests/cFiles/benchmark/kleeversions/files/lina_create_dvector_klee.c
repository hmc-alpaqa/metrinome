#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/lina.c>
#define SIZE 10
int main() {

  double N;
  double M;
  double I;
	klee_make_symbolic(&N, sizeof(N), "2ec4f2bb505f42bc8f7e168dc034947b");
  klee_make_symbolic(&M, sizeof(M), "5461f77c1e44494ebd8f7bdc3e15dff6");
  klee_make_symbolic(&I, sizeof(I), "5c521d78ff034e55bcb73cfe376485ee");
	create_dvector(N, M, I);
  return 0;
}
