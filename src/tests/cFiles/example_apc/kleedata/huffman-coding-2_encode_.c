#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/huffman-coding-2.c>
#define SIZE 10
int main() {

	const char *s;
	klee_make_symbolic(&s, sizeof(s), "fc6e4692db884acc91cd66b80c947ae1");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "90d53b8ebabd49cdbb033f1fb4a765f0");
	encode(s, out);
	return 0;
}
