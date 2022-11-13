#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/hailstone-sequence-2.c>
#define SIZE 10
int main() {

	ulong n;
	klee_make_symbolic(&n, sizeof(n), "652b2a162fdc487f9f42fe9a342fa119");
	return hailstone(n);
}
