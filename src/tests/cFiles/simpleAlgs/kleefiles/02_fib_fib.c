#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/02_fib.c>
#define SIZE 100
int main() {

	int count;
	klee_make_symbolic(&count, sizeof(count), "55abb5de79344e88ac37021d135d6e34");
	return fib(count);
}
