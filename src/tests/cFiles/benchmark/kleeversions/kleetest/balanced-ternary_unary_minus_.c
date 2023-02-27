#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b;
	klee_make_symbolic(&b, sizeof(b), "dab77bce53f647e48316ea036ff850a0");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "4b2de35e737a41ba8f083c3d04fc3ea7");
	unary_minus(b, out);
	return 0;
}
