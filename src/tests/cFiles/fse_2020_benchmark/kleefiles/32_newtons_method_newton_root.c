#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/32_newtons_method.c>
#define SIZE 100
int main() {

	float x0;
	klee_make_symbolic(&x0, sizeof(x0), "ec1065c7e8ae488899e8de3f276ec23f");

	float allerr;
	klee_make_symbolic(&allerr, sizeof(allerr), "8d4d783887fe4f7da3371decb370dd96");

	int maxmitr;
	klee_make_symbolic(&maxmitr, sizeof(maxmitr), "75c290cd344a4600b87a1be5fd10d3b1");
	return newton_root(x0, allerr, maxmitr);
}
