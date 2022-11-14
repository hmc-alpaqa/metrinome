#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/sorting-algorithms-radix-sort.c>
#define SIZE 10
int main() {

	unsigned *from;
	klee_make_symbolic(&from, sizeof(from), "d3b59eb2b51c40f8a8e6be44cb3677c1");

	unsigned *to;
	klee_make_symbolic(&to, sizeof(to), "8b8530ecc2504770a982a7e4dcb49c70");

	unsigned bit;
	klee_make_symbolic(&bit, sizeof(bit), "7195c0819b9c4369803a2c66e64f238d");
	rad_sort_u(from, to, bit);
	return 0;
}
