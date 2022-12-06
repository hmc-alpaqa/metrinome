#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "5a28f18c7f164ce0a439c5b515c4916e");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "98c52017a28240958fe079cc134f2bd4");
	encode(s, out);
	return 0;
}
