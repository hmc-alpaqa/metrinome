#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "5a4cba0a501242ad98150db310e49b75");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "d736528f58ad4e4cb92b323e687597c2");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "3807c7667d4843af995d206d63ec7e05");
	add(b1, b2, out);
	return 0;
}
