#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/01_greatestof3.c>
#define SIZE 100
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "8620f6e2b7c9411fb1cc8064477b5cab");

	int y;
	klee_make_symbolic(&y, sizeof(y), "9189e710f80440d7aa175d89844eea66");

	int z;
	klee_make_symbolic(&z, sizeof(z), "ceb9cefa66e047649fee060198bb86ba");
	return greatestof3(x, y, z);
}
