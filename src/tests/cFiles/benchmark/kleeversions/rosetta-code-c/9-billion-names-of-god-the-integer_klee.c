#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/rosetta-code-c/9-billion-names-of-god-the-integer.c>
#define SIZE 10
int main() {

	int n;
	klee_make_symbolic(&n, sizeof(n), "e48c2080dfd14ce685335cfd77737b8d");
	if ((n<-1) || (n>1024)) {
		 return 0;}
	calc(n);
  return 0;
}
