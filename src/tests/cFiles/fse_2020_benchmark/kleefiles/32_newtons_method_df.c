#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/32_newtons_method.c>
#define SIZE 100
int main() {

	float x;
	klee_make_symbolic(&x, sizeof(x), "11f812d98c194a8fb7d9d3ca0371ef65");
	return df(x);
}
