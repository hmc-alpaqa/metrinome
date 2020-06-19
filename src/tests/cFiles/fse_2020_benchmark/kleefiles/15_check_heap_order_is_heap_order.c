#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/15_check_heap_order.c>
#define SIZE 100
int main() {

	int a[SIZE];
	klee_make_symbolic(&a, sizeof(a), "fc1565a45da34567bf31931c35b73fc1");

	int n;
	klee_make_symbolic(&n, sizeof(n), "98faf62263f840deb1b1a8ef1d8caa1c");
	return is_heap_order(a, n);
}
