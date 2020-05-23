#include <klee/klee.h>
#include </app/code/tests/cFiles/nested_if.c>
#define SIZE 10
int main() {

	int x;
	klee_make_symbolic(&x, sizeof(x), "521f260debf746aea76faee2cc76c9f4");
	return nested_if_func(x);
}
