#include <klee/klee.h>
#include </app/code/tests/cFiles/nested_if.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "518e33d2f14e421c8274815b26a850a6");
	return nested_if_func(x);
}
