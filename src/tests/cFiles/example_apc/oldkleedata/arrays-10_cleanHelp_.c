#include <klee/klee.h>
#include </app/code/tests/cFiles/benchmark/kleeversions/files/arrays-10.c>
#define SIZE 10
int main() {

	node *el;
	klee_make_symbolic(&el, sizeof(el), "0566285a423f4831b9572927cb618154");
	cleanHelp(el);
	return 0;
}
