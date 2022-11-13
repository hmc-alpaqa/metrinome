#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "20c53bdc9b4b4fc7a7283141c10a4fb3");
	init(s);
	return 0;
}
