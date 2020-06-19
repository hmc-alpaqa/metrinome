#include <klee/klee.h>
#include </app/code/tests/cFiles/simpleAlgs/05_parity.c>
#define SIZE 100
int main() {

	int num;
	klee_make_symbolic(&num, sizeof(num), "a85ad5e2048743baa8322e0ad3f2389a");
	return parity(num);
}
