#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/32_newtons_method.c>
#define SIZE 100
int main() {

	float x;
	klee_make_symbolic(&x, sizeof(x), "81dd6a1f6121492abf2a713ae9b35e83");
	return f(x);
}
