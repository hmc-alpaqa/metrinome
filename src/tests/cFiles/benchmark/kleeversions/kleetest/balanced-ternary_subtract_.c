#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	const char *b1;
	klee_make_symbolic(&b1, sizeof(b1), "4feb9669c17b49ca99a236cba33ed204");

	const char *b2;
	klee_make_symbolic(&b2, sizeof(b2), "f942fb8960f044ce90858571be05756c");

	char *out;
	klee_make_symbolic(&out, sizeof(out), "6fb937dc577e4922bc39abbfd3de5236");
	subtract(b1, b2, out);
	return 0;
}
