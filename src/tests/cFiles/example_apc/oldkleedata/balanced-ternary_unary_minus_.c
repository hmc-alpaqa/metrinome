#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b;
	klee_make_symbolic(&b, sizeof(b), "dc8d1458e8f74feaaa645625d24d038e");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "f490c62d73cc46578b4136936ceb1ddd");
	unary_minus(b, out);
	return 0;
}
