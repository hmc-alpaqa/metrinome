#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/balanced-ternary.c>
#define SIZE 10
int main() {

	char *ptr;
	klee_make_symbolic(&ptr, sizeof(ptr), "33781ecaa5d942d49be6a4ff64386272");
	return last_char(ptr);
}
