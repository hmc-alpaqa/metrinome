#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "e66eb338082c476dab420c6fca823909");

	node t;
	klee_make_symbolic(&t, sizeof(t), "a962449e3f354fdbb2278c9331242a9d");
	decode(s, t);
	return 0;
}
