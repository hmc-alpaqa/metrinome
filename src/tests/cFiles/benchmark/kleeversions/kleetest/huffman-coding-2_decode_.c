#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "c37c4725853548c7ab1aa723c7201ea3");

	node t;
	klee_make_symbolic(&t, sizeof(t), "7af521ab4fc34d25a90ffe387d74f602");
	decode(s, t);
	return 0;
}
